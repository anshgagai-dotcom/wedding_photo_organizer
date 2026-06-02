from __future__ import annotations

from src.metadata.models import PhotoMetadata


class SearchEngine:
    def search(self, records: list[PhotoMetadata], query: str) -> list[PhotoMetadata]:
        tokens = [item.strip().lower() for item in query.split() if item.strip()]
        if not tokens:
            return records

        matched: list[PhotoMetadata] = []
        for record in records:
            haystack = " ".join(
                [
                    record.scene,
                    record.scene_description,
                    record.event_type,
                    record.category,
                    record.primary_category,
                    record.venue_type,
                    record.location_context,
                    " ".join(record.tags),
                    " ".join(record.emotions),
                    " ".join(record.attire),
                ]
            ).lower()
            if all(token in haystack for token in tokens):
                matched.append(record)
        return matched
