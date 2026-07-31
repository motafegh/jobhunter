from pathlib import Path

from jobhunter.cli import main


def test_fetch_requires_one_selection_mode(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch"]) == 2


def test_fetch_rejects_ids_with_missing_selector(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "abc1", "--missing"]) == 2


def test_fetch_rejects_ids_with_refresh_due_selector(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "abc1", "--refresh-due"]) == 2


def test_fetch_rejects_multiple_automatic_selectors(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "--missing", "--refresh-due"]) == 2


def test_fetch_rejects_limit_with_explicit_ids(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "abc1", "--limit", "2"]) == 2


def test_fetch_rejects_age_without_refresh_due(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "--missing", "--older-than-hours", "24"]) == 2


def test_refresh_due_handles_empty_database(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "--refresh-due"]) == 0


def test_jobs_list_handles_empty_database(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobs", "list"]) == 0


def test_jobs_checks_handles_empty_history(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobs", "checks", "abc1"]) == 0
