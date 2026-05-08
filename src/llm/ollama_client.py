import requests
import json
import base64
from pathlib import Path

from src.core.settings import OLLAMA_URL, OLLAMA_MODEL


class OllamaClient:
    """
    Local Ollama multimodal client for wedding image analysis
    """

    def __init__(self):
        self.api_url = f"{OLLAMA_URL}/api/generate"
        self.model = OLLAMA_MODEL

    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Converts image to base64 for Ollama API
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        except Exception as e:
            print(f"Image encoding failed: {e}")
            return ""

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Sends image + prompt to Ollama
        Returns raw model response
        """
        try:
            image_data = self.encode_image_to_base64(image_path)

            if not image_data:
                return ""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_data],
                "stream": False
            }

            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            return result.get("response", "")

        except requests.exceptions.RequestException as e:
            print(f"Ollama request failed: {e}")
            return ""

        except Exception as e:
            print(f"Ollama image analysis failed: {e}")
            return ""

    def check_connection(self) -> bool:
        """
        Checks if Ollama server is running
        """
        try:
            response = requests.get(f"{OLLAMA_URL}", timeout=5)
            return response.status_code == 200

        except Exception:
            return False