from pathlib import Path

import cv2
import numpy as np

from src.image_processing.quality import blur_label, laplacian_blur_score


def test_blur_label_and_score(tmp_path: Path) -> None:
    sharp_path = tmp_path / "sharp.jpg"
    blurry_path = tmp_path / "blurry.jpg"

    sharp = np.zeros((200, 200, 3), dtype=np.uint8)
    sharp[:, :100] = 255
    cv2.imwrite(str(sharp_path), sharp)

    blurry = cv2.GaussianBlur(sharp, (31, 31), 0)
    cv2.imwrite(str(blurry_path), blurry)

    sharp_score = laplacian_blur_score(sharp_path)
    blurry_score = laplacian_blur_score(blurry_path)

    assert sharp_score > blurry_score
    assert blur_label(blurry_score, threshold=120.0) in {"blurry", "acceptable"}
