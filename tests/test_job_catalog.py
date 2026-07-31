from datetime import UTC, datetime
from pathlib import Path

from jobhunter.job_catalog import JobCatalog, format_job_list
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _add_job(
    store: JobHunterStore,
    *,
    source_job_id: str,
    title: str,
) -> int:
    result = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=source_job_id,
            company_slug="acme",
            canonical_url=(
                f"https://jobinja.ir/companies/acme/jobs/{source_job_id}/example"
            ),
            observed_text=title,
        ),
        observed_at=datetime(2026, 7, 31, 12, 0, tzinfo=UTC),
    )
    return result.job_posting_id


def test_lists_available_and_missing_jobs(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    acquired_id = _add_job(store, source_job_id="abc1", title="Python Developer")
    _add_job(store, source_job_id="xyz2", title="Security Engineer")
    store.record_job_detail(
        job_posting_id=acquired_id,
        fetched_at=datetime(2026, 7, 31, 12, 5, tzinfo=UTC),
        requested_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/abc1/example",
        status_code=200,
        content_sha256="raw-hash",
        semantic_sha256="semantic-hash",
        evidence_path=Path("page.html"),
        metadata_path=Path("page.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={"title": "Python Developer", "description": "Build APIs"},
    )

    catalog = JobCatalog(database_path)
    all_jobs = catalog.list_jobs()
    available = catalog.list_jobs(detail_filter="available")
    missing = catalog.list_jobs(detail_filter="missing")

    assert [job.source_job_id for job in all_jobs] == ["abc1", "xyz2"]
    assert [job.source_job_id for job in available] == ["abc1"]
    assert available[0].detail_status == "parsed"
    assert available[0].semantic_versions == 1
    assert [job.source_job_id for job in missing] == ["xyz2"]
    assert catalog.missing_job_ids(limit=5) == ("xyz2",)
    assert "abc1 [parsed, v1] Python Developer" in format_job_list(all_jobs)
    assert "xyz2 [missing] Security Engineer" in format_job_list(all_jobs)
