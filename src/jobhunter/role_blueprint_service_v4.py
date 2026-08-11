"""Role Capability Blueprint v4 service with deterministic provenance attachment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.role_blueprint_inference_v4 import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_store import RoleBlueprintArtifact, RoleBlueprintStore
from jobhunter.role_blueprint_v4_models import RoleBlueprintDraft, reconcile_role_blueprint_v4
from jobhunter.translation_store import TranslationStore

BLUEPRINT_PROMPT_VERSION = "role-capability-blueprint-v4"
BLUEPRINT_SCHEMA_VERSION = "role-capability-blueprint-v3"

_SYSTEM_PROMPT = """You are JobHunter's senior practitioner/domain-specialist role analyst.

MISSION
Explain what this position probably requires in practice. Use the professional frame that matches
the vacancy. Add useful practitioner interpretation beyond the accepted factual and Capability
layers without pretending that professional inference is employer fact.

V4 RESPONSIBILITY BOUNDARY
JobHunter, not you, owns all provenance bookkeeping. Do NOT emit source indices, requirement
indices, responsibility indices, source strength fields, source depth fields, or source-role
constraints. JobHunter attaches those deterministically after generation.

CAPABILITY ORDER
The request supplies accepted Capability profiles in a fixed order. Return EXACTLY one
capability_interpretations item per supplied profile, in exactly the same order. Interpret each
profile; do not regroup, merge, split, rename, or create extra curriculum areas. The persisted
Blueprint receives the authoritative Capability label and source links mechanically.

SOURCE FACTS VS CAPABILITY REASONING
Within each supplied capability:
- source_requirements and source_responsibilities are authoritative employer facts;
- requirement_type and depth_signal are authoritative when present;
- capability_reasoning is accepted machine reasoning above those facts, not new employer truth.
When they differ in strength, source facts win.

OPTIONALITY AND DEPTH
Preserve required/preferred/contextual/inferred distinctions. Contextual or preferred technology
must not become mandatory because it appears beside required work. Explicit depth applies only to
the exact source concept that carries it. Do not spread Python expert depth, for example, to ML
frameworks or neighboring tools.

SUGGESTED TOOLS
suggested_tools_or_examples is ONLY for practitioner-created examples not already named by the
source facts. Use likely_example or possible_example. They are not employer requirements and must
not be called required, mandatory, necessary, expert-level, or mastery expectations. If a tool is
already source-named, explain its practical relevance in the capability prose if useful; do not
re-add it as a suggested tool.

HIDDEN REQUIREMENTS
These are model-created professional inferences, never employer facts. v4 intentionally allows
only plausible or speculative strength. Prefer a small number of defensible insights over generic
curriculum prerequisites.

PROFESSIONAL EXAMPLE SCENARIOS
All generated scenarios are illustrative professional examples, not claims about the employer's
actual architecture. They can only be plausible or speculative. Do not infer that a list of Kafka,
Spark, Airflow, MLflow, Docker, cloud, edge, MES, databases, or frameworks forms one deployed
system. When a useful example chooses topology, latency, vendor, batch/stream mode, cloud/edge
placement, scale, ownership, orchestration, or feedback-loop behavior that is not source-stated,
put that choice in assumptions and write it as one possible implementation.

TECHNICAL CORRECTNESS
Keep normal technical meanings and boundaries. Spark and Kafka are not interchangeable.
Airflow/Prefect are workflow orchestrators, not streaming engines. MES/SECS-GEM references do not
prove a specific data path. Cloud names do not prove cloud deployment. Edge being a plus does not
prove edge inference. "Move models toward production" does not prove microservices, CI/CD, model
registries, real-time control loops, or autonomous feedback.

EVIDENCE DENSITY
Sparse evidence should yield fewer strong claims and more unknowns. Rich evidence may support
deeper interpretation, but detail is not permission to invent company architecture.

ROLE-LEVEL CONSTRAINTS
The request may show deterministic degree/experience constraints for context. Do not transform
them into new inferred capabilities. JobHunter copies them into the final Blueprint exactly.

