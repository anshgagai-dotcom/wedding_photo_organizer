from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from src.config.config import get_config


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging() -> None:
    """Configure global application logging once per process."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    config = get_config()
    log_file = config.logs_dir / "app.log"

    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
