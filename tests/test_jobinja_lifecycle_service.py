from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.evidence import EvidenceStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.lifecycle import LifecycleStore
from jobhunter.sources import DiscoveredJobLink, FetchedJobPage, JobinjaAcquisitionError
from jobhunter.storage import JobHunterStore


class _ExpiredClient:
    def fetch_job_page(self, job_url: str) -> FetchedJobPage:
        return FetchedJobPage(
            requested_url=job_url,
            final_url=job_url,
            status_code=200,
            headers={"content-type": "text/html"},
            content="<html>این فرصت شغلی منقضی شده</html>".encode(),
            text="<html>این فرصت شغلی منقضی شده</html>",
            classification="expired_explicit",
        )


def test_expired_page_keeps_raw_evidence_but_creates_no_semantic_version(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()
    url = "https://jobinja.ir/companies/acme/jobs/abc1/example"
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="abc1",
            company_slug="acme",
            canonical_url=url,
            observed_text="Example role",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    observations = JobDetailObservationStore(database_path)
    lifecycle = LifecycleStore(database_path)
    service = JobinjaDetailService(
        client=_ExpiredClient(),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        observation_store=observations,
        lifecycle_store=lifecycle,
    )

    with pytest.raises(JobinjaAcquisitionError) as captured:
        service.fetch("abc1")

    assert captured.value.classification == "expired_explicit"
    assert store.get_latest_job_detail("abc1") is None
    assert store.get_job("abc1").lifecycle_state == "expired"
    checks = observations.list_for_job("abc1")
    assert len(checks) == 1
    assert checks[0].outcome == "failed"
    events = lifecycle.list_for_job("abc1")
    assert events[0].classification == "expired_explicit"
    evidence_files = list((tmp_path / "evidence").rglob("*.html"))
    assert len(evidence_files) == 1
