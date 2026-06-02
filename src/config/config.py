from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Centralized application configuration loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="Wedding Photo Organizer", alias="APP_NAME")
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=7860, alias="APP_PORT")

    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-1.5-flash", alias="GEMINI_MODEL")
    google_client_id: str = Field(default="", alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", alias="GOOGLE_CLIENT_SECRET")
    email_address: str = Field(default="", alias="EMAIL_ADDRESS")
    email_password: str = Field(default="", alias="EMAIL_PASSWORD")

    batch_size: int = Field(default=32, alias="BATCH_SIZE")
    duplicate_hash_threshold: int = Field(default=6, alias="DUPLICATE_HASH_THRESHOLD")
    blur_threshold: float = Field(default=120.0, alias="BLUR_THRESHOLD")

    sqlite_db_name: str = Field(default="wedding_photos.db", alias="SQLITE_DB_NAME")
    sqlite_timeout_seconds: float = Field(default=30.0, alias="SQLITE_TIMEOUT_SECONDS")

    base_dir: Path = Path(__file__).resolve().parents[2]

    @property
    def input_photos_dir(self) -> Path:
        return self.base_dir / "input_photos"

    @property
    def organized_photos_dir(self) -> Path:
        return self.base_dir / "organized_photos"

    @property
    def metadata_dir(self) -> Path:
        return self.base_dir / "metadata"

    @property
    def logs_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def assets_dir(self) -> Path:
        return self.base_dir / "assets"

    @property
    def tests_dir(self) -> Path:
        return self.base_dir / "tests"

    @property
    def database_dir(self) -> Path:
        return self.base_dir / "database"

    @property
    def sqlite_db_path(self) -> Path:
        return self.database_dir / self.sqlite_db_name

    @property
    def host(self) -> str:
        return self.app_host

    @property
    def port(self) -> int:
        return self.app_port

    @property
    def input_dir(self) -> Path:
        return self.input_photos_dir

    @property
    def organized_dir(self) -> Path:
        return self.organized_photos_dir

    @property
    def metadata_file(self) -> Path:
        return self.metadata_dir / "photos_metadata.json"

    @property
    def required_external_keys(self) -> dict[str, str]:
        return {
            "GEMINI_API_KEY": self.gemini_api_key,
            "GOOGLE_CLIENT_ID": self.google_client_id,
            "GOOGLE_CLIENT_SECRET": self.google_client_secret,
            "EMAIL_ADDRESS": self.email_address,
            "EMAIL_PASSWORD": self.email_password,
        }

    def ensure_project_directories(self) -> None:
        for directory in [
            self.input_photos_dir,
            self.organized_photos_dir,
            self.metadata_dir,
            self.logs_dir,
            self.assets_dir,
            self.tests_dir,
            self.database_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    config = AppConfig()
    config.ensure_project_directories()
    return config
