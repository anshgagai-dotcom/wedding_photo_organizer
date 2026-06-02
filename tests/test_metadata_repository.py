from pathlib import Path

from src.config.config import AppConfig
from src.database.connection import create_connection
from src.database.repository import MetadataRepository
from src.metadata.models import PhotoMetadata


def test_repository_upsert_and_fetch(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    config = AppConfig(base_dir=tmp_path)
    config.ensure_project_directories()
    monkeypatch.setenv("SQLITE_DB_NAME", "test.db")

    def _fake_get_config() -> AppConfig:
        return config

    # Late import monkeypatch target via module attributes.
    import src.database.connection as connection_module
    import src.database.repository as repository_module

    monkeypatch.setattr(connection_module, "get_config", _fake_get_config)
    monkeypatch.setattr(repository_module, "create_connection", create_connection)

    repo = MetadataRepository()
    sample = PhotoMetadata(
        photo_name="demo.jpg",
        path=str(Path(tmp_path / "input_photos" / "demo.jpg")),
        filename="demo.jpg",
        category="Bride",
        photo_category="Bride",
        scene_description="Bride portrait",
        tags=["bride"],
    )
    repo.upsert_many([sample])
    records = repo.fetch_all()
    assert len(records) == 1
    assert records[0].category == "Bride"
