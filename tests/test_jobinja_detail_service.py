from datetime import UTC, datetime
from pathlib import Path

import httpx

from jobhunter.evidence import EvidenceStore
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.sources import DiscoveredJobLink, JobinjaClient
from jobhunter.storage import JobHunterStore


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

    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
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
    service = JobinjaDetailService(
        client=JobinjaClient(
            user_agent="JobHunter-Test/1",
            timeout_seconds=5,
            transport=httpx.MockTransport(handler),
        ),
        evidence_store=EvidenceStore(tmp_path / "evidence"),
        store=store,
    )

    first = service.fetch("abc1")
    second = service.fetch("abc1")
    detail = service.show("abc1")

    assert first.is_new_version is True
    assert second.is_new_version is False
    assert first.version_id == second.version_id
    assert Path(first.evidence_path).is_file()
    assert Path(second.evidence_path).is_file()
    assert first.evidence_path != second.evidence_path
    assert store.count_job_detail_versions("abc1") == 1
    assert detail.fields["title"] == "Python Developer"
    assert detail.fields["company"] == "Acme"
    assert detail.fields["description"] == "Build APIs"
    assert detail.parse_status == "parsed"
