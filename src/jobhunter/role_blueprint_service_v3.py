"""Role Capability Blueprint v3 service with deterministic upstream grounding."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.role_blueprint_inference import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_models import RoleCapabilityBlueprint, reconcile_role_blueprint
from jobhunter.role_blueprint_store import RoleBlueprintArtifact, RoleBlueprintStore
from jobhunter.translation_store import TranslationStore

BLUEPRINT_PROMPT_VERSION = "role-capability-blueprint-v3"
BLUEPRINT_SCHEMA_VERSION = "role-capability-blueprint-v2"

_SYSTEM_PROMPT = """You are JobHunter's senior practitioner/domain-specialist role analyst.

MISSION
Explain what this position probably requires in practice. Use the professional frame that matches
this vacancy. Add useful practitioner interpretation without rewriting the advertisement.

UPSTREAM AUTHORITY
The request contains accepted P1.6 employer facts and accepted Capability v7 reasoning. Those
upstream layers remain authoritative for source facts, requirement strength, explicit depth,
responsibilities, role-level qualifications, and provenance. Do not overwrite them.

BLUEPRINT V3 GROUNDING
Every capability area MUST include source_capability_indices using zero-based indices into the
supplied capability_intelligence.capabilities array. Across all areas, cover every accepted
Capability profile at least once. Do not create an ungrounded generic curriculum area.

SOURCE-NAMED TOOLS
A tool is source_named only when the supplied P1.6 facts actually name it. For source_named tools,
link the supporting accepted P1.6 requirement/responsibility indices. Leave
source_requirement_strength as unspecified and source_depth_signals empty; JobHunter fills those
mechanically after generation. Do not spread one tool's explicit depth to neighboring tools.

For likely_example or possible_example tools, leave all source indices empty. These are practitioner
examples, not employer requirements, and must never be described as mandatory or necessary.

OPTIONALITY
Preserve required/preferred/contextual/inferred distinctions. A source-named contextual or
preferred technology is not converted into a mandatory technology by appearing in a Blueprint.
The global idea that depth in a core stack matters does not prove mastery of every named framework.

HIDDEN REQUIREMENTS
Hidden requirements are derived practitioner conclusions, not new employer facts. If one is
highly_likely, link the accepted Capability profiles and/or responsibilities that make it strong.
Use plausible when credible alternatives or material unknowns remain.

END-TO-END SCENARIOS
Every scenario must declare scenario_basis:
- source_stated_workflow: use only when the vacancy itself establishes the workflow/sequence;
- professional_example: a coherent practitioner-created example used to explain likely work.

Professional examples can be plausible or speculative but NEVER highly_likely. Do not assemble a
technology list into a claimed company architecture. If an example depends on assumptions about
latency, topology, vendors, batch/streaming mode, cloud/edge placement, data scale, or ownership,
state those assumptions explicitly. A highly_likely scenario cannot depend on unresolved
assumptions.

TECHNICAL CORRECTNESS
Keep normal technical meanings. Spark and Kafka are not interchangeable. Airflow/Prefect do not
become streaming engines. A technology list does not establish runtime topology. Prefer coherent,
defensible alternatives over sophisticated-looking invented architecture.

EVIDENCE DENSITY
Sparse advertisements should produce fewer strong claims and more unknowns. Rich advertisements
may support deeper interpretation. Do not manufacture the same detail for both.

ROLE-LEVEL CONSTRAINTS
Do not invent or restate degree/experience constraints as model inference. JobHunter deterministically
copies role-level P1.6 constraints into the persisted Blueprint after generation.

