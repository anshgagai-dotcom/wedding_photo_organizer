from __future__ import annotations

import sqlite3

from src.config.config import get_config


def create_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection.

    Phase 1 scope:
    - provide resilient DB connectivity foundation
    - schema creation will be added in Phase 3 metadata engine
    """
    config = get_config()
    connection = sqlite3.connect(
        database=config.sqlite_db_path,
        timeout=config.sqlite_timeout_seconds,
    )
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
