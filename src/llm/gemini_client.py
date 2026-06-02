from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import google.generativeai as genai
from PIL import Image
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from src.config.config import AppConfig
from src.llm.prompt_templates import GEMINI_IMAGE_ANALYSIS_PROMPT
from src.metadata.models import GeminiPhotoSignal
from src.logging.logging_setup import get_logger


LOGGER = get_logger(__name__)


class GeminiVisionClient:
    def __init__(self, settings: AppConfig) -> None:
        self.settings = settings
        self.fallback_mode = not bool(settings.gemini_api_key.strip())
        self.model = None
        if self.fallback_mode:
            LOGGER.warning("GEMINI_API_KEY missing. Using mock Gemini fallback mode.")
            return
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(Exception),
    )
    def _generate_with_retry(self, image: Image.Image) -> str:
        if self.model is None:
            raise RuntimeError("Gemini model unavailable in fallback mode.")
        response = self.model.generate_content(
            [GEMINI_IMAGE_ANALYSIS_PROMPT, image],
            generation_config={"response_mime_type": "application/json"},
        )
        return response.text or "{}"

    def analyze_image(self, image_path: Path) -> GeminiPhotoSignal:
        if self.fallback_mode:
            payload = self._fallback_payload()
            payload["scene"] = f"Fallback analysis for {image_path.name}"
            payload["tags"] = ["fallback_mode", "mock_classification"]
            payload["confidence_score"] = 0.2
            return GeminiPhotoSignal.from_dict(payload)
        try:
            with Image.open(image_path) as image:
                raw = self._generate_with_retry(image)
            parsed = self._extract_json(raw)
            return GeminiPhotoSignal.from_dict(parsed)
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Gemini analysis failed for %s: %s", image_path, exc)
            return GeminiPhotoSignal.from_dict(self._fallback_payload())

    @staticmethod
    def _extract_json(raw: str) -> dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(raw[start:end])
            raise

    @staticmethod
    def _fallback_payload() -> dict[str, Any]:
        return {
            "scene": "",
            "people_count": 0,
            "event_type": "other",
            "bride_present": False,
            "groom_present": False,
            "emotions": [],
            "attire": [],
            "location_context": "other",
            "venue_type": "other",
            "photo_category": "Candid",
            "confidence_score": 0.0,
            "tags": ["analysis_failed"],
        }
