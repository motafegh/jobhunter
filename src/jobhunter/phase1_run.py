"""Shared bounded Phase-1 orchestration for browser/CLI entry points.

The service composes the already-established acquisition, translation, analysis,
and Market layers without changing their authority. It deliberately keeps source
acquisition useful when model stages are unavailable and preserves partial success.
"""

from __future__ import annotations

from dataclasses import dataclass

from jobhunter.analysis_service import (
    ANALYSIS_SCHEMA_VERSION,
    PROMPT_VERSION,
    AnalysisBatchSummary,
    JobAnalysisService,
    format_analysis_batch_summary,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.evidence import EvidenceStore
from jobhunter.inference import LMStudioProvider
from jobhunter.job_audit import JobDetailAuditor
from jobhunter.job_catalog import JobCatalog
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.job_workflow import JobWorkflowStore
from jobhunter.jobinja_batch import JobinjaBatchFetchService
from jobhunter.jobinja_detail_service import JobinjaDetailService
from jobhunter.jobinja_discovery import DiscoverySearch, JobinjaDiscoveryService
from jobhunter.jobinja_sync import JobinjaSyncService, JobinjaSyncSummary, format_sync_summary
from jobhunter.lifecycle import LifecycleStore
from jobhunter.market_insights import MarketInsights, MarketSummary
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobHunterStore
from jobhunter.translation import GoogleCloudTranslationProvider, LMStudioTranslationProvider
from jobhunter.translation_service import (
    TranslationBatchSummary,
    TranslationService,
    format_translation_batch_summary,
)
from jobhunter.translation_store import TranslationStore


@dataclass(frozen=True, slots=True)
class Phase1RunSummary:
    """One complete bounded source-to-Market orchestration result."""

    status: str
    sync: JobinjaSyncSummary
    translation: TranslationBatchSummary | None
    translation_skipped_reason: str | None
    analysis: AnalysisBatchSummary | None
    analysis_skipped_reason: str | None
    analysis_selected: tuple[str, ...]
    analysis_eligible_before: int | None
    analysis_remaining: int | None
    market: MarketSummary

    @property
    def has_failures(self) -> bool:
        return self.status == "completed_with_failures"


class Phase1RunService:
    """Compose Phase-1 services while retaining their independent durable results."""

    def __init__(
        self,
        *,
        sync_service: JobinjaSyncService,
        translation_service: TranslationService,
        analysis_service: JobAnalysisService | None,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        workflow_store: JobWorkflowStore,
        market_insights: MarketInsights,
        translation_enabled: bool,
        analysis_model: str | None,
    ) -> None:
        self._sync_service = sync_service
        self._translation_service = translation_service
        self._analysis_service = analysis_service
        self._source_store = source_store
        self._analysis_store = analysis_store
        self._workflow_store = workflow_store
        self._market_insights = market_insights
        self._translation_enabled = translation_enabled
        self._analysis_model = analysis_model

    def _analysis_ready_ids(
        self,
        *,
        preferred_ids: tuple[str, ...],
        limit: int,
    ) -> tuple[tuple[str, ...], int]:
        if self._analysis_service is None or self._analysis_model is None:
            return (), 0

        preferred_rank = {job_id: index for index, job_id in enumerate(preferred_ids)}
        sources = list(self._source_store.latest_source_versions(limit=5000))
        sources.sort(
            key=lambda source: (
                0 if source.source_job_id in preferred_rank else 1,
                preferred_rank.get(source.source_job_id, source.job_detail_version_id),
                source.job_detail_version_id,
            )
        )

        selected: list[str] = []
        eligible = 0
        for source in sources:
            workflow = self._workflow_store.get_state(source.source_job_id)
            if workflow.triage_state == "not_relevant":
                continue
            if self._translation_service.current_artifact(source.source_job_id) is None:
                continue
            current = self._analysis_store.latest_current(
                source.source_job_id,
                model=self._analysis_model,
                prompt_version=PROMPT_VERSION,
                schema_version=ANALYSIS_SCHEMA_VERSION,
            )
            if current is not None:
                continue
            eligible += 1
            if len(selected) < limit:
                selected.append(source.source_job_id)
        return tuple(selected), eligible

    def run(
        self,
        searches: tuple[DiscoverySearch, ...],
        *,
        missing_limit: int,
        refresh_limit: int,
        refresh_after_hours: float,
        translation_limit: int,
        analysis_limit: int,
    ) -> Phase1RunSummary:
        if not searches:
            raise ValueError("At least one configured Jobinja search is required")
        if not 0 <= missing_limit <= 50:
            raise ValueError("missing_limit must be between 0 and 50")
        if not 0 <= refresh_limit <= 50:
            raise ValueError("refresh_limit must be between 0 and 50")
        if missing_limit + refresh_limit > 50:
            raise ValueError("combined missing and refresh limits may not exceed 50")
        if refresh_after_hours <= 0:
            raise ValueError("refresh_after_hours must be greater than zero")
        if not 1 <= translation_limit <= 50:
            raise ValueError("translation_limit must be between 1 and 50")
        if not 1 <= analysis_limit <= 20:
            raise ValueError("analysis_limit must be between 1 and 20")

        sync = self._sync_service.run(
            searches,
            missing_limit=missing_limit,
            refresh_limit=refresh_limit,
            refresh_after_hours=refresh_after_hours,
        )
        attention_required = not sync.succeeded
        preferred_ids = _successful_detail_ids(sync)

        translation: TranslationBatchSummary | None = None
        translation_skipped_reason: str | None = None
        if self._translation_enabled:
            translation = self._translation_service.run(
                missing=True,
                limit=translation_limit,
                preferred_ids=preferred_ids,
            )
            attention_required = attention_required or bool(translation.failures)
        else:
            translation_skipped_reason = "translation is disabled in configuration"
            attention_required = True

        analysis: AnalysisBatchSummary | None = None
        analysis_skipped_reason: str | None = None
        analysis_selected: tuple[str, ...] = ()
        analysis_eligible_before: int | None = None
        analysis_remaining: int | None = None

        if self._analysis_service is None or self._analysis_model is None:
            analysis_skipped_reason = "no analysis model is configured"
            attention_required = True
        else:
            analysis_selected, analysis_eligible_before = self._analysis_ready_ids(
                preferred_ids=preferred_ids,
                limit=analysis_limit,
            )
            if analysis_selected:
                analysis = self._analysis_service.run(
                    analysis_selected,
                    limit=analysis_limit,
                )
                attention_required = attention_required or bool(analysis.failures)
                analysis_remaining = max(
                    analysis_eligible_before - len(analysis.results),
                    0,
                )
            else:
                analysis_skipped_reason = "no eligible current jobs need analysis"
                analysis_remaining = 0

        market = self._market_insights.market_summary()
        return Phase1RunSummary(
            status=(
                "completed_with_failures" if attention_required else "completed"
            ),
            sync=sync,
            translation=translation,
            translation_skipped_reason=translation_skipped_reason,
            analysis=analysis,
            analysis_skipped_reason=analysis_skipped_reason,
            analysis_selected=analysis_selected,
            analysis_eligible_before=analysis_eligible_before,
            analysis_remaining=analysis_remaining,
            market=market,
        )


def configured_searches(settings: Settings, *, limit: int) -> tuple[DiscoverySearch, ...]:
    """Return the bounded configured search plan used by the complete Phase-1 run."""

    if not 1 <= limit <= 500:
        raise ValueError("search limit must be between 1 and 500")
    searches = [
        DiscoverySearch(name=item.name, url=item.url, max_pages=item.max_pages)
        for item in settings.jobinja_searches
        if item.enabled
    ]
    searches.extend(
        DiscoverySearch(name=item.name, url=item.url, max_pages=item.max_pages)
        for item in settings.expanded_keyword_searches()
    )
    unique_by_url: dict[str, DiscoverySearch] = {}
    for search in searches:
        unique_by_url.setdefault(search.url, search)
    return tuple(unique_by_url.values())[:limit]


def _translation_service(settings: Settings) -> TranslationService:
    provider = None
    if (
        settings.translation_enabled
        and settings.translation_provider == "google-cloud"
        and not settings.google_translation_api_key
    ):
        raise ValueError(
            "Google translation is enabled but "
            "JOBHUNTER_GOOGLE_TRANSLATION_API_KEY is not configured"
        )
    if settings.translation_enabled and settings.translation_provider == "lm-studio":
        provider = LMStudioTranslationProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.effective_translation_lm_studio_model(),
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
            max_tokens=settings.translation_lm_studio_max_tokens,
            request_character_target=settings.translation_lm_studio_character_target,
        )
    elif settings.translation_enabled and settings.translation_provider == "google-cloud":
        provider = GoogleCloudTranslationProvider(
            api_key=settings.google_translation_api_key or "",
            model=settings.google_translation_model,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
        )
    return TranslationService(
        store=TranslationStore(settings.database_path),
        provider=provider,
        target_language=settings.translation_target_language,
    )


