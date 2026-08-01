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


def test_search_catalog_does_not_require_configuration(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "catalog", "--show-terms"]) == 0


def test_search_plan_expands_bilingual_profile_without_network(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert (
        main(
            [
                "jobinja",
                "plan",
                "--profile",
                "ai-security-python",
                "--search-limit",
                "8",
                "--request-budget",
                "4",
            ]
        )
        == 0
    )


def test_search_plan_rejects_unknown_pack(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "plan", "--pack", "unknown"]) == 2


def test_sync_rejects_combined_detail_limit_over_fifty(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert (
        main(
            [
                "jobinja",
                "sync",
                "--term",
                "Python",
                "--missing-limit",
                "30",
                "--refresh-limit",
                "21",
            ]
        )
        == 2
    )


def test_translation_status_is_offline_and_available_when_disabled(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["translations", "status"]) == 0


def test_translation_run_requires_explicit_external_opt_in(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["translations", "run", "--missing"]) == 2


def test_translation_run_reports_missing_google_credentials(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config = tmp_path / "jobhunter.toml"
    config.write_text(
        """
[jobhunter]
translation_enabled = true
translation_provider = "google-cloud"
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    assert main(["translations", "run", "--missing"]) == 2
