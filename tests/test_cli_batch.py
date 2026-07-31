from pathlib import Path

from jobhunter.cli import main


def test_fetch_requires_ids_or_missing_selector(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch"]) == 2


def test_fetch_rejects_ids_with_missing_selector(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "abc1", "--missing"]) == 2


def test_fetch_rejects_limit_without_missing_selector(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "abc1", "--limit", "2"]) == 2


def test_jobs_list_handles_empty_database(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobs", "list"]) == 0
