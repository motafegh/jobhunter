from pathlib import Path
from types import SimpleNamespace

import pytest

import jobhunter.web.app as web_app
from jobhunter.config import Settings


class _RunService:
    def __init__(self, *, status: str) -> None:
        self.summary = SimpleNamespace(status=status)
        self.calls = []

    def run(self, searches, **kwargs):
        self.calls.append((tuple(searches), kwargs))
        return self.summary


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
        translation_enabled=True,
        analysis_lm_studio_model="analysis-model",
    )


def _patch_shared_run(monkeypatch, *, status: str) -> _RunService:
    service = _RunService(status=status)
    monkeypatch.setattr(
        web_app,
        "configured_phase1_searches",
        lambda _settings, *, limit: (SimpleNamespace(name=f"search-{limit}"),),
    )
    monkeypatch.setattr(
        web_app,
        "build_phase1_run_service",
        lambda _settings, *, request_budget: (
            service if request_budget == 3 else None
        ),
    )
    monkeypatch.setattr(
        web_app,
        "format_phase1_run_summary",
        lambda summary: f"shared summary: {summary.status}",
    )
    return service


def test_full_workflow_uses_shared_phase1_service_and_summary(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    service = _patch_shared_run(monkeypatch, status="completed")

    result = web_app._full_workflow_output(
        settings,
        search_limit=2,
        request_budget=3,
        missing_limit=4,
        refresh_limit=5,
        refresh_after_hours=24,
        translation_limit=6,
        analysis_limit=7,
    )

    assert result.status == "completed"
    assert result.summary == "shared summary: completed"
    assert service.calls == [
        (
            (SimpleNamespace(name="search-2"),),
            {
                "missing_limit": 4,
                "refresh_limit": 5,
                "refresh_after_hours": 24,
                "translation_limit": 6,
                "analysis_limit": 7,
            },
        )
    ]


def test_full_workflow_preserves_shared_partial_success_status(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    _patch_shared_run(monkeypatch, status="completed_with_failures")

    result = web_app._full_workflow_output(
        settings,
        search_limit=2,
        request_budget=3,
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=1,
        analysis_limit=1,
    )

    assert result.status == "completed_with_failures"
    assert result.summary == "shared summary: completed_with_failures"


def test_full_workflow_rejects_empty_configured_search_plan(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    monkeypatch.setattr(
        web_app,
        "configured_phase1_searches",
        lambda _settings, *, limit: (),
    )

    with pytest.raises(ValueError, match="No enabled Jobinja searches"):
        web_app._full_workflow_output(
            settings,
            search_limit=2,
            request_budget=3,
            missing_limit=0,
            refresh_limit=0,
            refresh_after_hours=24,
            translation_limit=1,
            analysis_limit=1,
        )


def test_complete_processing_distinguishes_intentional_not_requested(
    tmp_path: Path,
) -> None:
    result = web_app._complete_processing_result(
        _settings(tmp_path),
        ("job-1",),
        requested=False,
    )

    assert result.status == "completed"
    assert "Skipped intentionally" in result.summary
    assert "not requested" in result.summary


def test_complete_processing_preserves_translation_failure_as_partial_success(
    tmp_path: Path,
    monkeypatch,
) -> None:
    class Translation:
        def run(self, **_kwargs):
            return SimpleNamespace(
                results=(),
                failures=(SimpleNamespace(source_job_id="bad", error="provider failed"),),
            )

    monkeypatch.setattr(web_app, "_translation_service", lambda _settings: Translation())
    monkeypatch.setattr(
        web_app,
        "format_translation_batch_summary",
        lambda _summary: "translation: attempted=1, completed=0, failed=1",
    )

    result = web_app._complete_processing_result(
        _settings(tmp_path),
        ("bad",),
        requested=True,
    )

    assert result.status == "completed_with_failures"
    assert "translation: attempted=1, completed=0, failed=1" in result.summary
    assert "no requested jobs produced a current English projection" in result.summary


def test_complete_processing_keeps_completed_translation_when_analysis_fails(
    tmp_path: Path,
    monkeypatch,
) -> None:
    class Translation:
        def run(self, **_kwargs):
            return SimpleNamespace(
                results=(SimpleNamespace(source_job_id="good"),),
                failures=(),
            )

    class Analysis:
        def run_english(self, job_ids, *, limit):
            assert job_ids == ("good",)
            assert limit == 1
            return SimpleNamespace(
                results=(),
                failures=(SimpleNamespace(source_job_id="good", error="model failed"),),
            )

    monkeypatch.setattr(web_app, "_translation_service", lambda _settings: Translation())
    monkeypatch.setattr(web_app, "_analysis_service", lambda _settings: Analysis())
    monkeypatch.setattr(
        web_app,
        "format_translation_batch_summary",
        lambda _summary: "translation completed",
    )
    monkeypatch.setattr(
        web_app,
        "format_analysis_batch_summary",
        lambda _summary: "analysis failed",
    )

    result = web_app._complete_processing_result(
        _settings(tmp_path),
        ("good",),
        requested=True,
    )

    assert result.status == "completed_with_failures"
    assert "translation completed" in result.summary
    assert "analysis failed" in result.summary
