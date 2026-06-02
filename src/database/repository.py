from __future__ import annotations

import json
import sqlite3
from typing import Any

import pandas as pd

from src.database.connection import create_connection
from src.metadata.models import PhotoMetadata


class MetadataRepository:
    def __init__(self) -> None:
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with create_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS photo_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo_name TEXT NOT NULL,
                    path TEXT NOT NULL UNIQUE,
                    filename TEXT NOT NULL,
                    category TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    people_count INTEGER NOT NULL,
                    scene_description TEXT NOT NULL,
                    bride_present INTEGER NOT NULL,
                    groom_present INTEGER NOT NULL,
                    emotions TEXT NOT NULL,
                    attire TEXT NOT NULL,
                    venue_type TEXT NOT NULL,
                    location_context TEXT NOT NULL,
                    duplicate_of TEXT NULL,
                    duplicate_similarity REAL NOT NULL,
                    is_blurry INTEGER NOT NULL,
                    blur_score REAL NOT NULL,
                    blur_label TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def upsert_many(self, records: list[PhotoMetadata]) -> None:
        payload = [
            (
                item.photo_name,
                item.path,
                item.filename,
                item.category,
                json.dumps(item.tags),
                item.event_type,
                item.confidence_score,
                item.timestamp,
                item.people_count,
                item.scene_description or item.scene,
                int(item.bride_present),
                int(item.groom_present),
                json.dumps(item.emotions),
                json.dumps(item.attire),
                item.venue_type,
                item.location_context,
                item.duplicate_of,
                item.duplicate_similarity,
                int(item.is_blurry),
                item.blur_score,
                item.blur_label,
            )
            for item in records
        ]
        if not payload:
            return

        with create_connection() as conn:
            conn.executemany(
                """
                INSERT INTO photo_metadata (
                    photo_name, path, filename, category, tags, event_type, confidence_score, timestamp,
                    people_count, scene_description, bride_present, groom_present, emotions, attire,
                    venue_type, location_context, duplicate_of, duplicate_similarity, is_blurry, blur_score, blur_label
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    photo_name=excluded.photo_name,
                    filename=excluded.filename,
                    category=excluded.category,
                    tags=excluded.tags,
                    event_type=excluded.event_type,
                    confidence_score=excluded.confidence_score,
                    timestamp=excluded.timestamp,
                    people_count=excluded.people_count,
                    scene_description=excluded.scene_description,
                    bride_present=excluded.bride_present,
                    groom_present=excluded.groom_present,
                    emotions=excluded.emotions,
                    attire=excluded.attire,
                    venue_type=excluded.venue_type,
                    location_context=excluded.location_context,
                    duplicate_of=excluded.duplicate_of,
                    duplicate_similarity=excluded.duplicate_similarity,
                    is_blurry=excluded.is_blurry,
                    blur_score=excluded.blur_score,
                    blur_label=excluded.blur_label
                """,
                payload,
            )
            conn.commit()

    def fetch_all(self) -> list[PhotoMetadata]:
        with create_connection() as conn:
            rows = conn.execute(
                """
                SELECT photo_name, path, filename, category, tags, event_type, confidence_score, timestamp,
                       people_count, scene_description, bride_present, groom_present, emotions, attire,
                       venue_type, location_context, duplicate_of, duplicate_similarity, is_blurry, blur_score, blur_label
                FROM photo_metadata
                ORDER BY id DESC
                """
            ).fetchall()
        return [self._row_to_model(row) for row in rows]

    def search(self, query: str) -> list[PhotoMetadata]:
        tokens = [token.strip().lower() for token in query.split() if token.strip()]
        if not tokens:
            return self.fetch_all()
        with create_connection() as conn:
            rows = conn.execute(
                """
                SELECT photo_name, path, filename, category, tags, event_type, confidence_score, timestamp,
                       people_count, scene_description, bride_present, groom_present, emotions, attire,
                       venue_type, location_context, duplicate_of, duplicate_similarity, is_blurry, blur_score, blur_label
                FROM photo_metadata
                """
            ).fetchall()
        candidates = [self._row_to_model(row) for row in rows]
        output: list[PhotoMetadata] = []
        for item in candidates:
            haystack = " ".join(
                [
                    item.category,
                    item.event_type,
                    item.scene_description,
                    item.venue_type,
                    " ".join(item.tags),
                    " ".join(item.emotions),
                    " ".join(item.attire),
                ]
            ).lower()
            if all(token in haystack for token in tokens):
                output.append(item)
        return output

    def analytics(self) -> dict[str, Any]:
        records = self.fetch_all()
        if not records:
            return {"total_photos": 0, "duplicates": 0, "blurry": 0, "top_categories": {}}
        frame = pd.DataFrame([item.model_dump() for item in records])
        return {
            "total_photos": int(len(frame)),
            "duplicates": int(frame["duplicate_of"].notna().sum()),
            "blurry": int(frame["is_blurry"].sum()),
            "top_categories": frame["category"].value_counts().head(10).to_dict(),
            "avg_confidence": float(frame["confidence_score"].mean()),
        }

    @staticmethod
    def _row_to_model(row: sqlite3.Row | tuple[Any, ...]) -> PhotoMetadata:
        (
            photo_name,
            path,
            filename,
            category,
            tags,
            event_type,
            confidence_score,
            timestamp,
            people_count,
            scene_description,
            bride_present,
            groom_present,
            emotions,
            attire,
            venue_type,
            location_context,
            duplicate_of,
            duplicate_similarity,
            is_blurry,
            blur_score,
            blur_label,
        ) = row

        return PhotoMetadata(
            photo_name=photo_name,
            path=path,
            filename=filename,
            category=category,
            photo_category=category,
            tags=json.loads(tags),
            event_type=event_type,
            confidence_score=float(confidence_score),
            timestamp=timestamp,
            people_count=int(people_count),
            scene=scene_description,
            scene_description=scene_description,
            bride_present=bool(bride_present),
            groom_present=bool(groom_present),
            emotions=json.loads(emotions),
            attire=json.loads(attire),
            venue_type=venue_type,
            location_context=location_context,
            duplicate_of=duplicate_of,
            duplicate_similarity=float(duplicate_similarity),
            is_blurry=bool(is_blurry),
            blur_score=float(blur_score),
            blur_label=blur_label,
        )
