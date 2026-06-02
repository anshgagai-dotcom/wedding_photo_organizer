from __future__ import annotations

from src.metadata.models import GeminiPhotoSignal


WEDDING_CATEGORIES = {
    "Bride",
    "Groom",
    "Couple",
    "Family",
    "Group",
    "Stage",
    "Candid",
    "Portrait",
    "Decoration",
    "Ceremony",
    "Reception",
}


class WeddingCategorizer:
    def determine_category(self, signal: GeminiPhotoSignal) -> str:
        candidate = signal.photo_category.strip().title()
        if candidate in WEDDING_CATEGORIES:
            return candidate

        if signal.bride_present and signal.groom_present:
            return "Couple"
        if signal.bride_present:
            return "Bride"
        if signal.groom_present:
            return "Groom"
        if signal.people_count >= 6:
            return "Group"
        if "family" in " ".join(signal.tags).lower():
            return "Family"
        if "stage" in signal.scene.lower() or signal.event_type == "stage":
            return "Stage"
        if "decoration" in " ".join(signal.tags).lower():
            return "Decoration"
        if signal.event_type == "ceremony":
            return "Ceremony"
        if signal.event_type == "reception":
            return "Reception"
        if signal.people_count <= 2:
            return "Portrait"
        return "Candid"
