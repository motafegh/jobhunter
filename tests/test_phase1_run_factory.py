from pathlib import Path

import jobhunter.phase1_run as phase1_run
from jobhunter.config import Settings
from jobhunter.lifecycle import LifecycleStore


def test_phase1_run_factory_uses_configured_retries_and_lifecycle_store(
    tmp_path: Path,
    monkeypatch,
) -> None:
    captured = {}

    class Client:
        def __init__(self, **kwargs) -> None:
            captured["client"] = kwargs

    class DetailService:
        def __init__(self, **kwargs) -> None:
            captured["detail"] = kwargs

    monkeypatch.setattr(phase1_run, "JobinjaClient", Client)
    monkeypatch.setattr(phase1_run, "JobinjaDetailService", DetailService)

    settings = Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
        jobinja_max_retries=3,
    )

    phase1_run.build_phase1_run_service(settings, request_budget=7)

    assert captured["client"]["max_retries"] == 3
    assert isinstance(captured["detail"]["lifecycle_store"], LifecycleStore)
