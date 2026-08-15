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


def _source_truth_payload(intelligence: dict[str, Any]) -> dict[str, Any]:
    source_truth = intelligence.get("source_truth") or {}
    if not isinstance(source_truth, dict):
        raise RoleBlueprintError("Capability source_truth is not an object")
    return {
        "role_purpose": source_truth.get("role_purpose") or [],
        "requirements": source_truth.get("requirements") or [],
        "responsibilities": source_truth.get("responsibilities") or [],
        "capability_requirement_indices": source_truth.get("capability_requirement_indices") or [],
        "role_level_requirement_indices": source_truth.get("role_level_requirement_indices") or [],
        "linked_requirement_indices": source_truth.get("linked_requirement_indices") or [],
        "linked_responsibility_indices": source_truth.get("linked_responsibility_indices") or [],
        "explicit_depth_requirement_indices": source_truth.get("explicit_depth_requirement_indices") or [],
    }


def _capability_payload(capability: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "capability_index": index,
        "capability_label": capability.get("capability_label"),
        "source_requirement_indices": capability.get("source_requirement_indices") or [],
        "source_responsibility_indices": capability.get("source_responsibility_indices") or [],
    }


class RoleBlueprintService:
    """Build or reuse bounded Blueprint v6 above its historically validated v7 dependency."""

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
        if not analysis_model.strip():
            raise ValueError("A concrete analysis model is required")
        if not capability_model.strip():
            raise ValueError("A concrete Capability model is required")
        if not blueprint_model.strip():
            raise ValueError("A concrete Blueprint model is required")
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")
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

    def build(self, source_job_id: str) -> RoleBlueprintResult:
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
            raise RoleBlueprintError("Job has no current accepted English P1.6 analysis")
        capability = self._capability_store.latest_current(
            source_job_id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if capability is None:
            raise RoleBlueprintError(
                "Job has no current Blueprint-compatible Capability v7 artifact; "
                "Blueprint remains deferred after Capability v9 promotion"
            )
        if capability.job_detail_version_id != source.job_detail_version_id:
            raise RoleBlueprintError("Capability artifact belongs to an older source version")
        if capability.analysis_artifact_id != analysis.id:
            raise RoleBlueprintError("Capability artifact does not depend on current P1.6 analysis")
        if capability.translation_artifact_id != analysis.translation_artifact_id:
            raise RoleBlueprintError("Capability artifact does not depend on current English projection")

        attempted_at = self._clock()
        existing = self._blueprint_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=capability.translation_artifact_id,
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
                translation_artifact_id=capability.translation_artifact_id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return RoleBlueprintResult(
                source_job_id=source.source_job_id,
                artifact_id=existing.id,
                outcome="reused",
                model=existing.model,
                capability_areas=len(existing.blueprint.get("capability_interpretations") or []),
                capability_artifact_id=capability.id,
            )

        capabilities = capability.intelligence.get("capabilities") or []
        if not isinstance(capabilities, list) or not capabilities:
            raise RoleBlueprintError("Capability artifact has no capability profiles")

        payload = {
            "source_job_id": source.source_job_id,
            "role_context": _compact_role_context(source.fields),
            "source_truth": _source_truth_payload(capability.intelligence),
            "capabilities": [
                _capability_payload(item, index)
                for index, item in enumerate(capabilities)
                if isinstance(item, dict)
            ],
        }
        context = {
            "source_truth": payload["source_truth"],
            "capabilities": payload["capabilities"],
        }
        try:
            inference = self._provider.complete(
                system_prompt=_SYSTEM_PROMPT,
                user_payload=payload,
                validation_context=context,
                max_tokens=self._max_tokens,
                seed=0,
            )
            draft = RoleBlueprintDraft.model_validate(inference.blueprint, context=context)
            blueprint = reconcile_role_blueprint_v6(
                draft,
                source_truth=payload["source_truth"],
                capabilities=payload["capabilities"],
            ).model_dump(mode="json")
            artifact_id = self._blueprint_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=capability.translation_artifact_id,
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
                translation_artifact_id=capability.translation_artifact_id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=inference.model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._blueprint_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=capability.translation_artifact_id,
                analysis_artifact_id=analysis.id,
                capability_artifact_id=capability.id,
                model=self._blueprint_model,
                prompt_version=BLUEPRINT_PROMPT_VERSION,
                schema_version=BLUEPRINT_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            if isinstance(exc, RoleBlueprintError):
                raise
            raise RoleBlueprintError(f"Blueprint v6 failed: {exc}") from exc

        artifact = self._blueprint_store.artifact_by_id(artifact_id)
        if artifact is None:
            raise RoleBlueprintError("Persisted Blueprint artifact could not be reloaded")
        return RoleBlueprintResult(
            source_job_id=source.source_job_id,
            artifact_id=artifact.id,
            outcome="completed",
            model=artifact.model,
            capability_areas=len(artifact.blueprint.get("capability_interpretations") or []),
            capability_artifact_id=capability.id,
        )


def build_role_blueprint_service(settings: Settings) -> RoleBlueprintService:
    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No Capability model is configured")
    blueprint_model = settings.effective_blueprint_lm_studio_model()
    if not blueprint_model:
        raise ValueError("No Blueprint model is configured")
    source_store = TranslationStore(settings.database_path)
    return RoleBlueprintService(
        source_store=source_store,
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


def format_role_blueprint(artifact: RoleBlueprintArtifact) -> str:
    lines = [
        f"Role Capability Blueprint for {artifact.source_job_id}",
        f"Model: {artifact.model}",
        f"Contract: {artifact.prompt_version} / {artifact.schema_version}",
        f"Capability artifact: {artifact.capability_artifact_id}",
        "",
    ]
    source_truth = artifact.blueprint.get("source_truth") or {}
    capabilities = artifact.blueprint.get("capability_interpretations") or []
    lines.append("Authoritative source truth")
    lines.append(
        "Capability requirements: "
        f"{len(source_truth.get('linked_requirement_indices') or [])}/"
        f"{len(source_truth.get('capability_requirement_indices') or [])} linked"
    )
    lines.append(
        "Responsibilities: "
        f"{len(source_truth.get('linked_responsibility_indices') or [])}/"
        f"{len(source_truth.get('responsibilities') or [])} linked"
    )
    lines.append(
        "Role-level requirements: "
        f"{source_truth.get('role_level_requirement_indices') or []}"
    )
    lines.append("")
    lines.append("Capability interpretations")
    for item in capabilities:
        lines.append(f"- {item.get('capability_label', '(unlabeled)')}")
        for consideration in item.get("professional_considerations") or []:
            lines.append(
                "  consideration: "
                f"[{consideration.get('interpretation_strength', 'unknown')}] "
                f"{consideration.get('statement', '')}"
            )
            lines.append(f"    uncertainty: {consideration.get('uncertainty', '')}")
        for unknown in item.get("important_unknowns") or []:
            lines.append(f"  unknown: {unknown}")
    return "\n".join(lines)


__all__ = [
    "BLUEPRINT_PROMPT_VERSION",
    "BLUEPRINT_SCHEMA_VERSION",
    "RoleBlueprintError",
    "RoleBlueprintResult",
    "RoleBlueprintService",
    "build_role_blueprint_service",
    "format_role_blueprint",
]
