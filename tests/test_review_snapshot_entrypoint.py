from pathlib import Path
from types import SimpleNamespace

import jobhunter.entrypoint as entrypoint


def test_jobs_snapshot_routes_to_review_export(monkeypatch, capsys, tmp_path: Path) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    calls: list[tuple[Path, str, Path]] = []

    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)

    def write(database_path: Path, job_id: str, *, output_dir: Path) -> Path:
        calls.append((database_path, job_id, output_dir))
        return output_dir / f"{job_id}.json"

    monkeypatch.setattr(entrypoint, "write_review_snapshot", write)

    exit_code = entrypoint.main(["jobs", "snapshot", "tG9K"])

    assert exit_code == 0
    assert calls == [
        (
            settings.database_path,
            "tG9K",
            Path("review-snapshots/jobs"),
        )
    ]
    assert "review-snapshots/jobs/tG9K.json" in capsys.readouterr().out


def test_global_config_can_precede_snapshot_command(monkeypatch, tmp_path: Path) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    seen_paths: list[Path | None] = []

    def load(path):
        seen_paths.append(path)
        return settings

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(
        entrypoint,
        "write_review_snapshot",
        lambda _database, job_id, *, output_dir: output_dir / f"{job_id}.json",
    )

    exit_code = entrypoint.main(
        ["--config", "custom.toml", "jobs", "snapshot", "abc1"]
    )

    assert exit_code == 0
    assert seen_paths == [Path("custom.toml")]


def test_global_help_surfaces_snapshot_command(capsys) -> None:
    assert entrypoint.main(["--help"]) == 0
    assert "jobs snapshot <id>" in capsys.readouterr().out
