"""Role Capability Blueprint v6 with source truth plus explicitly uncertain inference."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service_v7 import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.config import Settings
from jobhunter.role_blueprint_inference_v6 import RoleBlueprintInferenceProvider
from jobhunter.role_blueprint_store import RoleBlueprintArtifact, RoleBlueprintStore
from jobhunter.role_blueprint_v6_models import RoleBlueprintDraft, reconcile_role_blueprint_v6
from jobhunter.translation_store import TranslationStore

BLUEPRINT_PROMPT_VERSION = "role-capability-blueprint-v6"
BLUEPRINT_SCHEMA_VERSION = "role-capability-blueprint-v5"

_SYSTEM_PROMPT = """You are JobHunter's senior practitioner/domain-specialist role analyst.

MISSION
Add a small amount of useful professional context above accepted employer facts without inventing
an employer architecture, ownership model, topology, latency requirement, deployment pattern, or
candidate obligation.

V6 TRUST BOUNDARY
JobHunter separately displays all authoritative role purpose, requirements, responsibilities,
obligation strength, explicit depth, evidence, and role-level constraints. You do not summarize or
rewrite the role. You only provide bounded professional considerations and explicit unknowns.

CAPABILITY ORDER
The request supplies accepted Capability profiles in fixed order. Return EXACTLY one
capability_interpretations item per supplied Capability, in exactly that order. Do not regroup,
merge, split, rename, or create additional capability areas.

MODEL OUTPUT SURFACE
For each Capability you may produce:
- zero to four professional_considerations;
- one or more important_unknowns.
There is deliberately no free-form role summary, role shape, likely depth, architecture scenario,
hidden requirement, tool recommendation, work-product list, or bottom-line field.

PROFESSIONAL CONSIDERATIONS
Use a consideration only when it adds material practitioner value beyond rereading the source
facts. Each consideration is professional inference, never employer fact, and MUST include:
- interpretation_strength = plausible or speculative;
- uncertainty = one concrete sentence saying what the vacancy does not establish.
Do not use mandatory/required/must/necessary/expected-to/responsible-for wording for model-created
claims. Do not describe full/end-to-end lifecycle, stack, pipeline, system, or infrastructure scope.

SOURCE OPTIONALITY AND DEPTH
Treat requirement_type and depth_signal as authoritative source metadata. Contextual technology is
not mandatory. Preferred technology is not required. Explicit depth belongs only to the exact
source concept carrying it. Do not spread depth across neighboring tools.

TECHNOLOGY-LIST RULE
A technology list is not an architecture. Named frameworks, platforms, databases, orchestration,
cloud/edge tools, protocols, or MLOps tools may be alternatives, adjacent skills, or context. Do
not combine them into an unstated deployed system or imply a particular data-flow topology.

OPERATING-MODE RULE
Do not infer streaming from high-volume data, real-time behavior from process-control work,
low-latency requirements from anomaly detection, automated feedback from APC/SPC terminology,
cloud/edge placement from platform names, or lifecycle ownership from deployment/governance work.
If such a topic is professionally relevant, express it only as an unknown or a bounded
consideration with explicit uncertainty.

DOMAIN RULE
Do not invent process/equipment physics, regulatory requirements, CI/CD, microservices, model
registries, autonomous control loops, or other unstated candidate obligations.

UNKNOWNS
Every Capability MUST contain at least one important_unknown. Prefer material unresolved questions
about exact tool usage, deployment boundary, ownership, batch-vs-stream mode, latency, operational
scale, interfaces, or other facts not established by the vacancy. Unknowns must not themselves
smuggle in an assumption (for example, do not say 'the feedback loop latency is unknown' unless a
feedback loop is source-established; say 'whether any automated feedback loop exists is unknown').

OUTPUT
Describe professional considerations around the role, not the user's readiness. Do not create a
curriculum, learning plan, application advice, or architecture design.
"""

_ROLE_CONTEXT_KEYS = (
    "title",
    "location",
    "job_location",
    "employment_type",
    "work_type",
    "seniority",
    "category",
    "industry",
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
        raise RoleBlueprintError("Blueprint v6 requires accepted Capability v7 source truth")
    requirements = list(source_truth.get("requirements") or [])
    responsibilities = list(source_truth.get("responsibilities") or [])
    capability_profiles = list(capability_intelligence.get("capabilities") or [])
    if not capability_profiles:
        raise RoleBlueprintError("Blueprint v6 requires at least one accepted Capability profile")

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
        "source_role_purpose": role_purpose,
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
        max_tokens: int = 4096,
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
                "Blueprint v6 requires accepted Capability v7 source truth; rebuild Capability"
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
                "trust_boundary": (
                    "Model output contains only explicitly uncertain professional "
                    "considerations and unknowns. JobHunter owns all accepted source facts "
                    "and Capability identity."
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
            reconciled = reconcile_role_blueprint_v6(
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
        max_tokens=min(settings.analysis_max_tokens, 4096),
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
        "Source role purpose",
    ]
    purposes = data.get("source_role_purpose") or []
    if not purposes:
        lines.append("- none")
    else:
        lines.extend(f"- {item.get('statement')}" for item in purposes)

    lines.extend(["", "Source role constraints"])
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

    for index, area in enumerate(data.get("capability_areas") or [], start=1):
        lines.extend(
            [
                "",
                f"Area {index}: {area.get('name', '(unnamed)')}",
                f"Capability link: {area.get('source_capability_index')}",
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
        source_responsibilities = area.get("source_responsibilities") or []
        if source_responsibilities:
            lines.append("Source responsibilities:")
            for item in source_responsibilities:
                lines.append(
                    f"- P1.6 responsibility {item.get('responsibility_index')}: "
                    f"{item.get('statement')}"
                )
        considerations = area.get("professional_considerations") or []
        if considerations:
            lines.append("Professional considerations [inference, not employer fact]:")
            for item in considerations:
                lines.append(
                    f"- [{item.get('interpretation_strength')}] {item.get('statement')}"
                )
                lines.append(f"  Uncertainty: {item.get('uncertainty')}")
        unknowns = area.get("important_unknowns") or []
        lines.append("Important unknowns:")
        lines.extend(f"- {value}" for value in unknowns)

    overall_unknowns = data.get("overall_unknowns") or []
    if overall_unknowns:
        lines.extend(["", "Whole-role unknowns"])
        lines.extend(f"- {value}" for value in overall_unknowns)
    return "\n".join(lines)
