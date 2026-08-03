from datetime import UTC, datetime
from pathlib import Path

from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.lifecycle import LifecycleStore
from jobhunter.source_health import SourceHealthReader, format_source_health
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _prepare_job(database_path: Path) -> tuple[int, int]:
    store = JobHunterStore(database_path)
    store.initialize()
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="health1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/health1/example",
            observed_text="Health Test",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    detail = store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        status_code=200,
        content_sha256="raw-health1",
        semantic_sha256="semantic-health1",
        evidence_path=Path("health1.html"),
        metadata_path=Path("health1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Health Test",
            "description": "A sufficiently long source description for health testing.",
        },
    )
    return posting.job_posting_id, detail.version_id


def test_source_health_summarizes_last_success_and_consecutive_failures(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    posting_id, version_id = _prepare_job(database_path)
    observations = JobDetailObservationStore(database_path)
    lifecycle = LifecycleStore(database_path)

    success_at = datetime(2026, 8, 1, 1, 0, tzinfo=UTC)
    observations.record_success(
        job_posting_id=posting_id,
        checked_at=success_at,
        requested_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        status_code=200,
        content_sha256="raw-health-success",
        semantic_sha256="semantic-health1",
        evidence_path=Path("success.html"),
        metadata_path=Path("success.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        job_detail_version_id=version_id,
        is_new_version=False,
    )
    lifecycle.record("health1", classification="active", checked_at=success_at)

    first_failure_at = datetime(2026, 8, 2, 1, 0, tzinfo=UTC)
    observations.record_failure(
        job_posting_id=posting_id,
        checked_at=first_failure_at,
        requested_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        error=RuntimeError("temporary server failure"),
    )
    lifecycle.record(
        "health1",
        classification="server_error",
        status_code=503,
        retryable=True,
        checked_at=first_failure_at,
    )

    second_failure_at = datetime(2026, 8, 3, 1, 0, tzinfo=UTC)
    observations.record_failure(
        job_posting_id=posting_id,
        checked_at=second_failure_at,
        requested_url="https://jobinja.ir/companies/acme/jobs/health1/example",
        error=RuntimeError("not found check"),
    )
    lifecycle.record(
        "health1",
        classification="not_found",
        status_code=404,
        checked_at=second_failure_at,
    )

    summary = SourceHealthReader(database_path).get("health1")

    assert summary.lifecycle_state == "possibly_unavailable"
    assert summary.total_checks == 3
    assert summary.last_checked_at == second_failure_at.isoformat()
    assert summary.last_successful_check_at == success_at.isoformat()
    assert summary.consecutive_operational_failures == 2
    assert summary.latest_failure_type == "RuntimeError"
    assert summary.latest_failure_message == "not found check"
    assert summary.latest_lifecycle_classification == "not_found"
    assert summary.consecutive_lifecycle_failures == 2

    rendered = format_source_health(summary)
    assert "Last successful check:" in rendered
    assert "Consecutive operational failures: 2" in rendered
    assert "possibly_unavailable" in rendered


def test_source_health_supports_discovered_job_without_checks(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="fresh1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/fresh1/example",
            observed_text="Fresh Job",
        ),
        observed_at=datetime(2026, 8, 3, tzinfo=UTC),
    )

    summary = SourceHealthReader(database_path).get("fresh1")

    assert summary.lifecycle_state == "active"
    assert summary.total_checks == 0
    assert summary.last_successful_check_at is None
    assert summary.consecutive_operational_failures == 0
    assert summary.latest_lifecycle_classification is None
