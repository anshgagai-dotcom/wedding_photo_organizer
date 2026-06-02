from pathlib import Path

from PIL import Image

from src.image_processing.duplicates import DuplicateDetector


def _make_image(path: Path, color: tuple[int, int, int]) -> None:
    image = Image.new("RGB", (64, 64), color=color)
    image.save(path)


def test_duplicate_detection(tmp_path: Path) -> None:
    first = tmp_path / "a.jpg"
    second = tmp_path / "b.jpg"
    _make_image(first, (255, 0, 0))
    _make_image(second, (255, 0, 0))

    detector = DuplicateDetector(threshold=6)
    original, score_first = detector.find_duplicate_of(first)
    duplicate_of, score_second = detector.find_duplicate_of(second)

    assert original is None
    assert score_first == 0.0
    assert duplicate_of is not None
    assert score_second > 0.8
