from __future__ import annotations

from pathlib import Path

import imagehash
from PIL import Image


class DuplicateDetector:
    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        self._hash_by_path: dict[str, imagehash.ImageHash] = {}

    def find_duplicate_of(self, image_path: Path) -> tuple[str | None, float]:
        current_hash = imagehash.phash(Image.open(image_path))
        best_path: str | None = None
        best_similarity = 0.0
        for existing_path, existing_hash in self._hash_by_path.items():
            distance = current_hash - existing_hash
            similarity = max(0.0, 1.0 - (distance / 64.0))
            if distance <= self.threshold and similarity > best_similarity:
                best_path = existing_path
                best_similarity = similarity
        self._hash_by_path[str(image_path)] = current_hash
        return best_path, best_similarity
