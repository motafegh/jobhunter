from pathlib import Path
from types import SimpleNamespace

import jobhunter.entrypoint as entrypoint
from jobhunter.config import Settings


class _RunService:
    def __init__(self, *, has_failures: bool = False) -> None:
        self.has_failures = has_failures
        self.calls = []

    def run(self, searches, **kwargs):
        self.calls.append((tuple(searches), kwargs))
        return SimpleNamespace(has_failures=self.has_failures)


class _AnalysisService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def analyze_english_job(self, source_job_id: str):
        self.calls.append(("english", source_job_id))
        return SimpleNamespace(
            source_job_id=source_job_id,
            artifact_id=41,
            outcome="completed",
            model="analysis-model",
            responsibilities=2,
            requirements=3,
        )

    def analyze_original_job(self, source_job_id: str):
        self.calls.append(("original", source_job_id))
        return SimpleNamespace(
            source_job_id=source_job_id,
            artifact_id=42,
            outcome="reused",
            model="analysis-model",
            responsibilities=1,
            requirements=4,
        )


def test_run_command_uses_bounded_settings_defaults(monkeypatch, capsys) -> None:
    settings = Settings(
        jobinja_search_request_budget=7,
        jobinja_max_expanded_searches=9,
        jobinja_sync_missing_limit=3,
        jobinja_sync_refresh_limit=2,
        jobinja_refresh_after_hours=12,
        translation_batch_limit=4,
        analysis_batch_limit=2,
    )
    service = _RunService()
    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)
    monkeypatch.setattr(
        entrypoint,
        "configured_searches",
        lambda _settings, *, limit: (SimpleNamespace(name=f"limit-{limit}"),),
    )
    monkeypatch.setattr(
        entrypoint,
        "build_phase1_run_service",
        lambda _settings, *, request_budget: (
            service if request_budget == 7 else None
        ),
    )
    monkeypatch.setattr(entrypoint, "format_phase1_run_summary", lambda _summary: "summary")

    exit_code = entrypoint.main(["run"])

    assert exit_code == 0
    assert service.calls == [
        (
            (SimpleNamespace(name="limit-9"),),
            {
                "missing_limit": 3,
                "refresh_limit": 2,
                "refresh_after_hours": 12,
                "translation_limit": 4,
                "analysis_limit": 2,
            },
        )
    ]
    assert "summary" in capsys.readouterr().out


def test_run_command_accepts_global_config_before_run(monkeypatch) -> None:
    captured = {}
    settings = Settings()
    service = _RunService()

    def load(path):
        captured["path"] = path
        return settings

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(
        entrypoint,
        "configured_searches",
        lambda _settings, *, limit: (SimpleNamespace(name=str(limit)),),
    )
    monkeypatch.setattr(
        entrypoint,
        "build_phase1_run_service",
        lambda _settings, *, request_budget: service,
    )
    monkeypatch.setattr(entrypoint, "format_phase1_run_summary", lambda _summary: "summary")

    exit_code = entrypoint.main(
        ["--config", "custom.toml", "run", "--missing-limit", "0", "--refresh-limit", "0"]
    )

    assert exit_code == 0
    assert captured["path"] == Path("custom.toml")


def test_jobs_health_command_uses_same_config_and_reader(monkeypatch, capsys) -> None:
    captured = {}
    settings = Settings(database_path=Path("custom.sqlite3"))

    class Reader:
        def __init__(self, database_path: Path) -> None:
            captured["database_path"] = database_path

        def get(self, source_job_id: str):
            captured["source_job_id"] = source_job_id
            return SimpleNamespace(source_job_id=source_job_id)

    monkeypatch.setattr(entrypoint, "_load_settings", lambda path: settings)
    monkeypatch.setattr(entrypoint, "SourceHealthReader", Reader)
    monkeypatch.setattr(
        entrypoint,
        "format_source_health",
        lambda summary: f"health:{summary.source_job_id}",
    )

    exit_code = entrypoint.main(["jobs", "health", "abc1"])

    assert exit_code == 0
    assert captured == {
        "database_path": Path("custom.sqlite3"),
        "source_job_id": "abc1",
    }
    assert "health:abc1" in capsys.readouterr().out


def test_global_config_can_precede_jobs_health(monkeypatch) -> None:
    captured = {}
    settings = Settings(database_path=Path("custom.sqlite3"))

    def load(path):
        captured["config"] = path
        return settings

    class Reader:
        def __init__(self, _database_path: Path) -> None:
            pass

        def get(self, source_job_id: str):
            return SimpleNamespace(source_job_id=source_job_id)

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(entrypoint, "SourceHealthReader", Reader)
    monkeypatch.setattr(entrypoint, "format_source_health", lambda _summary: "health")

    assert entrypoint.main(["--config", "custom.toml", "jobs", "health", "abc1"]) == 0
    assert captured["config"] == Path("custom.toml")


def test_jobs_analyze_defaults_to_english_and_uses_targeted_service(monkeypatch, capsys) -> None:
    settings = Settings()
    service = _AnalysisService()
    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)
    monkeypatch.setattr(entrypoint, "build_job_analysis_service", lambda _settings: service)

    exit_code = entrypoint.main(["jobs", "analyze", "t4jp"])

    assert exit_code == 0
    assert service.calls == [("english", "t4jp")]
    output = capsys.readouterr().out
    assert "English P1.6 for t4jp" in output
    assert "Artifact: 41" in output
    assert "job-analysis-english-v9 / job-analysis-v4" in output


def test_jobs_analyze_can_target_original_language(monkeypatch, capsys) -> None:
    settings = Settings()
    service = _AnalysisService()
    monkeypatch.setattr(entrypoint, "_load_settings", lambda _path: settings)
    monkeypatch.setattr(entrypoint, "build_job_analysis_service", lambda _settings: service)

    exit_code = entrypoint.main(["jobs", "analyze", "t4jp", "--mode", "original"])

    assert exit_code == 0
    assert service.calls == [("original", "t4jp")]
    output = capsys.readouterr().out
    assert "Original-language P1.6 for t4jp" in output
    assert "Artifact: 42" in output
    assert "job-analysis-original-v9 / job-analysis-v4" in output


def test_global_config_can_precede_jobs_analyze(monkeypatch) -> None:
    captured = {}
    service = _AnalysisService()

    def load(path):
        captured["config"] = path
        return Settings()

    monkeypatch.setattr(entrypoint, "_load_settings", load)
    monkeypatch.setattr(entrypoint, "build_job_analysis_service", lambda _settings: service)

    assert (
        entrypoint.main(["--config", "custom.toml", "jobs", "analyze", "t4jp"])
        == 0
    )
    assert captured["config"] == Path("custom.toml")
    assert service.calls == [("english", "t4jp")]


def test_global_help_surfaces_phase1_commands(capsys) -> None:
    assert entrypoint.main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "Additional Phase-1 commands" in output
    assert "run --help" in output
    assert "jobs health <id>" in output
    assert "jobs analyze <id>" in output
