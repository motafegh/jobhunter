from datetime import UTC, datetime, timedelta
from pathlib import Path

from jobhunter.lifecycle import LifecycleStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _add_job(database_path: Path) -> JobHunterStore:
    store = JobHunterStore(database_path)
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="abc1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
            observed_text="Example role",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    return store


def test_two_not_found_signals_are_required_before_removed(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store = _add_job(database_path)
    lifecycle = LifecycleStore(database_path)
    base = datetime(2026, 8, 1, tzinfo=UTC)

    lifecycle.record(
        "abc1",
        classification="not_found",
        status_code=404,
        checked_at=base,
    )
    assert source_store.get_job("abc1").lifecycle_state == "possibly_unavailable"

    lifecycle.record(
        "abc1",
        classification="gone",
        status_code=410,
        checked_at=base + timedelta(hours=1),
    )
    assert source_store.get_job("abc1").lifecycle_state == "removed"


def test_transient_failure_does_not_change_active_state_and_success_resets(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store = _add_job(database_path)
    lifecycle = LifecycleStore(database_path)
    base = datetime(2026, 8, 1, tzinfo=UTC)

    lifecycle.record(
        "abc1",
        classification="server_error",
        status_code=503,
        retryable=True,
        checked_at=base,
    )
    assert source_store.get_job("abc1").lifecycle_state == "active"
    assert lifecycle.consecutive_failures("abc1") == 1

    lifecycle.record(
        "abc1",
        classification="active",
        status_code=200,
        checked_at=base + timedelta(minutes=5),
    )
    assert source_store.get_job("abc1").lifecycle_state == "active"
    assert lifecycle.consecutive_failures("abc1") == 0


def test_explicit_expiry_is_strong_source_evidence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store = _add_job(database_path)
    lifecycle = LifecycleStore(database_path)

    lifecycle.record(
        "abc1",
        classification="expired_explicit",
        status_code=200,
        checked_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    assert source_store.get_job("abc1").lifecycle_state == "expired"
