from datetime import UTC, datetime
from pathlib import Path

from jobhunter.job_detail_observations import (
    JobDetailObservationStore,
    format_job_detail_observations,
)
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _add_job(
    store: JobHunterStore,
    *,
    source_job_id: str,
    fetched_at: datetime,
) -> int:
    result = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=source_job_id,
            company_slug="acme",
            canonical_url=(
                f"https://jobinja.ir/companies/acme/jobs/{source_job_id}/example"
            ),
            observed_text=f"Job {source_job_id}",
        ),
        observed_at=fetched_at,
    )
    store.record_job_detail(
        job_posting_id=result.job_posting_id,
        fetched_at=fetched_at,
        requested_url=(
            f"https://jobinja.ir/companies/acme/jobs/{source_job_id}/example"
        ),
        final_url=(
            f"https://jobinja.ir/companies/acme/jobs/{source_job_id}/example"
        ),
        status_code=200,
        content_sha256=f"raw-{source_job_id}",
        semantic_sha256=f"semantic-{source_job_id}",
        evidence_path=Path(f"{source_job_id}.html"),
        metadata_path=Path(f"{source_job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": f"Job {source_job_id}",
            "description": "A sufficiently long job description for testing.",
        },
    )
    return result.job_posting_id


def test_refresh_due_uses_observations_and_legacy_version_fallback(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    old_job_id = _add_job(
        store,
        source_job_id="old1",
        fetched_at=datetime(2026, 7, 29, 12, 0, tzinfo=UTC),
    )
    _add_job(
        store,
        source_job_id="new2",
        fetched_at=datetime(2026, 8, 1, 6, 0, tzinfo=UTC),
    )

    observations = JobDetailObservationStore(database_path)
    observations.record_success(
        job_posting_id=old_job_id,
        checked_at=datetime(2026, 7, 31, 0, 0, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/acme/jobs/old1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/old1/example",
        status_code=200,
        content_sha256="raw-old-check",
        semantic_sha256="semantic-old1",
        evidence_path=Path("old-check.html"),
        metadata_path=Path("old-check.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        job_detail_version_id=1,
        is_new_version=False,
    )

    due = observations.refresh_due_job_ids(
        as_of=datetime(2026, 8, 1, 12, 0, tzinfo=UTC),
        older_than_hours=24,
        limit=10,
    )

    assert due == ("old1",)


def test_formats_success_and_failure_check_history(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    job_posting_id = _add_job(
        store,
        source_job_id="abc1",
        fetched_at=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
    )
    observations = JobDetailObservationStore(database_path)
    observations.record_success(
        job_posting_id=job_posting_id,
        checked_at=datetime(2026, 8, 1, 1, 0, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
        status_code=200,
        content_sha256="raw-success",
        semantic_sha256="semantic-abc1",
        evidence_path=Path("success.html"),
        metadata_path=Path("success.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        job_detail_version_id=1,
        is_new_version=False,
    )
    observations.record_failure(
        job_posting_id=job_posting_id,
        checked_at=datetime(2026, 8, 1, 2, 0, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
        error=RuntimeError("temporary failure"),
    )

    history = observations.list_for_job("abc1")
    rendered = format_job_detail_observations(history, source_job_id="abc1")

    assert [entry.outcome for entry in history] == ["failed", "unchanged"]
    assert "Observations shown: 2" in rendered
    assert "temporary failure" in rendered
    assert "raw evidence: success.html" in rendered