OUTPUT
Write for a technically curious human. Describe the job, not the reader's readiness. Explain
practical depth, useful subskills, likely work products, operational concerns, probable
non-requirements, and important unknowns. Do not create a personalized learning plan.
"""

_ROLE_CONTEXT_KEYS = (
    "title",
    "company",
    "company_name",
    "location",
    "job_location",
    "employment_type",
    "work_type",
    "seniority",
    "category",
    "industry",
    "company_description",
)
_REASONING_KEYS = (
    "sub_capabilities",
    "underlying_knowledge",
    "operational_practices",
    "operational_context",
    "unknown_scope",
)


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


def _compact_role_context(fields: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in _ROLE_CONTEXT_KEYS:
        if key not in fields:
            continue
        value = fields[key]
        if value is None or value == "" or value == []:
            continue
        result[key] = value
    return result


def _reasoning_projection(profile: dict[str, Any]) -> dict[str, Any]:
    projected: dict[str, Any] = {"summary": str(profile.get("summary") or "")}
    for key in _REASONING_KEYS:
        raw = profile.get(key) or []
        if not isinstance(raw, list):
            projected[key] = []
            continue
        projected[key] = [
            {
                "statement": str(item.get("statement") or ""),
                "evidence_status": str(item.get("evidence_status") or ""),
                "confidence": str(item.get("confidence") or ""),
            }
            for item in raw
            if isinstance(item, dict) and str(item.get("statement") or "").strip()
        ]
    return projected


def _source_requirement_projection(requirement: dict[str, Any]) -> dict[str, Any]:
    return {
        "concept": str(requirement.get("concept") or ""),
        "concept_type": str(requirement.get("concept_type") or ""),
        "requirement_type": str(requirement.get("requirement_type") or ""),
        "depth_signal": requirement.get("depth_signal"),
    }


def _source_responsibility_projection(responsibility: dict[str, Any]) -> dict[str, Any]:
    return {"statement": str(responsibility.get("statement") or "")}


def _blueprint_inputs(
    *,
    analysis_fields: dict[str, Any],
    capability_intelligence: dict[str, Any],
) -> dict[str, Any]:
    source_truth = capability_intelligence.get("source_truth")
    if not isinstance(source_truth, dict):
        raise RoleBlueprintError("Blueprint v4 requires accepted Capability v7 source truth")
    requirements = list(source_truth.get("requirements") or [])
    responsibilities = list(source_truth.get("responsibilities") or [])
    capability_profiles = list(capability_intelligence.get("capabilities") or [])
    if not capability_profiles:
        raise RoleBlueprintError("Blueprint v4 requires at least one accepted Capability profile")

    capabilities: list[dict[str, Any]] = []
    for profile in capability_profiles:
        if not isinstance(profile, dict):
            raise RoleBlueprintError("Accepted Capability profile is not an object")
        requirement_facts: list[dict[str, Any]] = []
        for index in profile.get("source_requirement_indices") or []:
            if not isinstance(index, int) or not 0 <= index < len(requirements):
                raise RoleBlueprintError("Accepted Capability contains invalid requirement links")
            requirement = requirements[index]
            if isinstance(requirement, dict):
                requirement_facts.append(_source_requirement_projection(requirement))

        responsibility_facts: list[dict[str, Any]] = []
        for index in profile.get("source_responsibility_indices") or []:
            if not isinstance(index, int) or not 0 <= index < len(responsibilities):
                raise RoleBlueprintError(
                    "Accepted Capability contains invalid responsibility links"
                )
            responsibility = responsibilities[index]
            if isinstance(responsibility, dict):
                responsibility_facts.append(_source_responsibility_projection(responsibility))

        capabilities.append(
            {
                "capability_label": str(profile.get("capability_label") or ""),
                "source_requirements": requirement_facts,
                "source_responsibilities": responsibility_facts,
                "capability_reasoning": _reasoning_projection(profile),
            }
        )

    role_constraints: list[dict[str, Any]] = []
    for index in source_truth.get("role_level_requirement_indices") or []:
        if not isinstance(index, int) or not 0 <= index < len(requirements):
            raise RoleBlueprintError("Capability source truth contains invalid role constraint")
        requirement = requirements[index]
        if isinstance(requirement, dict):
            role_constraints.append(_source_requirement_projection(requirement))

    role_purpose = [
        str(item.get("statement") or "")
        for item in source_truth.get("role_purpose") or []
        if isinstance(item, dict) and str(item.get("statement") or "").strip()
    ]
    return {
        "role_context": _compact_role_context(analysis_fields),
        "role_purpose": role_purpose,
        "role_level_constraints": role_constraints,
        "capabilities": capabilities,
    }


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
                "Blueprint v4 requires accepted Capability v7 source truth; rebuild Capability"
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

        user_payload = {
            "source_job_id": source_job_id,
            "blueprint_inputs": _blueprint_inputs(
                analysis_fields=translation.fields,
                capability_intelligence=capability.intelligence,
            ),
            "contract": {
                "prompt_version": BLUEPRINT_PROMPT_VERSION,
                "schema_version": BLUEPRINT_SCHEMA_VERSION,
                "capability_artifact_id": capability.id,
                "capability_interpretation_count": len(
                    capability.intelligence.get("capabilities") or []
                ),
                "deterministic_reconciliation": (
                    "JobHunter attaches Capability identity/coverage, P1.6 source requirements "
                    "and responsibilities, and role-level constraints after generation."
                ),
            },
        }

        try:
            inference = self._provider.complete(
                system_prompt=_SYSTEM_PROMPT,
                user_payload=user_payload,
                max_tokens=self._max_tokens,
            )
            draft = RoleBlueprintDraft.model_validate(inference.blueprint)
            reconciled = reconcile_role_blueprint_v4(
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
                f"Capability link: {area.get('source_capability_index')}",
                f"Interpretation: {area.get('interpretation_strength', '?')}",
                f"Likely depth: {area.get('likely_depth', '')}",
                f"Why it matters: {area.get('why_this_matters', '')}",
            ]
        )
        source_requirements = area.get("source_requirements") or []
        if source_requirements:
            lines.append("Source requirements:")
            for item in source_requirements:
                depth = item.get("depth_signal")
                suffix = f"; depth={depth}" if depth else ""
                lines.append(
                    f"- P1.6 requirement {item.get('requirement_index')}: "
                    f"{item.get('concept')} ({item.get('requirement_type')}{suffix})"
                )
        for tool in area.get("suggested_tools_or_examples") or []:
            lines.append(
                f"Suggested tool/example: {tool.get('name')} [{tool.get('relationship')}]"
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

    scenarios = data.get("professional_example_scenarios") or []
    if scenarios:
        lines.extend(["", "Professional example scenarios"])
        for scenario in scenarios:
            lines.append(
                f"- {scenario.get('name')} [{scenario.get('interpretation_strength')}; "
                "professional_example]"
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
