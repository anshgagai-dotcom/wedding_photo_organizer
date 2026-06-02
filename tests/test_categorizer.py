from src.metadata.models import GeminiPhotoSignal
from src.organizer.categorizer import WeddingCategorizer


def test_couple_category_detection() -> None:
    categorizer = WeddingCategorizer()
    signal = GeminiPhotoSignal(
        scene="Bride and groom on stage",
        people_count=2,
        event_type="stage",
        bride_present=True,
        groom_present=True,
        emotions=["happy"],
        attire=["lehenga", "sherwani"],
        location_context="stage",
        venue_type="indoor",
        photo_category="unknown",
        confidence_score=0.91,
        tags=["wedding", "stage"],
    )
    assert categorizer.determine_category(signal) == "Couple"
