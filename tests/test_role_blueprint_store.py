import sqlite3
from pathlib import Path

from jobhunter.role_blueprint_store import RoleBlueprintStore


def test_role_blueprint_store_initializes_idempotently(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = RoleBlueprintStore(database_path)

    store.initialize()
    store.initialize()

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert "job_role_blueprint_artifacts" in tables
    assert "job_role_blueprint_attempts" in tables
