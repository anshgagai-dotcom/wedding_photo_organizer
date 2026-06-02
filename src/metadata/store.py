from __future__ import annotations

import json
from pathlib import Path

from src.database.repository import MetadataRepository
from src.metadata.models import PhotoMetadata


class MetadataStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.repository = MetadataRepository()

    def save(self, records: list[PhotoMetadata]) -> None:
        payload = [record.model_dump() for record in records]
        self.file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.repository.upsert_many(records)

    def load(self) -> list[PhotoMetadata]:
        db_records = self.repository.fetch_all()
        if db_records:
            return db_records
        if not self.file_path.exists():
            return []
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [PhotoMetadata.model_validate(item) for item in data]
