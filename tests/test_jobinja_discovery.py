from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from jobhunter.evidence import EvidenceStore
from jobhunter.jobinja_discovery import DiscoverySearch, JobinjaDiscoveryService
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore


def test_discovery_preserves_evidence_and_is_repeat_safe(tmp_path: Path) -> None:
    html = """
    <html><body>
      <a href="/companies/acme/jobs/abc1/python-developer?_ref=1">
        Python Developer
      </a>
      <a href="/companies/example/jobs/xyz2/security-engineer">
        مهندس امنیت
      </a>
    </body></html>
    """

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            request=request,
            headers={"content-type": "text/html; charset=utf-8"},
            text=html,
        )

    counter = 0

    def clock() -> datetime:
        nonlocal counter
        value = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc) + timedelta(
            seconds=counter
        )
        counter += 1
        return value

    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
    service = JobinjaDiscoveryService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            transport=httpx.MockTransport(handler),
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
        request_delay_seconds=0,
        sleep=lambda _seconds: None,
        clock=clock,
    )
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
    assert second.unique_jobs == 2
    assert second.new_jobs == 0
    assert second.known_jobs == 2
    assert store.count_job_postings() == 2
    assert len(list((tmp_path / "evidence").rglob("*.html"))) == 2
    assert len(list((tmp_path / "evidence").rglob("*.json"))) == 2
