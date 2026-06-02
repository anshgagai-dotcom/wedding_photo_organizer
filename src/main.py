from __future__ import annotations

from dataclasses import dataclass

from dotenv import load_dotenv

from src.config.config import AppConfig, get_config
from src.logging.logging_setup import get_logger
from src.metadata.store import MetadataStore
from src.pipeline import WeddingPhotoPipeline
from src.utils.file_utils import scan_images
from src.utils.notifications import NotificationService


LOGGER = get_logger(__name__)


@dataclass
class PipelineRunSummary:
    ingested: int
    analyzed: int
    organized: int
    category_distribution: dict[str, int]


def load_environment() -> AppConfig:
    load_dotenv(override=False)
    config = get_config()
    missing = [name for name, value in config.required_external_keys.items() if not value.strip()]
    if missing:
        LOGGER.error(
            "Missing environment keys: %s. Running in fallback-safe mode for external integrations.",
            ", ".join(missing),
        )
    else:
        LOGGER.info("All required external environment keys are configured.")
    return config


def run_pipeline() -> PipelineRunSummary:
    config = load_environment()

    LOGGER.info("Step 1/6: Ingest input photos from %s", config.input_dir)
    image_paths = scan_images(config.input_dir)
    LOGGER.info("Found %d image(s) for processing.", len(image_paths))

    LOGGER.info("Step 2/6: Initialize metadata and processing pipeline.")
    store = MetadataStore(config.metadata_file)
    pipeline = WeddingPhotoPipeline(settings=config, metadata_store=store)

    LOGGER.info("Step 3/6: Run metadata extraction, Gemini classification, duplicate and blur checks.")
    analysis_result = pipeline.analyze_all()

    LOGGER.info("Step 4/6: Persist metadata and quality signals.")
    LOGGER.info("Analyzed=%d categories=%s", analysis_result.total_analyzed, analysis_result.category_distribution)

    LOGGER.info("Step 5/6: Organize photos into category folders.")
    organized_count = pipeline.organize_all()

    LOGGER.info("Step 6/6: Notify pipeline completion (safe stub).")
    notifier = NotificationService(config)
    notifier.send_pipeline_summary(
        subject="Wedding Photo Organizer run completed",
        body=(
            f"Ingested={len(image_paths)}, Analyzed={analysis_result.total_analyzed}, "
            f"Organized={organized_count}, Categories={analysis_result.category_distribution}"
        ),
    )

    return PipelineRunSummary(
        ingested=len(image_paths),
        analyzed=analysis_result.total_analyzed,
        organized=organized_count,
        category_distribution=analysis_result.category_distribution,
    )


def main() -> int:
    LOGGER.info("Starting Wedding Photo Organizer pipeline via python -m src.main")
    summary = run_pipeline()
    LOGGER.info(
        "Pipeline completed successfully. Ingested=%d Analyzed=%d Organized=%d",
        summary.ingested,
        summary.analyzed,
        summary.organized,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
