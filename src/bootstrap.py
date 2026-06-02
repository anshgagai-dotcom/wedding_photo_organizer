from __future__ import annotations

from src.config.config import AppConfig, get_config
from src.logging.logging_setup import configure_logging, get_logger


def bootstrap_application() -> AppConfig:
    settings = get_config()
    settings.ensure_project_directories()
    configure_logging()
    get_logger(__name__).info("Application bootstrap complete")
    return settings
