from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from jobhunter.evidence import EvidenceStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.lifecycle import LifecycleStore
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


def _service(
    tmp_path: Path,
    handler,
    *,
    max_retries: int = 1,
) -> tuple[
    JobinjaDetailService,
    JobHunterStore,
    JobDetailObservationStore,
    LifecycleStore,
]:
    job_url = "https://jobinja.ir/companies/acme/jobs/abc1/python-developer"
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    _add_job(store, job_url=job_url)
    observation_store = JobDetailObservationStore(database_path)
    lifecycle_store = LifecycleStore(database_path)
    service = JobinjaDetailService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            max_retries=max_retries,
            transport=httpx.MockTransport(handler),
            sleep=lambda _seconds: None,
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        observation_store=observation_store,
        lifecycle_store=lifecycle_store,
    )
    return service, store, observation_store, lifecycle_store


def test_fetches_preserves_and_reuses_semantically_unchanged_job_detail(
    tmp_path: Path,
) -> None:
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

    service, store, observation_store, lifecycle_store = _service(tmp_path, handler)

    first = service.fetch("abc1")
    second = service.fetch("abc1")
    detail = service.show("abc1")
    observations = observation_store.list_for_job("abc1")
    lifecycle_events = lifecycle_store.list_for_job("abc1")

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
    assert [event.classification for event in lifecycle_events] == ["active", "active"]
    assert detail.fields["title"] == "Python Developer"
    assert detail.fields["company"] == "Acme"
    assert detail.fields["description"] == "Build APIs"
    assert detail.parse_status == "parsed"


def test_failed_network_fetch_records_observation_and_non_destructive_lifecycle(
    tmp_path: Path,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("network unavailable", request=request)

    service, store, observation_store, lifecycle_store = _service(
        tmp_path,
        handler,
        max_retries=0,
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        service.fetch("abc1")

    observations = observation_store.list_for_job("abc1")
    lifecycle_events = lifecycle_store.list_for_job("abc1")
    assert caught.value.classification == "network_error"
    assert len(observations) == 1
    assert observations[0].outcome == "failed"
    assert observations[0].error_type == "JobinjaAcquisitionError"
    assert "network unavailable" in (observations[0].error_message or "")
    assert lifecycle_events[0].classification == "network_error"
    assert lifecycle_events[0].retryable is True
    assert store.get_job("abc1").lifecycle_state == "active"
    assert store.count_job_detail_versions("abc1") == 0


@pytest.mark.parametrize(
    ("status_code", "expected_classification", "retryable"),
    [
        (429, "rate_limited", True),
        (502, "server_error", True),
        (503, "server_error", True),
        (504, "server_error", True),
    ],
)
def test_transient_http_failure_never_becomes_expired_or_removed(
    tmp_path: Path,
    status_code: int,
    expected_classification: str,
    retryable: bool,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code,
            request=request,
            headers={"content-type": "text/html"},
            text="temporary source failure",
        )

    service, store, observations, lifecycle = _service(
        tmp_path,
        handler,
        max_retries=0,
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        service.fetch("abc1")

    assert caught.value.classification == expected_classification
    assert caught.value.retryable is retryable
    assert store.get_job("abc1").lifecycle_state == "active"
    assert store.count_job_detail_versions("abc1") == 0
    assert observations.list_for_job("abc1")[0].outcome == "failed"
    event = lifecycle.list_for_job("abc1")[0]
    assert event.classification == expected_classification
    assert event.status_code == status_code


def test_challenge_page_never_creates_source_version_or_removal(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>Verify you are human CAPTCHA</body></html>",
        )

    service, store, observations, lifecycle = _service(tmp_path, handler)

    with pytest.raises(JobinjaAcquisitionError) as caught:
        service.fetch("abc1")

    assert caught.value.classification == "challenge"
    assert store.get_job("abc1").lifecycle_state == "active"
    assert store.count_job_detail_versions("abc1") == 0
    assert observations.list_for_job("abc1")[0].outcome == "failed"
    assert lifecycle.list_for_job("abc1")[0].classification == "challenge"


def test_explicit_expiry_preserves_raw_evidence_without_creating_semantic_version(
    tmp_path: Path,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>این موقعیت شغلی منقضی شده</body></html>",
        )

    service, store, observations, lifecycle = _service(tmp_path, handler)

    with pytest.raises(JobinjaAcquisitionError) as caught:
        service.fetch("abc1")

    assert caught.value.classification == "expired_explicit"
    assert store.get_job("abc1").lifecycle_state == "expired"
    assert store.count_job_detail_versions("abc1") == 0
    assert observations.list_for_job("abc1")[0].outcome == "failed"
    event = lifecycle.list_for_job("abc1")[0]
    assert event.classification == "expired_explicit"
    assert event.status_code == 200
    assert len(list((tmp_path / "evidence").rglob("*.html"))) == 1
    assert len(list((tmp_path / "evidence").rglob("*.json"))) == 1
