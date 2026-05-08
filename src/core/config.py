from pathlib import Path

# Root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Main folders
INPUT_DIR = BASE_DIR / "input_photos"
NON_FACES_DIR = BASE_DIR / "non_faces"
OUTPUT_DIR = BASE_DIR / "output_photos"
REPORTS_DIR = BASE_DIR / "reports"
KNOWN_FACES_DIR = BASE_DIR / "known_faces"

# Supported image extensions
SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

# Wedding categories
WEDDING_CATEGORIES = [
    "Haldi",
    "Mehendi",
    "Sangeet",
    "Baraat",
    "Wedding_Ceremony",
    "Bride_Solo",
    "Groom_Solo",
    "Couple_Portraits",
    "Family",
    "Group_Photos",
    "Candid",
    "Traditional",
    "Reception",
    "Decoration",
    "Food",
    "Miscellaneous"
]

# Blur threshold
BLUR_THRESHOLD = 100.0

# Face recognition tolerance
FACE_MATCH_THRESHOLD = 0.45

# Ollama config
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llava:latest"

# Best shots confidence
BEST_SHOT_THRESHOLD = 0.85





