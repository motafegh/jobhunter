import httpx
import pytest

from jobhunter.sources import (
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