def build_phase1_run_service(
    settings: Settings,
    *,
    request_budget: int,
) -> Phase1RunService:
    """Build the shared Phase-1 dependency graph with one consistent source policy."""

    if not 1 <= request_budget <= 500:
        raise ValueError("request budget must be between 1 and 500")

    client = JobinjaClient(
        user_agent=settings.jobinja_user_agent,
        timeout_seconds=settings.jobinja_request_timeout_seconds,
        max_retries=settings.jobinja_max_retries,
    )
    source_store = JobHunterStore(settings.database_path)
    observations = JobDetailObservationStore(settings.database_path)
    lifecycle = LifecycleStore(settings.database_path)
    detail_service = JobinjaDetailService(
        client=client,
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=source_store,
        observation_store=observations,
        lifecycle_store=lifecycle,
    )
    batch_service = JobinjaBatchFetchService(
        detail_service=detail_service,
        request_delay_seconds=settings.jobinja_request_delay_seconds,
    )
    discovery_service = JobinjaDiscoveryService(
        client=client,
        evidence_store=EvidenceStore(settings.evidence_dir),
        store=source_store,
        request_delay_seconds=settings.jobinja_request_delay_seconds,
        request_budget=request_budget,
    )
    sync_service = JobinjaSyncService(
        discovery_service=discovery_service,
        batch_service=batch_service,
        catalog=JobCatalog(settings.database_path),
        observations=observations,
        auditor=JobDetailAuditor(settings.database_path),
    )

    translation_store = TranslationStore(settings.database_path)
    translation_service = _translation_service(settings)
    analysis_store = AnalysisStore(settings.database_path)
    model = settings.effective_analysis_lm_studio_model()
    analysis_service = None
    if model:
        analysis_service = JobAnalysisService(
            source_store=translation_store,
            translation_service=translation_service,
            analysis_store=analysis_store,
            provider=LMStudioProvider(
                base_url=settings.lm_studio_base_url,
                configured_model=model,
                api_token=settings.lm_studio_api_token,
                timeout_seconds=settings.inference_timeout_seconds,
                max_retries=settings.inference_max_retries,
            ),
            model=model,
            max_tokens=settings.analysis_max_tokens,
        )

    return Phase1RunService(
        sync_service=sync_service,
        translation_service=translation_service,
        analysis_service=analysis_service,
        source_store=translation_store,
        analysis_store=analysis_store,
        workflow_store=JobWorkflowStore(settings.database_path),
        market_insights=MarketInsights(
            settings.database_path,
            analysis_model=model,
            analysis_prompt_version=PROMPT_VERSION,
            analysis_schema_version=ANALYSIS_SCHEMA_VERSION,
        ),
        translation_enabled=settings.translation_enabled,
        analysis_model=model,
    )


