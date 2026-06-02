from src.metadata.models import PhotoMetadata
from src.search.query_engine import SearchEngine


def test_search_matches_query_tokens() -> None:
    records = [
        PhotoMetadata(
            photo_name="b1.jpg",
            path="/tmp/b1.jpg",
            filename="b1.jpg",
            category="Bride",
            photo_category="Bride",
            scene_description="Bride smiling on reception stage",
            event_type="reception",
            tags=["bride", "stage"],
            emotions=["happy"],
            attire=["lehenga"],
        ),
        PhotoMetadata(
            photo_name="f1.jpg",
            path="/tmp/f1.jpg",
            filename="f1.jpg",
            category="Family",
            photo_category="Family",
            scene_description="Family group portrait",
            event_type="ceremony",
            tags=["family"],
        ),
    ]
    matches = SearchEngine().search(records, "bride reception")
    assert len(matches) == 1
    assert matches[0].category == "Bride"
