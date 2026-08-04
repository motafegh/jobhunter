from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.web.launcher import build_runtime_app


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
    )


def test_runtime_app_registers_capability_review_routes(tmp_path: Path) -> None:
    app = build_runtime_app(_settings(tmp_path))
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in (getattr(route, "methods", None) or set())
    }

    path = "/jobs/{source_job_id}/capability-intelligence"
    assert (path, "GET") in route_methods
    assert (path, "POST") in route_methods


def test_capability_review_page_renders_before_analysis(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    store = JobHunterStore(settings.database_path)
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="webcap1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/webcap1/example",
            observed_text="Infrastructure Security Specialist",
        ),
        observed_at=datetime(2026, 8, 4, tzinfo=UTC),
    )

    response = TestClient(build_runtime_app(settings)).get(
        "/jobs/webcap1/capability-intelligence"
    )

    assert response.status_code == 200
    assert "Capability Intelligence" in response.text
    assert "English analysis required" in response.text
