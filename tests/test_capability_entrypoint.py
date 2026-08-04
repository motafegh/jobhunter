from pathlib import Path
from types import SimpleNamespace

import jobhunter.entrypoint as entrypoint


class _Service:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def analyze_job(self, job_id: str):
        self.calls.append(job_id)
        return SimpleNamespace(
            source_job_id=job_id,
            artifact_id=7,
            outcome="completed",
            model="analysis-model",
            capabilities=2,
            analysis_artifact_id=5,
            translation_artifact_id=4,
        )


class _Store:
    artifact = SimpleNamespace(
        source_job_id="abc1",
        model="analysis-model",
        prompt_version="job-capability-intelligence-v2",
        schema_version="job-capability-intelligence-v2",
        analysis_artifact_id=5,
        intelligence={
            "role_interpretation": "A sufficiently long interpreted role description.",
            "capabilities": [],
            "cross_capability_observations": [],
            "uncertainties": [],
        },
    )

    def __init__(self, _database_path: Path) -> None:
        pass

    def latest_current(self, source_job_id: str, **_kwargs):
        assert source_job_id == "abc1"
        return self.artifact


def test_jobs_capability_routes_to_new_service(monkeypatch, capsys, tmp_path: Path) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    service = _Service()
    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)
    monkeypatch.setattr(
        entrypoint,
        "build_capability_intelligence_service",
        lambda _settings: service,
    )
    monkeypatch.setattr(entrypoint, "CapabilityIntelligenceStore", _Store)

    exit_code = entrypoint.main(["jobs", "capability", "abc1"])

    assert exit_code == 0
    assert service.calls == ["abc1"]
    output = capsys.readouterr().out
    assert "Outcome: completed" in output
    assert "Capability intelligence for abc1" in output


def test_global_config_can_precede_capability_command(
    monkeypatch,
    capsys,
    tmp_path: Path,
) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    service = _Service()
    seen_paths: list[Path | None] = []

    def load(path):
        seen_paths.append(path)
        return settings

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(
        entrypoint,
        "build_capability_intelligence_service",
        lambda _settings: service,
    )
    monkeypatch.setattr(entrypoint, "CapabilityIntelligenceStore", _Store)

    exit_code = entrypoint.main(
        ["--config", "custom.toml", "jobs", "capability", "abc1"]
    )

    assert exit_code == 0
    assert seen_paths == [Path("custom.toml")]
    assert service.calls == ["abc1"]
    assert "Outcome: completed" in capsys.readouterr().out
