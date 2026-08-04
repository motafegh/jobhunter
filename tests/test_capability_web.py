from pathlib import Path

from jobhunter.config import Settings
from jobhunter.web.launcher import build_runtime_app


def test_runtime_app_registers_capability_review_routes(tmp_path: Path) -> None:
    settings = Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
    )

    app = build_runtime_app(settings)
    route_methods = {
        (route.path, method)
        for route in app.routes
        for method in (getattr(route, "methods", None) or set())
    }

    path = "/jobs/{source_job_id}/capability-intelligence"
    assert (path, "GET") in route_methods
    assert (path, "POST") in route_methods
