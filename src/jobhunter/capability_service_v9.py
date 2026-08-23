"""Capability v9 candidate: guarded v8 staging plus corrected source-truth accounting."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference_v8 import (
    CapabilityV8InferenceProvider,
    CapabilityV8InferenceResult,
)
from jobhunter.capability_service_v6 import (
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
)
from jobhunter.capability_service_v6 import (
    format_capability_intelligence as _format_capability_v6,
)
from jobhunter.capability_service_v8 import CapabilityIntelligenceServiceV8
from jobhunter.capability_store import (
    CapabilityIntelligenceArtifact,
    CapabilityIntelligenceStore,
)
from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityGroupPlanV8,
    CapabilityProfileReasoningV8,
)
from jobhunter.capability_v9_models import (
    CapabilityAssignmentPartitionV9,
    CapabilityGroupPlanV9,
    CapabilityProfileReasoningV9,
    CapabilityReasoningDraftV9,
    reconcile_capability_intelligence_v9,
)
from jobhunter.config import Settings
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

CAPABILITY_PROMPT_VERSION = "job-capability-intelligence-v9"
CAPABILITY_SCHEMA_VERSION = "job-capability-intelligence-v5"

_GROUP_PLAN_PROMPT_V9 = """You are JobHunter's Capability v9 group planner.

Propose a small coherent set of capability groups for the supplied accepted job facts.
Do not perform source-index bookkeeping and do not reproduce every technology as its own group.
Group by meaningful work/capability areas. Dense jobs should normally use 3-6 groups; sparse jobs
may use 1-3. Role-level education and standalone experience-duration constraints are context only
and must not become capability groups by themselves.

SEPARATION OF AUTHORITY
JobHunter owns requirement strength, source-explicit technical depth, and source-link accounting.
Keep role interpretation, labels, and summaries neutral on those dimensions. Do not infer
end-to-end/full-lifecycle ownership, autonomy, leadership, or architecture.
"""

_ASSIGNMENT_PROMPT_V9 = """You are JobHunter's Capability v9 source-fact assignment engine.

Assign EVERY supplied owned requirement and responsibility to one or at most two provided
capability groups. Return every owned index exactly once in its assignment list. Use only provided
group IDs. This is bounded provenance bookkeeping, not new extraction or requirement-strength
reasoning. Choose the smallest set of groups that materially fits each fact and omit nothing.
"""

_PROFILE_PROMPT_V9 = """You are JobHunter's Capability v9 per-group reasoning engine.

The group and its accepted P1.6 source facts are already selected. Reason only about this bounded
capability area. JobHunter owns source links, requirement strength, source-explicit depth, and
source-explicit responsibilities.

OPTIONAL MODEL ENRICHMENT
You may add strongly implied technical decomposition, defensible prerequisites, operational
practices/context, bounded work-implied depth, and explicit unknown scope when the supplied evidence
actually supports them. These are optional enrichments, not required output. It is valid to return
only a neutral summary with all analytical lists empty when no additional inference is defensible.
Do not invent an uncertainty merely to fill a field.

CALIBRATION
- Ordinary summaries and non-depth analytical sections must remain neutral on source obligation and
  technical depth. Use words such as supports, involves, covers, combines, or applies.
- depth_signals are optional and should be used only for genuinely work-implied depth beyond the
  source-explicit depth that JobHunter already owns.
- A model_inferred_prerequisite may use prerequisite/necessity language because its status already
  marks it as inference, but it must not be presented as employer-stated required/mandatory/must.
- Preferred/contextual-only facts are not a basis for a model_inferred_prerequisite unless the same
  concept has an independent required basis.
