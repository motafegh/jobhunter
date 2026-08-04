from pathlib import Path
from types import SimpleNamespace

import jobhunter.web.app as web_app
from jobhunter.config import Settings


class _TranslationService:
    def __init__(self, *, failures=()) -> None:
        self._failures = failures

    def run(self, **_kwargs):
        return SimpleNamespace(failures=self._failures, results=())


class _Repository:
    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def list_jobs(self, **_kwargs):
        return ()


class _Market:
    def market_summary(self):
        return SimpleNamespace(
            discovered_jobs=10,
            current_parsed_jobs=8,
            analyzed_jobs=4,
            distinct_employers=3,
            responsibility_claims=12,
            requirement_claims=20,
            sample_warning="small sample",
            concentration_warning=None,
        )


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
        translation_enabled=True,
        analysis_lm_studio_model="analysis-model",
    )


def _patch_common(monkeypatch, *, sync_succeeded: bool, translation_failures=()) -> None:
    monkeypatch.setattr(
        web_app,
        "_run_sync",
        lambda *_args, **_kwargs: SimpleNamespace(succeeded=sync_succeeded),
    )
    monkeypatch.setattr(web_app, "_successful_detail_ids", lambda _summary: ())
    monkeypatch.setattr(web_app, "format_web_sync_summary", lambda _summary: "sync")
    monkeypatch.setattr(
        web_app,
        "_translation_service",
        lambda _settings: _TranslationService(failures=translation_failures),
    )
    monkeypatch.setattr(
        web_app,
        "format_translation_batch_summary",
        lambda _summary: "translation",
    )
    monkeypatch.setattr(web_app, "WebRepository", _Repository)
    monkeypatch.setattr(web_app, "_market_insights", lambda _settings: _Market())


def test_full_workflow_returns_completed_when_all_executed_stages_are_clean(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    _patch_common(monkeypatch, sync_succeeded=True)

    result = web_app._full_workflow_output(
        settings,
        search_limit=1,
        request_budget=1,
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=1,
        analysis_limit=1,
    )

    assert result.status == "completed"
    assert "Current accepted English analyses: 4" in result.summary
    assert "Market sampling warning" in result.summary


def test_full_workflow_returns_partial_success_when_sync_has_attention_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    _patch_common(monkeypatch, sync_succeeded=False)

    result = web_app._full_workflow_output(
        settings,
        search_limit=1,
        request_budget=1,
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=1,
        analysis_limit=1,
    )

    assert result.status == "completed_with_failures"


def test_full_workflow_returns_partial_success_when_translation_batch_has_failures(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = _settings(tmp_path)
    _patch_common(
        monkeypatch,
        sync_succeeded=True,
        translation_failures=(SimpleNamespace(error="bad translation"),),
    )

    result = web_app._full_workflow_output(
        settings,
        search_limit=1,
        request_budget=1,
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=1,
        analysis_limit=1,
    )

    assert result.status == "completed_with_failures"


def test_full_workflow_marks_disabled_semantic_pipeline_as_incomplete(
    tmp_path: Path,
    monkeypatch,
) -> None:
    settings = Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        evidence_dir=tmp_path / "evidence",
        translation_enabled=False,
    )
    monkeypatch.setattr(
        web_app,
        "_run_sync",
        lambda *_args, **_kwargs: SimpleNamespace(succeeded=True),
    )
    monkeypatch.setattr(web_app, "_successful_detail_ids", lambda _summary: ())
    monkeypatch.setattr(web_app, "format_web_sync_summary", lambda _summary: "sync")
    monkeypatch.setattr(web_app, "_market_insights", lambda _settings: _Market())

    result = web_app._full_workflow_output(
        settings,
        search_limit=1,
        request_budget=1,
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=1,
        analysis_limit=1,
    )

    assert result.status == "completed_with_failures"
    assert "translation is disabled" in result.summary
    assert "no analysis model is configured" in result.summary
