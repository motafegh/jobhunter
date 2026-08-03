import httpx
import pytest

from jobhunter.sources import (
    JobinjaAcquisitionError,
    JobinjaClient,
    JobinjaUrlError,
    canonicalize_job_url,
    canonicalize_search_url,
    extract_job_links,
    with_search_page,
)


def test_canonicalizes_search_url_and_removes_page() -> None:
    url = (
        "https://www.jobinja.ir/jobs/?filters%5Bkeywords%5D%5B0%5D=python"
        "&page=8#results"
    )

    assert canonicalize_search_url(url) == (
        "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=python"
    )


def test_adds_bounded_page_without_losing_filters() -> None:
    search_url = (
        "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=python"
        "&filters%5Blocations%5D%5B%5D=tehran"
    )

    page_url = with_search_page(search_url, 3)

    assert "filters%5Bkeywords%5D%5B0%5D=python" in page_url
    assert "filters%5Blocations%5D%5B%5D=tehran" in page_url
    assert page_url.endswith("page=3")


def test_canonicalizes_job_url_and_removes_tracking() -> None:
    result = canonicalize_job_url(
        "/companies/aseh-tejarat-asia/jobs/tpLF/example-title?_ref=28"
    )

    assert result.source_job_id == "tpLF"
    assert result.company_slug == "aseh-tejarat-asia"
    assert result.canonical_url == (
        "https://jobinja.ir/companies/aseh-tejarat-asia/jobs/tpLF/example-title"
    )


def test_rejects_non_jobinja_url() -> None:
    with pytest.raises(JobinjaUrlError, match="host"):
        canonicalize_search_url("https://example.com/jobs?q=python")


def test_extracts_and_deduplicates_job_links() -> None:
    html = """
    <main>
      <a href="/companies/acme/jobs/abc1/python-developer?_ref=1">
        Python Developer
      </a>
      <a href="https://jobinja.ir/companies/acme/jobs/abc1/python-developer?_ref=2">
        Duplicate result
      </a>
      <a href="/companies/example/jobs/xyz2/security-engineer">
        مهندس امنیت
      </a>
      <a href="/companies/acme">Company page</a>
    </main>
    """

    links = extract_job_links(html, base_url="https://jobinja.ir/jobs?page=1")

    assert [link.source_job_id for link in links] == ["abc1", "xyz2"]
    assert links[0].observed_text == "Python Developer"
    assert links[1].observed_text == "مهندس امنیت"


def test_recovers_title_from_later_duplicate_link() -> None:
    html = """
    <article>
      <a href="/companies/acme/jobs/abc1/python-developer">
        <img src="logo.png" alt="">
      </a>
      <a href="/companies/acme/jobs/abc1/python-developer">
        توسعه دهنده پایتون
      </a>
    </article>
    """

    links = extract_job_links(html, base_url="https://jobinja.ir/jobs")

    assert len(links) == 1
    assert links[0].source_job_id == "abc1"
    assert links[0].observed_text == "توسعه دهنده پایتون"


def test_fetches_public_search_page_with_expected_headers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "jobinja.ir"
        assert request.url.params["page"] == "2"
        assert request.headers["user-agent"] == "JobHunter-Test/1"
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html; charset=utf-8"},
            text="<html><body>ok</body></html>",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        transport=httpx.MockTransport(handler),
    )

    page = client.fetch_search_page("https://jobinja.ir/jobs?q=python", 2)

    assert page.status_code == 200
    assert page.requested_url.endswith("q=python&page=2")
    assert page.text == "<html><body>ok</body></html>"


def test_retries_transient_server_error_then_returns_success() -> None:
    attempts = 0
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(
                503,
                request=request,
                headers={"content-type": "text/html"},
                text="temporarily unavailable",
            )
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>recovered</body></html>",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=1,
        transport=httpx.MockTransport(handler),
        sleep=sleeps.append,
    )

    page = client.fetch_search_page("https://jobinja.ir/jobs?q=python", 1)

    assert attempts == 2
    assert sleeps == [0.5]
    assert page.status_code == 200


def test_exhausted_server_error_is_retryable_but_not_expiry() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(
            502,
            request=request,
            headers={"content-type": "text/html"},
            text="bad gateway",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=1,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_search_page("https://jobinja.ir/jobs?q=python", 1)

    assert attempts == 2
    assert caught.value.classification == "server_error"
    assert caught.value.status_code == 502
    assert caught.value.retryable is True
    assert caught.value.classification not in {"expired_explicit", "not_found", "gone"}


def test_rate_limit_is_classified_retryable_without_becoming_empty_result() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            request=request,
            headers={"content-type": "text/html"},
            text="slow down",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_search_page("https://jobinja.ir/jobs?q=python", 1)

    assert caught.value.classification == "rate_limited"
    assert caught.value.status_code == 429
    assert caught.value.retryable is True


def test_network_failure_retries_then_remains_network_failure() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        raise httpx.ConnectError("resolver unavailable", request=request)

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=1,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_search_page("https://jobinja.ir/jobs?q=python", 1)

    assert attempts == 2
    assert caught.value.classification == "network_error"
    assert caught.value.retryable is True
    assert caught.value.status_code is None


def test_challenge_page_is_not_retried_or_treated_as_job_content() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>Verify you are human CAPTCHA</body></html>",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=3,
        transport=httpx.MockTransport(handler),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_job_page(
            "https://jobinja.ir/companies/acme/jobs/abc1/example"
        )

    assert attempts == 1
    assert caught.value.classification == "challenge"
    assert caught.value.retryable is False


def test_unexpected_non_html_response_is_explicit_failure_not_empty_result() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "application/json"},
            json={"jobs": []},
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_search_page("https://jobinja.ir/jobs?q=python", 1)

    assert caught.value.classification == "unexpected_page"
    assert caught.value.status_code == 200
    assert caught.value.retryable is False
    assert "content type" in str(caught.value).casefold()


def test_explicit_expiry_page_remains_successful_evidence_with_expiry_classification() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>این موقعیت شغلی منقضی شده</body></html>",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        transport=httpx.MockTransport(handler),
    )

    page = client.fetch_job_page(
        "https://jobinja.ir/companies/acme/jobs/abc1/example"
    )

    assert page.status_code == 200
    assert page.classification == "expired_explicit"


def test_login_redirect_is_auth_required_not_missing_job() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path != "/login":
            return httpx.Response(
                302,
                request=request,
                headers={"location": "https://jobinja.ir/login"},
            )
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text="<html><body>Login</body></html>",
        )

    client = JobinjaClient(
        user_agent="JobHunter-Test/1",
        timeout_seconds=5,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(JobinjaAcquisitionError) as caught:
        client.fetch_job_page(
            "https://jobinja.ir/companies/acme/jobs/abc1/example"
        )

    assert caught.value.classification == "auth_required"
    assert caught.value.status_code == 200
    assert caught.value.retryable is False
