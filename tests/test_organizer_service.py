from pathlib import Path

from PIL import Image

from src.config.config import AppConfig
from src.metadata.models import PhotoMetadata
from src.organizer.organizer_service import PhotoOrganizerService


def test_organize_moves_into_category(tmp_path: Path) -> None:
    input_dir = tmp_path / "input_photos"
    output_dir = tmp_path / "organized_photos"
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    file_path = input_dir / "sample.jpg"
    Image.new("RGB", (20, 20), color=(10, 20, 30)).save(file_path)

    config = AppConfig(base_dir=tmp_path)
    metadata = PhotoMetadata(
        photo_name="sample.jpg",
        path=str(file_path),
        filename="sample.jpg",
        category="Bride",
        photo_category="Bride",
    )

    count = PhotoOrganizerService(config).organize([metadata])
    assert count == 1
    assert (output_dir / "Bride" / "sample.jpg").exists()
