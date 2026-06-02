from __future__ import annotations

from pathlib import Path

import cv2


def laplacian_blur_score(image_path: Path) -> float:
    image = cv2.imread(str(image_path))
    if image is None:
        return 0.0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def is_blurry(image_path: Path, threshold: float) -> tuple[bool, float]:
    score = laplacian_blur_score(image_path)
    return score < threshold, score


def blur_label(score: float, threshold: float) -> str:
    if score >= threshold * 1.5:
        return "sharp"
    if score >= threshold:
        return "acceptable"
    return "blurry"
