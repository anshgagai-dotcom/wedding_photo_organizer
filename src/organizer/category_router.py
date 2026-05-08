from pathlib import Path

from src.core.config import OUTPUT_DIR


class CategoryRouter:
    """
    Routes images into category-based folders
    """

    def __init__(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def get_category_folder(self, category: str) -> Path:
        """
        Returns category folder path
        """
        safe_category = category.strip().replace(" ", "_")

        category_folder = OUTPUT_DIR / safe_category
        category_folder.mkdir(parents=True, exist_ok=True)

        return category_folder