def _successful_detail_ids(summary: JobinjaSyncSummary) -> tuple[str, ...]:
    if summary.detail_fetch is None:
        return ()
    return tuple(result.source_job_id for result in summary.detail_fetch.results)


def format_phase1_run_summary(summary: Phase1RunSummary) -> str:
    """Render a complete run without hiding partial stage failures or Market scope."""

    sections = [
        "Complete JobHunter Phase-1 run",
        f"Run status: {summary.status}",
        "",
        format_sync_summary(summary.sync),
    ]

    if summary.translation is not None:
        sections.extend(["", format_translation_batch_summary(summary.translation)])
    else:
        sections.extend(
            [
                "",
                "English v2 stage",
                f"Skipped: {summary.translation_skipped_reason or 'not requested'}",
            ]
        )

    if summary.analysis is not None:
        sections.extend(["", format_analysis_batch_summary(summary.analysis)])
        if summary.analysis_eligible_before is not None:
            sections.append(
                f"Analysis eligible before this batch: {summary.analysis_eligible_before}"
            )
        if summary.analysis_remaining is not None:
            sections.append(f"Analysis remaining eligible: {summary.analysis_remaining}")
    else:
        sections.extend(
            [
                "",
                "Evidence-backed job analysis",
                f"Skipped: {summary.analysis_skipped_reason or 'not requested'}",
            ]
        )

    market = summary.market
    sections.extend(
        [
            "",
            "Current Market scope",
            f"Discovered Jobinja identities: {market.discovered_jobs}",
            f"Current parsed jobs: {market.current_parsed_jobs}",
            f"Current accepted analyses: {market.analyzed_jobs}",
            f"Distinct employers in analyzed sample: {market.distinct_employers}",
            f"Responsibility claims: {market.responsibility_claims}",
            f"Requirement claims: {market.requirement_claims}",
        ]
    )
    if market.sample_warning:
        sections.extend(["", f"Market sampling warning: {market.sample_warning}"])
    if market.concentration_warning:
        sections.extend(["", f"Market concentration warning: {market.concentration_warning}"])
    return "\n".join(sections)
