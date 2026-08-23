"""Neutral current-corpus report shared by the Phase-1 CLI and browser."""

from __future__ import annotations

from dataclasses import dataclass

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.job_workflow import JobWorkflowStore
from jobhunter.market_insights import MarketInsights, MarketSummary
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_service import TranslationService, build_translation_service
from jobhunter.translation_store import TranslationStore


@dataclass(frozen=True, slots=True)
class Phase1ReportRow:
    """Current dependency state for one parsed Jobinja posting."""

    source_job_id: str
    title: str
    triage_state: str
    job_detail_version_id: int
    source_language: str
    parser_version: str
    translation_artifact_id: int | None
    translation_identity: str | None
    analysis_artifact_id: int | None
    analysis_review_status: str
    capability_artifact_id: int | None
    chain_status: str


@dataclass(frozen=True, slots=True)
class Phase1Report:
    """Exact current-state counts, queues, and dependency lineages."""

    discovered_jobs: int
    current_parsed_jobs: int
    current_english_projections: int
    pending_english_analyses: int
    accepted_english_analyses: int
    current_capabilities: int
    analysis_model: str | None
    capability_model: str | None
    parser_versions: tuple[str, ...]
    translation_schema_version: str
    market: MarketSummary
    rows: tuple[Phase1ReportRow, ...]
    translation_missing: tuple[str, ...]
    analysis_ready: tuple[str, ...]
    analysis_pending_review: tuple[str, ...]
    capability_ready: tuple[str, ...]
    current_chains: tuple[str, ...]


