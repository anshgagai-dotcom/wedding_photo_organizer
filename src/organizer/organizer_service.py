from __future__ import annotations

import shutil
from pathlib import Path

from src.config.config import AppConfig
from src.metadata.models import PhotoMetadata


class PhotoOrganizerService:
    def __init__(self, settings: AppConfig) -> None:
        self.settings = settings

    def organize(self, records: list[PhotoMetadata]) -> int:
        count = 0
        for record in records:
            source = Path(record.path)
            if not source.exists():
                continue
            target_dir = self.settings.organized_dir / record.primary_category
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / source.name
            shutil.copy2(source, target)
            count += 1
        return count
