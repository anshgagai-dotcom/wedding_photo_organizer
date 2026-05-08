import os
from dotenv import load_dotenv

load_dotenv()

# Environment settings
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llava:latest")

# Processing settings
MAX_IMAGES_PER_BATCH = int(os.getenv("MAX_IMAGES_PER_BATCH", 50))
ENABLE_DUPLICATE_CHECK = os.getenv("ENABLE_DUPLICATE_CHECK", "True") == "True"
ENABLE_BLUR_CHECK = os.getenv("ENABLE_BLUR_CHECK", "True") == "True"