class Phase1ReportService:
    """Read current artifact state without mutating source or model data."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        translation_service: TranslationService,
        analysis_store: AnalysisStore,
        capability_store: CapabilityIntelligenceStore,
        workflow_store: JobWorkflowStore,
        market_insights: MarketInsights,
        analysis_model: str | None,
        capability_model: str | None,
    ) -> None:
        self._source_store = source_store
        self._translation_service = translation_service
        self._analysis_store = analysis_store
        self._capability_store = capability_store
        self._workflow_store = workflow_store
        self._market_insights = market_insights
        self._analysis_model = analysis_model
        self._capability_model = capability_model

    def build(self) -> Phase1Report:
        market = self._market_insights.market_summary()
        rows: list[Phase1ReportRow] = []
        translation_missing: list[str] = []
        analysis_ready: list[str] = []
        pending_review: list[str] = []
        capability_ready: list[str] = []
        current_chains: list[str] = []

        for source in self._source_store.latest_source_versions(limit=5000):
            job_id = source.source_job_id
            workflow = self._workflow_store.get_state(job_id)
            translation = self._translation_service.current_artifact(job_id)
            analysis = None
            if translation is not None and self._analysis_model is not None:
                analysis = self._analysis_store.find_artifact(
                    job_detail_version_id=source.job_detail_version_id,
                    translation_artifact_id=translation.id,
                    require_translation_dependency=True,
                    model=self._analysis_model,
                    prompt_version=ENGLISH_PROMPT_VERSION,
                    schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
                )

            capability = None
            if (
                analysis is not None
                and analysis.semantic_review_status == "accepted"
                and self._capability_model is not None
            ):
                capability = self._capability_store.find_artifact(
                    job_detail_version_id=source.job_detail_version_id,
                    translation_artifact_id=translation.id,
                    analysis_artifact_id=analysis.id,
                    model=self._capability_model,
                    prompt_version=CAPABILITY_PROMPT_VERSION,
                    schema_version=CAPABILITY_SCHEMA_VERSION,
                )

            if translation is None:
                chain_status = "translation_missing"
                translation_missing.append(job_id)
            elif analysis is None:
                chain_status = (
                    "analysis_ready"
                    if self._analysis_model is not None
                    and workflow.triage_state != "not_relevant"
                    else "analysis_not_selected"
                )
                if chain_status == "analysis_ready":
                    analysis_ready.append(job_id)
            elif analysis.semantic_review_status == "pending":
                chain_status = "analysis_pending_review"
                pending_review.append(job_id)
            elif capability is None:
                chain_status = (
                    "capability_ready"
                    if self._capability_model is not None
                    else "capability_not_configured"
                )
                if chain_status == "capability_ready":
                    capability_ready.append(job_id)
            else:
                chain_status = "current"
                current_chains.append(job_id)

            title = str(source.fields.get("title") or job_id).strip() or job_id
            translation_identity = None
            if translation is not None:
                translation_identity = (
                    f"{translation.provider_name}/{translation.provider_model} / "
                    f"{translation.translation_schema_version}"
                )
            rows.append(
                Phase1ReportRow(
                    source_job_id=job_id,
                    title=title,
                    triage_state=workflow.triage_state,
                    job_detail_version_id=source.job_detail_version_id,
                    source_language=source.source_language,
                    parser_version=str(
                        source.fields.get("parser_version") or "unknown"
                    ),
                    translation_artifact_id=(translation.id if translation else None),
                    translation_identity=translation_identity,
                    analysis_artifact_id=(analysis.id if analysis else None),
                    analysis_review_status=(
                        analysis.semantic_review_status if analysis else "missing"
                    ),
                    capability_artifact_id=(capability.id if capability else None),
                    chain_status=chain_status,
                )
            )

        return Phase1Report(
            discovered_jobs=market.discovered_jobs,
            current_parsed_jobs=len(rows),
            current_english_projections=sum(
                row.translation_artifact_id is not None for row in rows
            ),
            pending_english_analyses=len(pending_review),
            accepted_english_analyses=sum(
                row.analysis_review_status == "accepted" for row in rows
            ),
            current_capabilities=sum(
                row.capability_artifact_id is not None for row in rows
            ),
            analysis_model=self._analysis_model,
            capability_model=self._capability_model,
            parser_versions=tuple(sorted({row.parser_version for row in rows})),
            translation_schema_version=TRANSLATION_SCHEMA_VERSION,
            market=market,
            rows=tuple(rows),
            translation_missing=tuple(translation_missing),
            analysis_ready=tuple(analysis_ready),
            analysis_pending_review=tuple(pending_review),
            capability_ready=tuple(capability_ready),
            current_chains=tuple(current_chains),
        )


def build_phase1_report_service(settings: Settings) -> Phase1ReportService:
    """Build the shared read-only report from configured public-current identities."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    capability_model = settings.effective_capability_lm_studio_model()
    return Phase1ReportService(
        source_store=TranslationStore(settings.database_path),
        translation_service=build_translation_service(settings),
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        workflow_store=JobWorkflowStore(settings.database_path),
        market_insights=MarketInsights(
            settings.database_path,
            analysis_model=analysis_model,
            analysis_prompt_version=ENGLISH_PROMPT_VERSION,
            analysis_schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            translation_service=build_translation_service(settings),
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
    )


def format_phase1_report(report: Phase1Report) -> str:
    """Render a deterministic report suitable for rerun comparison."""

    lines = [
        "JobHunter current Phase-1 report",
        "",
        "Current corpus",
        f"Discovered Jobinja identities: {report.discovered_jobs}",
        f"Current parsed jobs: {report.current_parsed_jobs}",
        f"Current effective English projections: {report.current_english_projections}",
        f"Pending English P1.6 review: {report.pending_english_analyses}",
        f"Accepted current English P1.6: {report.accepted_english_analyses}",
        f"Current Capability chains: {report.current_capabilities}",
        "",
        "Configured contracts",
        f"Parser versions: {', '.join(report.parser_versions) or 'none'}",
        f"English projection: {report.translation_schema_version}",
        f"Analysis model: {report.analysis_model or 'not configured'}",
        f"English P1.6: {ENGLISH_PROMPT_VERSION} / {ENGLISH_ANALYSIS_SCHEMA_VERSION}",
        f"Capability model: {report.capability_model or 'not configured'}",
        f"Capability: {CAPABILITY_PROMPT_VERSION} / {CAPABILITY_SCHEMA_VERSION}",
        "",
        "Action queues",
        _queue_line("Translation missing", report.translation_missing),
        _queue_line("Analysis ready", report.analysis_ready),
        _queue_line("Analysis pending review", report.analysis_pending_review),
        _queue_line("Capability ready", report.capability_ready),
        "",
        "Current Market scope",
        f"Accepted analyzed jobs: {report.market.analyzed_jobs}",
        f"Source scope: {report.market.source_scope}",
        f"Filter scope: {report.market.filter_scope}",
        f"Duplicate adjustment: {report.market.duplicate_adjustment}",
        (
            "Sampling warning: "
            f"{report.market.sample_warning or 'none'}"
        ),
        (
            "Concentration warning: "
            f"{report.market.concentration_warning or 'none'}"
        ),
        "",
        f"Current accepted chains ({len(report.current_chains)})",
    ]
    current_rows = {
        row.source_job_id: row
        for row in report.rows
        if row.source_job_id in report.current_chains
    }
    if not report.current_chains:
        lines.append("none")
    else:
        for job_id in report.current_chains:
            row = current_rows[job_id]
            lines.append(
                f"{job_id}: detail={row.job_detail_version_id}, "
                f"translation={row.translation_artifact_id}, "
                f"p16={row.analysis_artifact_id}, "
                f"capability={row.capability_artifact_id}"
            )
    return "\n".join(lines)


def _queue_line(label: str, job_ids: tuple[str, ...]) -> str:
    values = ", ".join(job_ids) if job_ids else "none"
    return f"{label} ({len(job_ids)}): {values}"
