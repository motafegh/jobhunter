from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from jobhunter.evidence import EvidenceStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.sources import (
    DiscoveredJobLink,
    JobinjaAcquisitionError,
    JobinjaClient,
)
from jobhunter.storage import JobHunterStore


def _add_job(store: JobHunterStore, *, job_url: str) -> None:
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="abc1",
            company_slug="acme",
            canonical_url=job_url,
            observed_text="Python Developer",
        ),
        observed_at=datetime.now(UTC),
    )


def test_fetches_preserves_and_reuses_semantically_unchanged_job_detail(
    tmp_path: Path,
) -> None:
    job_url = "https://jobinja.ir/companies/acme/jobs/abc1/python-developer"
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        html = f"""
        <html><head>
        <meta name="csrf-token" content="dynamic-{request_count}">
        <script type="application/ld+json">
        {{"@type":"JobPosting","title":"Python Developer",
          "description":"<p>Build APIs</p>",
          "hiringOrganization":{{"name":"Acme"}},
          "employmentType":"FULL_TIME"}}
        </script></head><body><h1>Python Developer</h1></body></html>
        """.encode()
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html; charset=utf-8"},
            content=html,
        )

    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    _add_job(store, job_url=job_url)
    observation_store = JobDetailObservationStore(database_path)
    service = JobinjaDetailService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            transport=httpx.MockTransport(handler),
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        observation_store=observation_store,
    )

    first = service.fetch("abc1")
    second = service.fetch("abc1")
    detail = service.show("abc1")
    observations = observation_store.list_for_job("abc1")

    assert first.is_new_version is True
    assert second.is_new_version is False
    assert first.version_id == second.version_id
    assert first.observation_id != second.observation_id
    assert Path(first.evidence_path).is_file()
    assert Path(second.evidence_path).is_file()
    assert first.evidence_path != second.evidence_path
    assert store.count_job_detail_versions("abc1") == 1
    assert observation_store.count_for_job("abc1") == 2
    assert [observation.outcome for observation in observations] == [
        "unchanged",
        "new_version",
    ]
    assert all(
        observation.job_detail_version_id == first.version_id
        for observation in observations
    )
    assert detail.fields["title"] == "Python Developer"
    assert detail.fields["company"] == "Acme"
    assert detail.fields["description"] == "Build APIs"
    assert detail.parse_status == "parsed"


def test_failed_fetch_records_retryable_observation(tmp_path: Path) -> None:
    job_url = "https://jobinja.ir/companies/acme/jobs/abc1/python-developer"

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("network unavailable", request=request)

    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    _add_job(store, job_url=job_url)
    observation_store = JobDetailObservationStore(database_path)
    service = JobinjaDetailService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            transport=httpx.MockTransport(handler),
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        observation_store=observation_store,
    )

    with pytest.raises(JobinjaAcquisitionError):
        service.fetch("abc1")

    observations = observation_store.list_for_job("abc1")
    assert len(observations) == 1
    assert observations[0].outcome == "failed"
    assert observations[0].error_type == "JobinjaAcquisitionError"
    assert "network unavailable" in (observations[0].error_message or "")
    assert store.count_job_detail_versions("abc1") == 0
