import httpx
import pytest

from jobhunter.sources import JobinjaAcquisitionError, JobinjaClient

_JOB_URL = "https://jobinja.ir/companies/acme/jobs/abc1/example"


def test_jobinja_retries_rate_limit_then_succeeds() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, request=request, text="slow down")
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>normal job</body></html>",
        )

    client = JobinjaClient(
        user_agent="test",
        timeout_seconds=5,
        max_retries=1,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )
    page = client.fetch_job_page(_JOB_URL)

    assert page.classification == "active"
    assert calls == 2


def test_jobinja_does_not_retry_access_denied() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(403, request=request, text="forbidden")

    client = JobinjaClient(
        user_agent="test",
        timeout_seconds=5,
        max_retries=3,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(JobinjaAcquisitionError) as captured:
        client.fetch_job_page(_JOB_URL)
    assert captured.value.classification == "access_denied"
    assert captured.value.retryable is False
    assert captured.value.status_code == 403
    assert calls == 1


def test_jobinja_classifies_challenge_without_retry() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body><div class='g-recaptcha'>verify</div></body></html>",
        )

    client = JobinjaClient(
        user_agent="test",
        timeout_seconds=5,
        max_retries=3,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(JobinjaAcquisitionError) as captured:
        client.fetch_job_page(_JOB_URL)
    assert captured.value.classification == "challenge"
    assert captured.value.retryable is False
    assert calls == 1


def test_jobinja_marks_explicit_expired_page_for_lifecycle_handling() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html; charset=utf-8"},
            text="<html><body>این فرصت شغلی منقضی شده</body></html>",
        )

    client = JobinjaClient(
        user_agent="test",
        timeout_seconds=5,
        transport=httpx.MockTransport(handler),
    )
    page = client.fetch_job_page(_JOB_URL)
    assert page.classification == "expired_explicit"
