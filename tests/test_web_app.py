import time
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.web.app import create_app


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path / "data",
        evidence_dir=tmp_path / "data/evidence",
        database_path=tmp_path / "data/jobhunter.sqlite3",
        translation_enabled=False,
    )


def test_web_app_renders_primary_local_pages(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        for path in ("/", "/jobs", "/searches", "/operations", "/system"):
            response = client.get(path)
            assert response.status_code == 200
            assert "JobHunter" in response.text
            assert response.headers["x-frame-options"] == "DENY"
            assert "frame-ancestors 'none'" in response.headers["content-security-policy"]


def test_web_app_serves_packaged_static_assets(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        css = client.get("/static/app.css")
        javascript = client.get("/static/app.js")
        icon = client.get("/static/icon.svg")
        manifest = client.get("/static/manifest.webmanifest")

    assert css.status_code == 200
    assert "--accent" in css.text
    assert javascript.status_code == 200
    assert "data-operation-id" in javascript.text
    assert icon.status_code == 200
    assert "<svg" in icon.text
    assert manifest.status_code == 200
    assert '"display": "standalone"' in manifest.text


def test_web_app_rejects_invalid_csrf_token(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        response = client.post(
            "/actions/audit",
            data={"csrf_token": "wrong"},
            follow_redirects=False,
        )

    assert response.status_code == 403


def test_web_app_runs_audit_through_operation_queue(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    token = app.state.csrf_token
    with TestClient(app) as client:
        response = client.post(
            "/actions/audit",
            data={"csrf_token": token},
            follow_redirects=False,
        )
        assert response.status_code == 303
        location = response.headers["location"]
        operation_id = location.rsplit("/", 1)[-1]

        payload = None
        for _ in range(100):
            payload = client.get(f"/api/operations/{operation_id}").json()
            if payload["status"] in {"completed", "failed"}:
                break
            time.sleep(0.01)

    assert payload is not None
    assert payload["status"] == "completed"
    assert "parser audit" in payload["summary"].casefold()


def test_web_app_jobs_filter_is_safe_on_empty_database(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        response = client.get(
            "/jobs",
            params={
                "q": "python",
                "detail": "missing",
                "translation": "missing",
                "lifecycle": "all",
            },
        )

    assert response.status_code == 200
    assert "0 matching jobs" in response.text


def test_web_app_renders_discovered_job_without_cli_error(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    store = JobHunterStore(settings.database_path)
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="tmW5",
            company_slug="example-company",
            canonical_url="https://jobinja.ir/companies/example-company/jobs/tmW5/example",
            observed_text="Example discovered job",
        ),
        observed_at=datetime.now(UTC),
    )

    app = create_app(settings)
    with TestClient(app) as client:
        response = client.get("/jobs/tmW5")

    assert response.status_code == 200
    assert "Details not acquired yet" in response.text
    assert "Fetch details" in response.text
    assert "jobhunter jobinja fetch tmW5" not in response.text
