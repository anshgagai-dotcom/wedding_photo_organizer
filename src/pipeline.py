from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable

from src.config.config import AppConfig
from src.image_processing.duplicates import DuplicateDetector
from src.image_processing.quality import blur_label, is_blurry
from src.llm.image_analysis_service import ImageAnalysisService
from src.metadata.models import BatchAnalysisResult, PhotoMetadata
from src.metadata.store import MetadataStore
from src.organizer.categorizer import WeddingCategorizer
from src.organizer.organizer_service import PhotoOrganizerService
from src.utils.file_utils import scan_images
from src.logging.logging_setup import get_logger


LOGGER = get_logger(__name__)


class WeddingPhotoPipeline:
    def __init__(self, settings: AppConfig, metadata_store: MetadataStore) -> None:
        self.settings = settings
        self.store = metadata_store
        self.analysis_service = ImageAnalysisService(settings)
        self.categorizer = WeddingCategorizer()
        self.duplicate_detector = DuplicateDetector(settings.duplicate_hash_threshold)
        self.organizer = PhotoOrganizerService(settings)

    def analyze_all(self, progress_cb: Callable[[int, int], None] | None = None) -> BatchAnalysisResult:
        image_paths = scan_images(self.settings.input_dir)
        if not image_paths:
            return BatchAnalysisResult()

        results: list[PhotoMetadata] = []
        workers = min(8, self.settings.batch_size)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(self._analyze_single, path): path for path in image_paths}
            total = len(futures)
            done = 0
            for future in as_completed(futures):
                image_path = futures[future]
                try:
                    results.append(future.result())
                except Exception as exc:  # noqa: BLE001
                    LOGGER.exception("Failed processing %s: %s", image_path, exc)
                done += 1
                if progress_cb:
                    progress_cb(done, total)

        self.store.save(results)
        category_distribution = dict(Counter(item.primary_category for item in results))
        return BatchAnalysisResult(
            total_analyzed=len(results),
            category_distribution=category_distribution,
            sample=results[:5],
        )

    def organize_all(self) -> int:
        records = self.store.load()
        return self.organizer.organize(records)

    def _analyze_single(self, image_path: Path) -> PhotoMetadata:
        signal = self.analysis_service.analyze(image_path)
        category = self.categorizer.determine_category(signal)
        duplicate_of, duplicate_similarity = self.duplicate_detector.find_duplicate_of(image_path)
        blurry, blur_score = is_blurry(image_path, self.settings.blur_threshold)
        quality_label = blur_label(blur_score, self.settings.blur_threshold)

        return PhotoMetadata(
            photo_name=image_path.name,
            path=str(image_path.resolve()),
            filename=image_path.name,
            category=category,
            confidence_score=signal.confidence_score,
            timestamp=datetime.now(UTC).isoformat(),
            scene=signal.scene,
            scene_description=signal.scene,
            people_count=signal.people_count,
            event_type=signal.event_type,
            bride_present=signal.bride_present,
            groom_present=signal.groom_present,
            emotions=signal.emotions,
            attire=signal.attire,
            venue_type=signal.venue_type,
            location_context=signal.location_context,
            photo_category=category,
            tags=signal.tags,
            duplicate_of=duplicate_of,
            duplicate_similarity=duplicate_similarity,
            is_blurry=blurry,
            blur_score=blur_score,
            blur_label=quality_label,
        )
