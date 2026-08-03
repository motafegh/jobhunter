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


def test_global_help_surfaces_complete_run_command(capsys) -> None:
    assert entrypoint.main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "Additional complete workflow command" in output
    assert "run --help" in output
