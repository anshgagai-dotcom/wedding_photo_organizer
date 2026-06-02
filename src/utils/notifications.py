from __future__ import annotations

from src.config.config import AppConfig
from src.logging.logging_setup import get_logger


LOGGER = get_logger(__name__)


class NotificationService:
    """
    Safe notification abstraction.

    Current implementation is a non-crashing stub that logs intended notifications.
    It can be replaced by real Gmail/API integrations later without changing callers.
    """

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.enabled = bool(
            config.google_client_id.strip()
            and config.google_client_secret.strip()
            and config.email_address.strip()
            and config.email_password.strip()
        )

    def send_pipeline_summary(self, subject: str, body: str) -> None:
        if not self.enabled:
            LOGGER.info("Notification stub mode active. Subject=%s Body=%s", subject, body)
            return
        # Safe stub even when credentials are present; no outbound network calls in this stage.
        LOGGER.info("Notification queued (stub). Subject=%s", subject)
