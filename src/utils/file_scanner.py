from pathlib import Path
from typing import List
from src.core.config import SUPPORTED_IMAGE_EXTENSIONS


class FileScanner:
    def __init__(self, input_dir: Path):
        self.input_dir = input_dir

    def scan_images(self) -> List[Path]:
        image_files = []

        for file_path in self.input_dir.rglob("*"):
            if file_path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
                image_files.append(file_path)

        return image_files