- Do not infer end-to-end/full-lifecycle ownership, autonomy, leadership, or architecture.
- Do not expand a contextual/preferred tool into a mandatory foundation.
- Evidence must use only supplied evidence_reference_ids.
- Do not expand the group into a generic curriculum.
"""


class _CapabilityInferenceV9Adapter:
    """Swap v9 models/prompts into the version-neutral staged orchestration."""

    def __init__(self, delegate: CapabilityV8InferenceProvider) -> None:
        self._delegate = delegate

    def complete(
        self,
        *,
        response_model: type,
        system_prompt: str,
        user_payload: dict[str, Any],
        validation_context: dict[str, Any] | None = None,
        max_tokens: int = 4096,
        seed: int = 0,
    ) -> CapabilityV8InferenceResult:
        context = dict(validation_context or {})
        if response_model is CapabilityGroupPlanV8:
            target_model = CapabilityGroupPlanV9
            target_prompt = _GROUP_PLAN_PROMPT_V9
        elif response_model is CapabilityAssignmentPartitionV8:
            target_model = CapabilityAssignmentPartitionV9
            target_prompt = _ASSIGNMENT_PROMPT_V9
        elif response_model is CapabilityProfileReasoningV8:
            target_model = CapabilityProfileReasoningV9
            target_prompt = _PROFILE_PROMPT_V9
            context["assigned_requirements"] = user_payload.get("requirements") or []
            context["assigned_responsibilities"] = user_payload.get("responsibilities") or []
            group = user_payload.get("group") or {}
            if isinstance(group, dict):
                context["group_summary"] = group.get("summary")
        else:
            raise ValueError(f"Unsupported Capability v9 stage model: {response_model!r}")

        return self._delegate.complete(
            response_model=target_model,
            system_prompt=target_prompt,
            user_payload=user_payload,
            validation_context=context,
            max_tokens=max_tokens,
            seed=seed,
        )


class _CapabilityStoreV9Adapter:
    """Give staged orchestration a distinct v9 persistence contract."""

    def __init__(self, delegate: CapabilityIntelligenceStore) -> None:
        self._delegate = delegate

    def translation_dependency(self, artifact_id: int):
        return self._delegate.translation_dependency(artifact_id)

    def find_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int,
        analysis_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
    ) -> CapabilityIntelligenceArtifact | None:
        return self._delegate.find_artifact(
            job_detail_version_id=job_detail_version_id,
            translation_artifact_id=translation_artifact_id,
            analysis_artifact_id=analysis_artifact_id,
            model=model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )

    def record_artifact(
        self,
        *,
        job_detail_version_id: int,
        translation_artifact_id: int,
        analysis_artifact_id: int,
        model: str,
        prompt_version: str,
        schema_version: str,
        intelligence: dict[str, Any],
        request_body: dict[str, Any],
        raw_response: dict[str, Any],
        created_at: datetime,
    ) -> int:
        v9_request = dict(request_body)
        v9_request["architecture"] = "source-led-group-plan-assignment-profile-v9"
        v9_request["semantic_boundary"] = {
            "source_truth": "strict deterministic authority",
            "model_enrichment": "optional and fail-closed",
            "profile_summary": "fallback to validated neutral group summary on inflation",
            "preferred_contextual_prerequisites": "require independent required concept basis",
            "source_truth_depth_accounting": "capability and role-level depth separated",
        }
        return self._delegate.record_artifact(
            job_detail_version_id=job_detail_version_id,
            translation_artifact_id=translation_artifact_id,
            analysis_artifact_id=analysis_artifact_id,
            model=model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
            intelligence=intelligence,
            request_body=v9_request,
            raw_response=raw_response,
            created_at=created_at,
        )

    def record_attempt(
        self,
        *,
        job_detail_version_id: int,
        attempted_at: datetime,
        model: str,
        prompt_version: str,
        schema_version: str,
        outcome: str,
        translation_artifact_id: int | None = None,
        analysis_artifact_id: int | None = None,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> int:
        return self._delegate.record_attempt(
            job_detail_version_id=job_detail_version_id,
            attempted_at=attempted_at,
            translation_artifact_id=translation_artifact_id,
            analysis_artifact_id=analysis_artifact_id,
            model=model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
            outcome=outcome,
            artifact_id=artifact_id,
            error=error,
        )


class CapabilityIntelligenceServiceV9:
    """V9 contract: strict source truth plus optional bounded model enrichment."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        capability_store: CapabilityIntelligenceStore,
        provider: CapabilityV8InferenceProvider,
        analysis_model: str,
        capability_model: str,
        translation_service: TranslationService | None = None,
        max_tokens: int = 8192,
    ) -> None:
        self._delegate = CapabilityIntelligenceServiceV8(
            source_store=source_store,
            analysis_store=analysis_store,
            capability_store=_CapabilityStoreV9Adapter(capability_store),
            provider=_CapabilityInferenceV9Adapter(provider),
            analysis_model=analysis_model,
            capability_model=capability_model,
            translation_service=translation_service,
            max_tokens=max_tokens,
            reasoning_draft_model=CapabilityReasoningDraftV9,
            reconciler=reconcile_capability_intelligence_v9,
        )

    def analyze_job(self, source_job_id: str) -> CapabilityIntelligenceResult:
        return self._delegate.analyze_job(source_job_id)


