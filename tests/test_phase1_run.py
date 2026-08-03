from types import SimpleNamespace

from jobhunter.analysis_service import AnalysisBatchSummary
from jobhunter.config import JobinjaSearchDefinition, Settings
from jobhunter.market_insights import MarketSummary
from jobhunter.phase1_run import Phase1RunService, configured_searches
from jobhunter.translation_service import TranslationBatchSummary, TranslationFailure


class _SyncService:
    def __init__(self, *, succeeded: bool = True, preferred_ids=()) -> None:
        self.succeeded = succeeded
        self.preferred_ids = tuple(preferred_ids)
        self.calls = []

    def run(self, searches, **kwargs):
        self.calls.append((tuple(searches), kwargs))
        detail_fetch = None
        if self.preferred_ids:
            detail_fetch = SimpleNamespace(
                results=tuple(
                    SimpleNamespace(source_job_id=job_id) for job_id in self.preferred_ids
                )
            )
        return SimpleNamespace(succeeded=self.succeeded, detail_fetch=detail_fetch)


class _TranslationService:
    def __init__(self, *, summary: TranslationBatchSummary, current_ids=()) -> None:
        self.summary = summary
        self.current_ids = set(current_ids)
        self.calls = []

    def run(self, **kwargs):
        self.calls.append(kwargs)
        return self.summary

    def current_artifact(self, source_job_id: str):
        if source_job_id in self.current_ids:
            return SimpleNamespace(id=1)
        return None


class _SourceStore:
    def __init__(self, ids) -> None:
        self.sources = tuple(
            SimpleNamespace(source_job_id=job_id, job_detail_version_id=index)
            for index, job_id in enumerate(ids, start=1)
        )

    def latest_source_versions(self, *, limit: int):
        return self.sources[:limit]


class _AnalysisStore:
    def __init__(self, current_ids=()) -> None:
        self.current_ids = set(current_ids)

    def latest_current(self, source_job_id: str, **_kwargs):
        if source_job_id in self.current_ids:
            return SimpleNamespace(id=1)
        return None


class _WorkflowStore:
    def __init__(self, not_relevant=()) -> None:
        self.not_relevant = set(not_relevant)

    def get_state(self, source_job_id: str):
        return SimpleNamespace(
            triage_state=(
                "not_relevant" if source_job_id in self.not_relevant else "unreviewed"
            )
        )


class _AnalysisService:
    def __init__(self, summary: AnalysisBatchSummary) -> None:
        self.summary = summary
        self.calls = []

    def run(self, source_job_ids, *, limit: int):
        self.calls.append((tuple(source_job_ids), limit))
        return self.summary


class _Market:
    def market_summary(self):
        return MarketSummary(
            discovered_jobs=10,
            current_parsed_jobs=8,
            analyzed_jobs=4,
            distinct_employers=3,
            largest_employer_jobs=2,
            responsibility_claims=12,
            requirement_claims=20,
            analysis_model="analysis-model",
            analysis_prompt_version="job-analysis-prompt-v2",
            analysis_schema_version="job-analysis-v2",
            sample_warning="small sample",
            concentration_warning=None,
            requirements=(),
        )


def _translation_summary(*, failures=()) -> TranslationBatchSummary:
    return TranslationBatchSummary(
        attempted=0,
        results=(),
        failures=tuple(failures),
    )


def _analysis_summary(*, results=(), failures=()) -> AnalysisBatchSummary:
    return AnalysisBatchSummary(
        attempted=len(tuple(results)) + len(tuple(failures)),
        results=tuple(results),
        failures=tuple(failures),
    )


def test_phase1_run_selects_only_current_relevant_missing_analyses() -> None:
    sync = _SyncService(preferred_ids=("new",))
    translation = _TranslationService(
        summary=_translation_summary(),
        current_ids=("new", "ordinary", "ignored", "done"),
    )
    analysis_result = SimpleNamespace(source_job_id="new")
    analysis = _AnalysisService(_analysis_summary(results=(analysis_result,)))
    service = Phase1RunService(
        sync_service=sync,
        translation_service=translation,
        analysis_service=analysis,
        source_store=_SourceStore(("ordinary", "ignored", "done", "new")),
        analysis_store=_AnalysisStore(current_ids=("done",)),
        workflow_store=_WorkflowStore(not_relevant=("ignored",)),
        market_insights=_Market(),
        translation_enabled=True,
        analysis_model="analysis-model",
    )

    summary = service.run(
        (SimpleNamespace(name="search"),),
        missing_limit=1,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=5,
        analysis_limit=1,
    )

    assert summary.status == "completed"
    assert summary.analysis_selected == ("new",)
    assert summary.analysis_eligible_before == 2
    assert summary.analysis_remaining == 1
    assert analysis.calls == [(('new',), 1)]
    assert translation.calls[0]["preferred_ids"] == ("new",)


def test_phase1_run_preserves_partial_success_when_translation_has_failures() -> None:
    failure = TranslationFailure(source_job_id="bad", error="translation failed")
    service = Phase1RunService(
        sync_service=_SyncService(),
        translation_service=_TranslationService(
            summary=_translation_summary(failures=(failure,)),
            current_ids=(),
        ),
        analysis_service=_AnalysisService(_analysis_summary()),
        source_store=_SourceStore(()),
        analysis_store=_AnalysisStore(),
        workflow_store=_WorkflowStore(),
        market_insights=_Market(),
        translation_enabled=True,
        analysis_model="analysis-model",
    )

    summary = service.run(
        (SimpleNamespace(name="search"),),
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=5,
        analysis_limit=2,
    )

    assert summary.status == "completed_with_failures"
    assert summary.translation is not None
    assert len(summary.translation.failures) == 1
    assert summary.analysis_skipped_reason == "no eligible current jobs need analysis"


def test_phase1_run_marks_disabled_model_stages_as_attention_required() -> None:
    service = Phase1RunService(
        sync_service=_SyncService(),
        translation_service=_TranslationService(summary=_translation_summary()),
        analysis_service=None,
        source_store=_SourceStore(()),
        analysis_store=_AnalysisStore(),
        workflow_store=_WorkflowStore(),
        market_insights=_Market(),
        translation_enabled=False,
        analysis_model=None,
    )

    summary = service.run(
        (SimpleNamespace(name="search"),),
        missing_limit=0,
        refresh_limit=0,
        refresh_after_hours=24,
        translation_limit=5,
        analysis_limit=2,
    )

    assert summary.status == "completed_with_failures"
    assert summary.translation_skipped_reason == "translation is disabled in configuration"
    assert summary.analysis_skipped_reason == "no analysis model is configured"


def test_configured_searches_deduplicates_canonical_urls() -> None:
    url = "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=Python"
    settings = Settings(
        jobinja_searches=[
            JobinjaSearchDefinition(name="one", url=url),
            JobinjaSearchDefinition(name="two", url=url),
        ]
    )

    searches = configured_searches(settings, limit=10)

    assert len(searches) == 1
    assert searches[0].name == "one"
