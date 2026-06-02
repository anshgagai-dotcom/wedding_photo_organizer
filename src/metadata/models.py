from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class PhotoMetadata(BaseModel):
    photo_name: str = ""
    path: str
    filename: str
    category: str = "Candid"
    confidence_score: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    scene: str = ""
    scene_description: str = ""
    people_count: int = 0
    event_type: str = "other"
    bride_present: bool = False
    groom_present: bool = False
    emotions: list[str] = Field(default_factory=list)
    attire: list[str] = Field(default_factory=list)
    location_context: str = "other"
    venue_type: str = "other"
    photo_category: str = "Candid"
    tags: list[str] = Field(default_factory=list)
    duplicate_of: str | None = None
    duplicate_similarity: float = 0.0
    is_blurry: bool = False
    blur_score: float = 0.0
    blur_label: str = "unknown"

    @property
    def primary_category(self) -> str:
        return self.category or self.photo_category


class BatchAnalysisResult(BaseModel):
    total_analyzed: int = 0
    category_distribution: dict[str, int] = Field(default_factory=dict)
    sample: list[PhotoMetadata] = Field(default_factory=list)


class GeminiPhotoSignal(BaseModel):
    scene: str
    people_count: int
    event_type: str
    bride_present: bool
    groom_present: bool
    emotions: list[str]
    attire: list[str]
    location_context: str
    venue_type: str
    photo_category: str
    confidence_score: float
    tags: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GeminiPhotoSignal":
        return cls(
            scene=str(payload.get("scene", "")),
            people_count=int(payload.get("people_count", 0)),
            event_type=str(payload.get("event_type", "other")),
            bride_present=bool(payload.get("bride_present", False)),
            groom_present=bool(payload.get("groom_present", False)),
            emotions=[str(item) for item in payload.get("emotions", [])],
            attire=[str(item) for item in payload.get("attire", payload.get("clothing", []))],
            location_context=str(payload.get("location_context", "other")),
            venue_type=str(payload.get("venue_type", payload.get("location_context", "other"))),
            photo_category=str(payload.get("photo_category", "Candid")),
            confidence_score=float(payload.get("confidence_score", 0.0)),
            tags=[str(item) for item in payload.get("tags", [])],
        )
