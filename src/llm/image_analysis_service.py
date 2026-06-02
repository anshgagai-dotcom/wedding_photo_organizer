from __future__ import annotations

from pathlib import Path

from src.config.config import AppConfig
from src.llm.gemini_client import GeminiVisionClient
from src.metadata.models import GeminiPhotoSignal


class ImageAnalysisService:
    """Service layer for image understanding with Gemini Vision."""

    def __init__(self, settings: AppConfig) -> None:
        self.client = GeminiVisionClient(settings)

    def analyze(self, image_path: Path) -> GeminiPhotoSignal:
        return self.client.analyze_image(image_path)
