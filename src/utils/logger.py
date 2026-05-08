import logging
from pathlib import Path


def setup_logger(log_file="reports/app.log"):
    Path("reports").mkdir(exist_ok=True)

    logger = logging.getLogger("WeddingPhotoOrganizer")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

    