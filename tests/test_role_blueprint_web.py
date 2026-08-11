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


def test_runtime_app_registers_role_blueprint_routes(tmp_path: Path) -> None:
    app = build_runtime_app(_settings(tmp_path))
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in (getattr(route, "methods", None) or set())
    }

    path = "/jobs/{source_job_id}/role-blueprint"
    assert (path, "GET") in route_methods
    assert (path, "POST") in route_methods


def test_role_blueprint_page_renders_before_capability_analysis(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    store = JobHunterStore(settings.database_path)
    store.initialize()
    store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="bpweb1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/bpweb1/example",
            observed_text="AI Automation Specialist",
        ),
        observed_at=datetime(2026, 8, 4, tzinfo=UTC),
    )

    response = TestClient(build_runtime_app(settings)).get("/jobs/bpweb1/role-blueprint")

    assert response.status_code == 200
    assert "Role Capability Blueprint" in response.text
    assert "Capability Intelligence required" in response.text
    assert "professional interpretation" in response.text


def test_role_blueprint_template_exposes_v6_boundary_not_legacy_expansion() -> None:
    template = Path("src/jobhunter/web/templates/role_blueprint.html").read_text(
        encoding="utf-8"
    )

    assert "professional_considerations" in template
    assert "important_unknowns" in template
    assert "source_role_purpose" in template
    for legacy_key in (
        "area.practical_interpretation",
        "area.interpretation_uncertainty",
        "area.probably_not_required",
        "bp.role_read",
        "bp.likely_role_shape",
        "area.likely_depth",
        "area.suggested_tools_or_examples",
        "bp.hidden_requirements",
        "bp.professional_example_scenarios",
        "bp.bottom_line",
    ):
        assert legacy_key not in template