def build_capability_v9_candidate_service(settings: Settings) -> CapabilityIntelligenceServiceV9:
    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for the accepted English extraction")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    source_store = TranslationStore(settings.database_path)
    return CapabilityIntelligenceServiceV9(
        source_store=source_store,
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        provider=CapabilityV8InferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=capability_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
        max_tokens=settings.analysis_max_tokens,
    )


def format_capability_v9(artifact: CapabilityIntelligenceArtifact) -> str:
    """Readable v9 review surface with non-misleading source-truth depth accounting."""

    base_lines = _format_capability_v6(artifact).splitlines()
    source_truth = artifact.intelligence.get("source_truth") or {}
    if not source_truth:
        return "\n".join(base_lines)

    capability_requirements = source_truth.get("capability_requirement_indices") or []
    linked_requirements = source_truth.get("linked_requirement_indices") or []
    responsibilities = source_truth.get("responsibilities") or []
    linked_responsibilities = source_truth.get("linked_responsibility_indices") or []
    capability_depth = source_truth.get("capability_explicit_depth_requirement_indices") or []
    linked_capability_depth = (
        source_truth.get("linked_capability_explicit_depth_requirement_indices") or []
    )
    all_depth = source_truth.get("all_explicit_depth_requirement_indices") or []
    role_depth = source_truth.get("role_level_explicit_depth_requirement_indices") or []
    role_level = source_truth.get("role_level_requirement_indices") or []

    source_lines = [
        "",
        "Deterministic P1.6 source truth",
        (
            "Capability requirements linked: "
            f"{len(linked_requirements)}/{len(capability_requirements)}"
        ),
        (
            "Responsibilities linked: "
            f"{len(linked_responsibilities)}/{len(responsibilities)}"
        ),
        (
            "Capability explicit depth represented: "
            f"{len(linked_capability_depth)}/{len(capability_depth)}"
        ),
        f"All explicit depth facts retained in source truth: {len(all_depth)}/{len(all_depth)}",
        f"Role-level explicit depth facts: {len(role_depth)}",
        f"Role-level requirement indices: {role_level}",
    ]

    requirement_by_index = {
        item.get("index"): item
        for item in source_truth.get("requirements") or []
        if isinstance(item, dict)
    }
    if role_level:
        source_lines.append("Role-level requirements:")
        for index in role_level:
            item = requirement_by_index.get(index) or {}
            depth = item.get("depth_signal") or "none"
            source_lines.append(
                "  - "
                f"[{index}] {item.get('concept', '(unknown)')} | "
                f"strength={item.get('requirement_type', 'unknown')} | depth={depth}"
            )

    insert_at = min(4, len(base_lines))
    return "\n".join([*base_lines[:insert_at], *source_lines, *base_lines[insert_at:]])


__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceError",
    "CapabilityIntelligenceResult",
    "CapabilityIntelligenceServiceV9",
    "build_capability_v9_candidate_service",
    "format_capability_v9",
]
