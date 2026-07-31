from datetime import UTC, datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def test_job_upsert_is_repeat_safe(tmp_path: Path) -> None:
    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
    store.initialize()
    observed_at = datetime(2026, 7, 31, 12, 0, tzinfo=UTC)
    job = DiscoveredJobLink(
        source_job_id="tpLF",
        company_slug="aseh-tejarat-asia",
        canonical_url=(
            "https://jobinja.ir/companies/aseh-tejarat-asia/jobs/tpLF/example-title"
        ),
        observed_text="AI Developer",
    )

    first = store.upsert_job(job=job, observed_at=observed_at)
    second = store.upsert_job(job=job, observed_at=observed_at)

    assert first.is_new is True
    assert second.is_new is False
    assert first.job_posting_id == second.job_posting_id
    assert store.count_job_postings() == 1