OUTPUT
Write for a technically curious human. Explain what the person would probably need to be able to
do, what work products and failure modes matter, and what does not matter. Preserve uncertainty.
Describe the JOB, not the reader's readiness, and do not create a personalized learning plan.
"""


class RoleBlueprintError(ValueError):
    """Raised when a job is not ready for the human-facing Blueprint layer."""


@dataclass(frozen=True, slots=True)
class RoleBlueprintResult:
    source_job_id: str
    artifact_id: int
    outcome: str
    model: str
    capability_areas: int
    capability_artifact_id: int


class RoleBlueprintService:
    def __init__(
        self,
        *,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        capability_store: CapabilityIntelligenceStore,
        blueprint_store: RoleBlueprintStore,
        provider: RoleBlueprintInferenceProvider,
        analysis_model: str,
        capability_model: str,
        blueprint_model: str,
        max_tokens: int = 8192,
        clock=lambda: datetime.now(UTC),
    ) -> None:
        self._source_store = source_store
        self._analysis_store = analysis_store
        self._capability_store = capability_store
        self._blueprint_store = blueprint_store
        self._provider = provider
        self._analysis_model = analysis_model.strip()
        self._capability_model = capability_model.strip()
        self._blueprint_model = blueprint_model.strip()
        self._max_tokens = max_tokens
        self._clock = clock
        if not self._analysis_model or not self._capability_model or not self._blueprint_model:
            raise ValueError("Concrete analysis/capability/blueprint model identities are required")

    def _dependencies(self, source_job_id: str):
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise RoleBlueprintError("Job has no current successfully parsed source version")

        analysis = self._analysis_store.latest_current(
            source_job_id,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        if analysis is None:
            raise RoleBlueprintError(
                "Run Analyze English before building a Role Capability Blueprint"
            )

        capability = self._capability_store.latest_current(
            source_job_id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if capability is None:
            raise RoleBlueprintError(
                "Build current Capability Intelligence before building a Role Capability Blueprint"
            )
        if capability.job_detail_version_id != source.job_detail_version_id:
            raise RoleBlueprintError(
                "Capability Intelligence is stale for the current source version"
            )
        if capability.analysis_artifact_id != analysis.id:
            raise RoleBlueprintError(
                "Capability Intelligence is stale for the current English analysis"
            )
        if analysis.translation_artifact_id is None:
            raise RoleBlueprintError("English analysis does not reference an English projection")
        if capability.translation_artifact_id != analysis.translation_artifact_id:
            raise RoleBlueprintError(
                "Capability Intelligence and English analysis disagree on projection provenance"
            )
        if not isinstance(capability.intelligence.get("source_truth"), dict):
            raise RoleBlueprintError(
                "Blueprint v3 requires accepted Capability v7 source truth; rebuild Capability"
            )

        translation = self._capability_store.translation_dependency(
            capability.translation_artifact_id
        )
        if translation is None:
            raise RoleBlueprintError(
                "Capability Intelligence references a missing English projection"
            )
        if translation.job_detail_version_id != source.job_detail_version_id:
            raise RoleBlueprintError(
                "Referenced English projection is stale for the current source version"
            )
        return source, translation, analysis, capability

    @staticmethod
    def _analysis_fields(fields: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in fields.items()
            if key not in {"language", "parser_version"}
        }

    def build(self, source_job_id: str) -> RoleBlueprintResult:
        source, translation, analysis, capability = self._dependencies(source_job_id)
        attempted_at = self._clock()

        existing = self._blueprint_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            capability_artifact_id=capability.id,
            model=self._blueprint_model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        if existing is not None:
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, "reused")

        analysis_fields = self._analysis_fields(translation.fields)
        user_payload = {
            "source_job_id": source_job_id,
            "analysis_fields": analysis_fields,
            "accepted_extraction": analysis.analysis,
            "capability_intelligence": capability.intelligence,
            "contract": {
                "prompt_version": BLUEPRINT_PROMPT_VERSION,
                "schema_version": BLUEPRINT_SCHEMA_VERSION,
                "capability_artifact_id": capability.id,
                "deterministic_reconciliation": (
                    "JobHunter validates Capability/P1.6 links, preserves source tool strength/depth, "
                    "injects role-level constraints, and enforces scenario certainty boundaries."
                ),
            },
        }

        try:
            inference = self._provider.complete(
                system_prompt=_SYSTEM_PROMPT,
                user_payload=user_payload,
                max_tokens=self._max_tokens,
            )
            draft = RoleCapabilityBlueprint.model_validate(inference.blueprint)
            reconciled = reconcile_role_blueprint(
                draft,
                accepted_extraction=analysis.analysis,
                capability_intelligence=capability.intelligence,
            )
            blueprint = reconciled.model_dump(mode="json")
            artifact_id = self._blueprint_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=inference.model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                blueprint=blueprint,
                request_body=inference.request_body,
                raw_response=inference.raw_response,
                created_at=attempted_at,
            )
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

        artifact = self._blueprint_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            capability_artifact_id=capability.id,
            model=self._blueprint_model,
            prompt_version=BLUEPRINT_PROMPT_VERSION,
            schema_version=BLUEPRINT_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Role Capability Blueprint disappeared after persistence")
        return _result(artifact, "completed")


def build_role_blueprint_service(settings: Settings) -> RoleBlueprintService:
    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No LM Studio analysis model is configured")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    blueprint_model = settings.effective_blueprint_lm_studio_model()
    if not blueprint_model:
        raise ValueError("No LM Studio Role Capability Blueprint model is configured")

    return RoleBlueprintService(
        source_store=TranslationStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        blueprint_store=RoleBlueprintStore(settings.database_path),
        provider=RoleBlueprintInferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=blueprint_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
        blueprint_model=blueprint_model,
        max_tokens=settings.analysis_max_tokens,
    )


def _result(artifact: RoleBlueprintArtifact, outcome: str) -> RoleBlueprintResult:
    return RoleBlueprintResult(
        source_job_id=artifact.source_job_id,
        artifact_id=artifact.id,
        outcome=outcome,
        model=artifact.model,
        capability_areas=len(artifact.blueprint.get("capability_areas") or []),
        capability_artifact_id=artifact.capability_artifact_id,
    )


def format_role_blueprint(artifact: RoleBlueprintArtifact) -> str:
    data = artifact.blueprint
    lines = [
        f"Role Capability Blueprint for {artifact.source_job_id}",
        f"Model: {artifact.model}",
        f"Contract: {artifact.prompt_version} / {artifact.schema_version}",
        f"Capability artifact: {artifact.capability_artifact_id}",
        "",
        "Source role constraints",
    ]
    constraints = data.get("source_role_constraints") or []
    if not constraints:
        lines.append("- none")
    for item in constraints:
        depth = item.get("depth_signal")
        suffix = f"; depth={depth}" if depth else ""
        lines.append(
            f"- P1.6 requirement {item.get('requirement_index')}: "
            f"{item.get('concept')} ({item.get('requirement_type')}{suffix})"
        )

    lines.extend(
        [
            "",
            "What this role probably is in practice",
            str(data.get("role_read") or ""),
            "",
            "Likely role shape",
            str(data.get("likely_role_shape") or ""),
        ]
    )

    for index, area in enumerate(data.get("capability_areas") or [], start=1):
        lines.extend(
            [
                "",
                f"Area {index}: {area.get('name', '(unnamed)')}",
                f"Capability links: {area.get('source_capability_indices') or []}",
                f"Interpretation: {area.get('interpretation_strength', '?')}",
                f"Likely depth: {area.get('likely_depth', '')}",
                f"Why it matters: {area.get('why_this_matters', '')}",
            ]
        )
        for tool in area.get("likely_tools_or_examples") or []:
            lines.append(
                "Tool/example: "
                f"{tool.get('name')} [{tool.get('relationship')}; "
                f"strength={tool.get('source_requirement_strength', 'unspecified')}; "
                f"depth={tool.get('source_depth_signals') or []}]"
            )
        for label, key in (
            ("Likely subskills", "likely_subskills"),
            ("Likely work products", "likely_work_products"),
            ("Operational concerns", "likely_failure_modes_or_operational_concerns"),
            ("Probably not required", "probably_not_required"),
        ):
            values = area.get(key) or []
            if values:
                lines.append(f"{label}:")
                lines.extend(f"- {value}" for value in values)

    scenarios = data.get("likely_end_to_end_scenarios") or []
    if scenarios:
        lines.extend(["", "End-to-end scenarios"])
        for scenario in scenarios:
            lines.append(
                f"- {scenario.get('name')} "
                f"[{scenario.get('interpretation_strength')}; {scenario.get('scenario_basis')}]"
            )
            assumptions = scenario.get("assumptions") or []
            if assumptions:
                lines.append(f"  Assumptions: {assumptions}")

    unknowns = data.get("important_unknowns") or []
    if unknowns:
        lines.extend(["", "Important unknowns"])
        lines.extend(f"- {value}" for value in unknowns)

    lines.extend(["", "Bottom line", str(data.get("bottom_line") or "")])
    return "\n".join(lines)
