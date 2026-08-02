import time
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.web.app import create_app
from jobhunter.web.operations import WebOperationManager


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
        for path in ("/", "/jobs", "/market", "/searches", "/operations", "/system"):
            response = client.get(path)
            assert response.status_code == 200
            assert "JobHunter" in response.text
            assert response.headers["x-frame-options"] == "DENY"
            assert "frame-ancestors 'none'" in response.headers["content-security-policy"]


def test_web_app_serves_packaged_static_assets(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        css = client.get("/static/app.css")
        workflow_css = client.get("/static/workflow.css")
        javascript = client.get("/static/app.js")
        icon = client.get("/static/icon.svg")
        manifest = client.get("/static/manifest.webmanifest")

    assert css.status_code == 200
    assert "--accent" in css.text
    assert "analysis-columns" in css.text
    assert workflow_css.status_code == 200
    assert "workflow-actions" in workflow_css.text
    assert javascript.status_code == 200
    assert "data-operation-id" in javascript.text
    assert "data-sync-preset" in javascript.text
    assert "window.location.assign" in javascript.text
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
        assert "return_to=%2F" in response.headers["location"]
        operation_id = response.headers["location"].split("?", 1)[0].rsplit("/", 1)[-1]

        payload = None
        for _ in range(100):
            payload = client.get(f"/api/operations/{operation_id}").json()
            if payload["status"] in {"completed", "failed"}:
                break
            time.sleep(0.01)

    assert payload is not None
    assert payload["status"] == "completed"
    assert "parser audit" in payload["summary"].casefold()


def test_operation_page_supports_safe_automatic_return(tmp_path: Path) -> None:
    operations = WebOperationManager()
    operation = operations.start("No-op", lambda: "done")
    app = create_app(_settings(tmp_path), operations=operations)

    with TestClient(app) as client:
        response = client.get(
            f"/operations/{operation.id}",
            params={"return_to": "/jobs/tmW5", "auto_return": "1"},
        )
        unsafe = client.get(
            f"/operations/{operation.id}",
            params={"return_to": "https://example.com", "auto_return": "1"},
        )

    assert response.status_code == 200
    assert 'data-return-url="/jobs/tmW5"' in response.text
    assert 'data-auto-return="true"' in response.text
    assert "Back to job" in response.text
    assert 'data-return-url=""' in unsafe.text
    assert 'data-auto-return="false"' in unsafe.text


def test_web_app_empty_priority_detail_backlog_needs_no_network(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    token = app.state.csrf_token
    with TestClient(app) as client:
        response = client.post(
            "/actions/fetch-missing",
            data={"csrf_token": token, "limit": "10"},
            follow_redirects=False,
        )
        assert response.status_code == 303
        operation_id = response.headers["location"].split("?", 1)[0].rsplit("/", 1)[-1]

        payload = None
        for _ in range(100):
            payload = client.get(f"/api/operations/{operation_id}").json()
            if payload["status"] in {"completed", "failed"}:
                break
            time.sleep(0.01)

    assert payload is not None
    assert payload["status"] == "completed"
    assert "No eligible discovered jobs need a detail-page fetch" in payload["summary"]


def test_web_app_jobs_filter_is_safe_on_empty_database(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        response = client.get(
            "/jobs",
            params={
                "q": "python",
                "detail": "missing",
                "translation": "missing",
                "analysis": "missing",
                "triage": "all",
                "lifecycle": "all",
            },
        )

    assert response.status_code == 200
    assert "0 matching jobs" in response.text


def test_web_app_explains_sync_controls_quick_add_and_pipeline(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        overview = client.get("/")
        jobs = client.get("/jobs")
        market = client.get("/market")

    assert "Search terms to try" in overview.text
    assert "What the full workflow does" in overview.text
    assert "Light scan" in overview.text
    assert "Run full workflow" in overview.text
    assert "Source sync only" in overview.text
    assert "English v2 jobs" in overview.text
    assert "Jobs to analyze" in overview.text
    assert "Fetch priority details" in overview.text
    assert "Repair / translate English" in overview.text
    assert "Analyze ready jobs" in overview.text
    assert "Quick Add" in jobs.text
    assert "Job URL, search URL, or keyword" in jobs.text
    assert "Process fetched jobs fully" in jobs.text
    assert "Market intelligence" in market.text


def test_full_workflow_rejects_invalid_model_stage_bounds_before_network(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    token = app.state.csrf_token
    with TestClient(app) as client:
        response = client.post(
            "/actions/full-workflow",
            data={
                "csrf_token": token,
                "search_limit": "1",
                "request_budget": "1",
                "missing_limit": "0",
                "refresh_limit": "0",
                "refresh_after_hours": "24",
                "translation_limit": "0",
                "analysis_limit": "1",
            },
            follow_redirects=False,
        )

    assert response.status_code == 400
    assert "translation limit must be 1-50" in response.text


def test_web_app_rejects_unapproved_quick_add_url_before_network(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    token = app.state.csrf_token
    with TestClient(app) as client:
        response = client.post(
            "/actions/quick-add",
            data={
                "csrf_token": token,
                "value": "https://example.com/jobs/123",
                "pages": "1",
                "detail_limit": "5",
            },
            follow_redirects=False,
        )

    assert response.status_code == 400
    assert "Jobinja URLs only" in response.text


def test_web_app_renders_discovered_job_and_allows_triage(tmp_path: Path) -> None:
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
    token = app.state.csrf_token
    with TestClient(app) as client:
        overview = client.get("/")
        detail_response = client.get("/jobs/tmW5")
        list_response = client.get("/jobs")
        triage_response = client.post(
            "/jobs/tmW5/triage",
            data={"csrf_token": token, "triage_state": "interested"},
            follow_redirects=False,
        )
        interested = client.get("/jobs", params={"triage": "interested"})

    assert "Example discovered job" in overview.text
    assert "Jobinja reference: tmW5" in overview.text
    assert 'action="/jobs/tmW5/fetch"' in overview.text
    assert 'name="return_to" value="/"' in overview.text
    assert detail_response.status_code == 200
    assert "Details not acquired yet" in detail_response.text
    assert "Fetch details" in detail_response.text
    assert "Jobinja reference tmW5" in detail_response.text
    assert "jobhunter jobinja fetch tmW5" not in detail_response.text
    assert "Company: Example Company" in list_response.text
    assert "Jobinja reference: tmW5" in list_response.text
    assert "Not fetched" in list_response.text
    assert triage_response.status_code == 303
    assert "Example discovered job" in interested.text
    assert "interested" in interested.text


def test_web_app_unknown_job_is_real_404(tmp_path: Path) -> None:
    app = create_app(_settings(tmp_path))
    with TestClient(app) as client:
        response = client.get("/jobs/not-known")

    assert response.status_code == 404
