from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx

from jobhunter.evidence import EvidenceStore
from jobhunter.jobinja_discovery import (
    DiscoverySearch,
    JobinjaDiscoveryService,
    format_discovery_summary,
)
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore


def _clock():
    counter = 0

    def clock() -> datetime:
        nonlocal counter
        value = datetime(2026, 7, 31, 12, 0, tzinfo=UTC) + timedelta(
            seconds=counter
        )
        counter += 1
        return value

    return clock


def _service(
    tmp_path: Path,
    handler,
    *,
    sleep=lambda _seconds: None,
    request_delay_seconds: float = 0,
    request_budget: int = 40,
) -> tuple[JobinjaDiscoveryService, JobHunterStore]:
    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
    service = JobinjaDiscoveryService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            transport=httpx.MockTransport(handler),
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        request_delay_seconds=request_delay_seconds,
        request_budget=request_budget,
        sleep=sleep,
        clock=_clock(),
    )
    return service, store


def _html(*jobs: tuple[str, str]) -> str:
    links = "".join(
        f'<a href="/companies/acme/jobs/{job_id}/example">{title}</a>'
        for job_id, title in jobs
    )
    return f"<html><body>{links}</body></html>"


def test_discovery_preserves_evidence_and_is_repeat_safe(tmp_path: Path) -> None:
    html = _html(
        ("abc1", "Python Developer"),
        ("xyz2", "مهندس امنیت"),
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html; charset=utf-8"},
            text=html,
        )

    service, store = _service(tmp_path, handler)
    searches = [
        DiscoverySearch(
            name="AI roles",
            url="https://jobinja.ir/jobs?q=ai",
            max_pages=1,
        )
    ]

    first = service.run(searches)
    second = service.run(searches)

    assert first.unique_jobs == 2
    assert first.new_jobs == 2
    assert first.known_jobs == 0
    assert first.search_summaries[0].stop_reason == "page_limit_reached"
    assert first.requests_attempted == 1
    assert first.request_budget == 40
    assert second.unique_jobs == 2
    assert second.new_jobs == 0
    assert second.known_jobs == 2
    assert store.count_job_postings() == 2
    assert len(list((tmp_path / "evidence").rglob("*.html"))) == 2
    assert len(list((tmp_path / "evidence").rglob("*.json"))) == 2


def test_stops_when_a_later_page_repeats_the_same_job_set(tmp_path: Path) -> None:
    requested_pages: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        requested_pages.append(page)
        if page == 1:
            html = _html(("abc1", "Python Developer"), ("xyz2", "Security"))
        elif page == 2:
            html = _html(("xyz2", "Security updated"), ("abc1", "Python"))
        else:
            raise AssertionError("page 3 must not be requested")
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text=html,
        )

    service, store = _service(tmp_path, handler)
    summary = service.run(
        [
            DiscoverySearch(
                name="Repeated search",
                url="https://jobinja.ir/jobs?q=ai",
                max_pages=3,
            )
        ]
    )

    assert requested_pages == [1, 2]
    assert summary.pages_fetched == 2
    assert summary.unique_jobs == 2
    assert summary.search_summaries[0].unique_jobs == 2
    assert summary.search_summaries[0].stop_reason == "repeated_result_set"
    assert store.count_job_postings() == 2
    assert "stop=repeated_result_set" in format_discovery_summary(summary)


def test_stops_on_an_empty_page(tmp_path: Path) -> None:
    requested_pages: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        requested_pages.append(page)
        if page == 1:
            html = _html(("abc1", "Python Developer"))
        elif page == 2:
            html = "<html><body>No jobs</body></html>"
        else:
            raise AssertionError("page 3 must not be requested")
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text=html,
        )

    service, _store = _service(tmp_path, handler)
    summary = service.run(
        [
            DiscoverySearch(
                name="Finite search",
                url="https://jobinja.ir/jobs?q=ai",
                max_pages=3,
            )
        ]
    )

    assert requested_pages == [1, 2]
    assert summary.pages_fetched == 2
    assert summary.search_summaries[0].stop_reason == "empty_page"


def test_reports_cross_search_overlap_without_inflating_unique_jobs(
    tmp_path: Path,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        query = request.url.params.get("q")
        html = (
            _html(("abc1", "Python Developer"))
            if query == "python"
            else _html(
                ("abc1", "Python Developer"),
                ("xyz2", "Security Engineer"),
            )
        )
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text=html,
        )

    service, store = _service(tmp_path, handler)
    summary = service.run(
        [
            DiscoverySearch(
                name="Python roles",
                url="https://jobinja.ir/jobs?q=python",
            ),
            DiscoverySearch(
                name="AI roles",
                url="https://jobinja.ir/jobs?q=ai",
            ),
        ]
    )

    assert summary.unique_jobs == 2
    assert summary.new_jobs == 2
    assert summary.cross_search_overlaps == 1
    assert summary.search_summaries[0].cross_search_overlaps == 0
    assert summary.search_summaries[1].cross_search_overlaps == 1
    assert store.count_job_postings() == 2


def test_one_search_failure_does_not_discard_other_searches(tmp_path: Path) -> None:
    delays: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("q") == "broken":
            return httpx.Response(
                503,
                request=request,
                headers={"content-type": "text/html"},
                text="unavailable",
            )
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text=_html(("abc1", "Python Developer")),
        )

    service, store = _service(
        tmp_path,
        handler,
        sleep=delays.append,
        request_delay_seconds=0.25,
    )
    summary = service.run(
        [
            DiscoverySearch(
                name="Broken search",
                url="https://jobinja.ir/jobs?q=broken",
            ),
            DiscoverySearch(
                name="Working search",
                url="https://jobinja.ir/jobs?q=working",
            ),
        ]
    )

    assert summary.succeeded is False
    assert len(summary.failures) == 1
    assert summary.unique_jobs == 1
    assert summary.search_summaries[0].stop_reason == "page_failed"
    assert summary.search_summaries[1].stop_reason == "page_limit_reached"
    assert delays == [0.25]
    assert store.count_job_postings() == 1


def test_global_request_budget_skips_remaining_searches(tmp_path: Path) -> None:
    requested_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_urls.append(str(request.url))
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html"},
            text=_html((f"job{len(requested_urls)}", "Role")),
        )

    service, _store = _service(tmp_path, handler, request_budget=2)
    summary = service.run(
        [
            DiscoverySearch(name="one", url="https://jobinja.ir/jobs?q=one"),
            DiscoverySearch(name="two", url="https://jobinja.ir/jobs?q=two"),
            DiscoverySearch(name="three", url="https://jobinja.ir/jobs?q=three"),
        ]
    )

    assert len(requested_urls) == 2
    assert summary.requests_attempted == 2
    assert summary.pages_fetched == 2
    assert summary.search_summaries[2].stop_reason == "request_budget_reached"
    assert "Page requests attempted: 2/2" in format_discovery_summary(summary)
