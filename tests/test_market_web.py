from pathlib import Path

from fastapi.testclient import TestClient

from jobhunter.config import Settings
from jobhunter.market_workspace import MarketWorkspaceService
from jobhunter.web.launcher import build_runtime_app


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
    )


def test_runtime_app_registers_target_scoped_market_routes(tmp_path: Path) -> None:
    app = build_runtime_app(_settings(tmp_path))
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in (getattr(route, "methods", None) or set())
    }

    assert ("/market/targets", "GET") in route_methods
    assert ("/market/runs/{run_id}", "GET") in route_methods
    assert ("/market/snapshots/{snapshot_id}", "GET") in route_methods
    assert ("/market/actions/target", "POST") in route_methods
    assert ("/market/actions/definition", "POST") in route_methods
    assert ("/market/actions/run", "POST") in route_methods


def test_market_workspace_renders_same_persisted_target_definition(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    workspace = MarketWorkspaceService(settings)
    target = workspace.create_target(
        slug="applied-ai",
        name="Applied AI",
        description="Target-scoped market evidence",
    )
    definition = workspace.create_definition(
        target.id,
        membership_intent="Applied AI engineering work",
        search_profiles=("ai-focused",),
    )

    response = TestClient(build_runtime_app(settings)).get(
        f"/market/targets?definition_id={definition.id}"
    )

    assert response.status_code == 200
    assert "Market targets" in response.text
    assert "Applied AI" in response.text
    assert "Applied AI engineering work" in response.text
    assert "Run bounded Market update" in response.text
    assert "Search vocabulary is candidate acquisition only" in response.text


def test_market_browser_unknown_history_is_not_fabricated(tmp_path: Path) -> None:
    client = TestClient(build_runtime_app(_settings(tmp_path)))

    assert client.get("/market/runs/999").status_code == 404
    assert client.get("/market/snapshots/999").status_code == 404
