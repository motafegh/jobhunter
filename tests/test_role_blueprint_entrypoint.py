from pathlib import Path
from types import SimpleNamespace

import jobhunter.entrypoint as entrypoint


class _Service:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def build(self, job_id: str):
        self.calls.append(job_id)
        return SimpleNamespace(
            source_job_id=job_id,
            artifact_id=9,
            outcome="completed",
            model="analysis-model",
            capability_areas=3,
            capability_artifact_id=7,
        )


class _Store:
    artifact = SimpleNamespace(
        source_job_id="abc1",
        model="analysis-model",
        prompt_version="role-capability-blueprint-v1",
        schema_version="role-capability-blueprint-v1",
        capability_artifact_id=7,
        analysis_artifact_id=5,
        translation_artifact_id=4,
        blueprint={
            "role_read": "An applied AI automation role.",
            "likely_role_shape": "Applied AI Automation / Integration Engineer",
            "capability_areas": [],
            "hidden_requirements": [],
            "likely_end_to_end_scenarios": [],
            "what_probably_does_not_matter": [],
            "important_unknowns": [],
            "bottom_line": "Build reliable AI-assisted business workflows.",
        },
    )

    def __init__(self, _database_path: Path) -> None:
        pass

    def latest_current(self, source_job_id: str, **_kwargs):
        assert source_job_id == "abc1"
        return self.artifact


def test_jobs_blueprint_routes_to_role_blueprint_service(monkeypatch, capsys, tmp_path: Path) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    service = _Service()
    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)
    monkeypatch.setattr(entrypoint, "build_role_blueprint_service", lambda _settings: service)
    monkeypatch.setattr(entrypoint, "RoleBlueprintStore", _Store)

    exit_code = entrypoint.main(["jobs", "blueprint", "abc1"])

    assert exit_code == 0
    assert service.calls == ["abc1"]
    output = capsys.readouterr().out
    assert "Outcome: completed" in output
    assert "Role Capability Blueprint for abc1" in output


def test_global_config_can_precede_blueprint_command(monkeypatch, capsys, tmp_path: Path) -> None:
    settings = SimpleNamespace(database_path=tmp_path / "jobhunter.sqlite3")
    service = _Service()
    seen_paths: list[Path | None] = []

    def load(path):
        seen_paths.append(path)
        return settings

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(entrypoint, "build_role_blueprint_service", lambda _settings: service)
    monkeypatch.setattr(entrypoint, "RoleBlueprintStore", _Store)

    exit_code = entrypoint.main(["--config", "custom.toml", "jobs", "blueprint", "abc1"])

    assert exit_code == 0
    assert seen_paths == [Path("custom.toml")]
    assert service.calls == ["abc1"]
    assert "Outcome: completed" in capsys.readouterr().out


def test_global_help_surfaces_blueprint_without_breaking_phase1_heading(capsys) -> None:
    assert entrypoint.main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "Additional Phase-1 commands" in output
    assert "jobs blueprint <id>" in output
