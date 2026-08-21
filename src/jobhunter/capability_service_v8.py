"""Capability v8 candidate: source-led grouping, bounded assignment, per-profile reasoning."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.capability_inference_v8 import (
    CapabilityV8InferenceProvider,
    CapabilityV8InferenceResult,
)
from jobhunter.capability_service_v6 import (
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
    _evidence_catalog,
    _result,
)
from jobhunter.capability_store import (
    CapabilityIntelligenceStore,
    CapabilityTranslationDependency,
)
from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft,
    partition_source_requirements,
    reconcile_capability_intelligence,
)
from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityGroupPlanV8,
    CapabilityProfileReasoningV8,
    assignment_partitions,
)
from jobhunter.config import Settings
from jobhunter.evidence_refs import evidence_reference_payload
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore

CAPABILITY_PROMPT_VERSION = "job-capability-intelligence-v8"
CAPABILITY_SCHEMA_VERSION = "job-capability-intelligence-v4"

_GROUP_PLAN_PROMPT = """You are JobHunter's Capability v8 group planner.

Your only task is to propose a small coherent set of capability groups for the supplied job facts.
Do NOT perform source-index bookkeeping and do NOT reproduce every technology as its own group.
Group by meaningful work/capability areas. Dense jobs should normally use 3-6 groups; sparse jobs
may use 1-3. Keep tooling/context families separate when they support materially different work.
Do not infer ownership, leadership, mastery, or mandatory strength beyond supplied facts.
Role-level education and standalone experience-duration constraints are context only and must not
be turned into capability groups by themselves.
"""

_ASSIGNMENT_PROMPT = """You are JobHunter's Capability v8 source-fact assignment engine.

Assign EVERY supplied owned requirement and responsibility to one or at most two of the provided
capability groups. Return each owned index exactly once in the corresponding assignment list.
Use only provided group IDs. This is provenance bookkeeping, not new semantic extraction.
Choose the smallest set of groups that materially fit the fact; do not attach unrelated facts just
for balance. Do not omit any owned fact.
"""

_PROFILE_PROMPT = """You are JobHunter's Capability v8 per-group reasoning engine.

The capability group and its accepted P1.6 source facts have already been selected by JobHunter.
Reason ONLY about this bounded group. JobHunter owns source links, requirement strength,
source-explicit depth, and source-explicit responsibilities, so DO NOT reproduce those as
source_explicit analytical items.

Allowed model reasoning:
- strongly_implied_by_work technical sub-capabilities;
- model_inferred_prerequisite knowledge when genuinely necessary;
- bounded operational practices/context supported by the assigned work;
- derived depth only when the work itself supports it;
- explicit unknown_or_unsupported boundaries.

Use evidence identifiers from evidence_reference_ids. Do not invent evidence. Do not convert
preferred/contextual tools into mandatory requirements. Do not infer end-to-end ownership,
autonomy, leadership, or architecture from build/pipeline/production/collaboration language.
Do not expand the group into a generic curriculum.
"""


def _authoritative_p16_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _authoritative_p16_payload(item)
            for key, item in value.items()
            if key != "rationale"
        }
    if isinstance(value, list):
        return [_authoritative_p16_payload(item) for item in value]
    return value


def _source_evidence(item: Any) -> list[str]:
    if not isinstance(item, dict):
        return []
    raw = item.get("evidence")
    values = raw if isinstance(raw, list) else [raw]
    return [value.strip() for value in values if isinstance(value, str) and value.strip()]


def _requirement_fact(index: int, requirements: list[Any]) -> dict[str, Any]:
    item = requirements[index]
    if not isinstance(item, dict):
        raise CapabilityIntelligenceError(f"Accepted P1.6 requirement {index} is not an object")
    return {
        "index": index,
        "concept": item.get("concept"),
        "concept_type": item.get("concept_type"),
        "requirement_type": item.get("requirement_type"),
        "depth_signal": item.get("depth_signal"),
        "evidence": _source_evidence(item),
        "confidence": item.get("confidence"),
    }


def _responsibility_fact(index: int, responsibilities: list[Any]) -> dict[str, Any]:
    item = responsibilities[index]
    if not isinstance(item, dict):
        raise CapabilityIntelligenceError(f"Accepted P1.6 responsibility {index} is not an object")
    return {
        "index": index,
        "statement": item.get("statement"),
        "evidence": _source_evidence(item),
        "confidence": item.get("confidence"),
    }


def _purpose_facts(accepted_extraction: dict[str, Any]) -> list[dict[str, Any]]:
    raw = accepted_extraction.get("role_purpose") or []
    if not isinstance(raw, list):
        raise CapabilityIntelligenceError("Accepted P1.6 role_purpose is not a list")
    return [
        {
            "statement": item.get("statement"),
            "evidence": _source_evidence(item),
            "confidence": item.get("confidence"),
        }
        for item in raw
        if isinstance(item, dict)
    ]


def _group_evidence_catalog(
    full_catalog: dict[str, str],
    requirement_indices: list[int],
    responsibility_indices: list[int],
) -> dict[str, str]:
    prefixes = [
        *(f"p1:requirements:{index}" for index in requirement_indices),
        *(f"p1:responsibilities:{index}" for index in responsibility_indices),
    ]
    return {
        key: value
        for key, value in full_catalog.items()
        if any(key == prefix or key.startswith(f"{prefix}:") for prefix in prefixes)
    }


def _validated_stage(
    result: CapabilityV8InferenceResult,
    fallback_model: type[BaseModel],
    *,
    context: dict[str, Any],
) -> BaseModel:
    """Use provider-normalized typed output; revalidate only legacy/fake provider results."""

    if result.validated_model is not None:
        if not isinstance(result.validated_model, fallback_model):
            raise TypeError(
                "Capability staged provider returned an incompatible validated model: "
                f"expected {fallback_model.__name__}, got "
                f"{type(result.validated_model).__name__}"
            )
        return result.validated_model
    return fallback_model.model_validate(result.intelligence, context=context)


class CapabilityIntelligenceServiceV8:
    """Build/reuse Capability v8 without making one model answer own whole-job coverage."""

    def __init__(
        self,
        *,
        source_store: TranslationStore,
        analysis_store: AnalysisStore,
        capability_store: CapabilityIntelligenceStore,
        provider: CapabilityV8InferenceProvider,
        analysis_model: str,
        capability_model: str,
        max_tokens: int = 8192,
        clock=lambda: datetime.now(UTC),
        reasoning_draft_model: type[CapabilityReasoningDraft] = CapabilityReasoningDraft,
        reconciler: Callable[..., Any] = reconcile_capability_intelligence,
    ) -> None:
        if not analysis_model.strip():
            raise ValueError("A concrete P1.6 English analysis model is required")
        if not capability_model.strip():
            raise ValueError("A concrete capability-intelligence model is required")
        if not 1 <= max_tokens <= 32768:
            raise ValueError("max_tokens must be between 1 and 32768")
        self._source_store = source_store
        self._analysis_store = analysis_store
        self._capability_store = capability_store
        self._provider = provider
        self._analysis_model = analysis_model.strip()
        self._capability_model = capability_model.strip()
        self._max_tokens = max_tokens
        self._clock = clock
        self._reasoning_draft_model = reasoning_draft_model
        self._reconciler = reconciler

    def _current_dependencies(
        self,
        source_job_id: str,
    ) -> tuple[Any, CapabilityTranslationDependency, AnalysisArtifact]:
        source = self._source_store.latest_source_version(source_job_id)
        if source is None:
            raise CapabilityIntelligenceError(
                "Job has no current successfully parsed source version"
            )
        analysis = self._analysis_store.latest_current(
            source_job_id,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            accepted_only=True,
        )
        if analysis is None:
            raise CapabilityIntelligenceError(
                "Job has no semantically accepted current English P1.6 analysis; run Analyze "
                "English first, then accept its semantic review"
            )
        if analysis.job_detail_version_id != source.job_detail_version_id:
            raise CapabilityIntelligenceError(
                "English analysis does not belong to the current source semantic version"
            )
        if analysis.translation_artifact_id is None:
            raise CapabilityIntelligenceError(
                "English analysis has no referenced hardened English projection"
            )
        translation = self._capability_store.translation_dependency(
            analysis.translation_artifact_id
        )
        if translation is None:
            raise CapabilityIntelligenceError(
                "English analysis references a missing English projection artifact"
            )
        if translation.source_job_id != source_job_id:
            raise CapabilityIntelligenceError(
                "English analysis references a translation artifact from another job"
            )
        if translation.job_detail_version_id != source.job_detail_version_id:
            raise CapabilityIntelligenceError(
                "English analysis references an English projection from an older source version"
            )
        if translation.target_language != "en":
            raise CapabilityIntelligenceError(
                "English analysis references a non-English translation artifact"
            )
        if translation.translation_schema_version != TRANSLATION_SCHEMA_VERSION:
            raise CapabilityIntelligenceError(
                "English analysis references a historical English projection and requires v2 repair"
            )
        return (
            source,
            translation,
            replace(analysis, analysis=_authoritative_p16_payload(analysis.analysis)),
        )

    @staticmethod
    def _analysis_fields(fields: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in fields.items()
            if key not in {"language", "parser_version"}
        }

    def analyze_job(self, source_job_id: str) -> CapabilityIntelligenceResult:
        source, translation, analysis = self._current_dependencies(source_job_id)
        attempted_at = self._clock()
        existing = self._capability_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if existing is not None:
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, outcome="reused")

        accepted = analysis.analysis
        requirements = accepted.get("requirements") or []
        responsibilities = accepted.get("responsibilities") or []
        if not isinstance(requirements, list):
            raise CapabilityIntelligenceError("Accepted P1.6 requirements are not a list")
        if not isinstance(responsibilities, list):
            raise CapabilityIntelligenceError("Accepted P1.6 responsibilities are not a list")

        analysis_fields = self._analysis_fields(translation.fields)
        full_evidence_catalog = _evidence_catalog(analysis_fields, accepted)
        capability_requirements, role_level_requirements = partition_source_requirements(accepted)
        stage_requests: list[dict[str, Any]] = []
        stage_responses: list[dict[str, Any]] = []

        try:
            plan_payload = {
                "source_job_id": source.source_job_id,
                "title": analysis_fields.get("title"),
                "company": analysis_fields.get("company"),
                "role_purpose": _purpose_facts(accepted),
                "capability_requirements": [
                    _requirement_fact(index, requirements)
                    for index in capability_requirements
                ],
                "role_level_constraints": [
                    _requirement_fact(index, requirements)
                    for index in role_level_requirements
                ],
                "responsibilities": [
                    _responsibility_fact(index, responsibilities)
                    for index in range(len(responsibilities))
                ],
            }
            plan_context = {
                "capability_requirement_count": len(capability_requirements),
                "responsibility_count": len(responsibilities),
            }
            plan_result = self._provider.complete(
                response_model=CapabilityGroupPlanV8,
                system_prompt=_GROUP_PLAN_PROMPT,
                user_payload=plan_payload,
                validation_context=plan_context,
                max_tokens=min(self._max_tokens, 3072),
                seed=0,
            )
            stage_requests.append(plan_result.request_body)
            stage_responses.append(plan_result.raw_response)
            plan = _validated_stage(
                plan_result,
                CapabilityGroupPlanV8,
                context=plan_context,
            )
            group_ids = {group.group_id for group in plan.groups}  # type: ignore[attr-defined]

            requirement_groups: dict[int, set[int]] = {
                index: set() for index in capability_requirements
            }
            responsibility_groups: dict[int, set[int]] = {
                index: set() for index in range(len(responsibilities))
            }
            partitions = assignment_partitions(
                capability_requirements,
                len(responsibilities),
            )
            for partition_index, (owned_requirements, owned_responsibilities) in enumerate(
                partitions
            ):
                assignment_payload = {
                    "source_job_id": source.source_job_id,
                    "groups": [
                        group.model_dump(mode="json")
                        for group in plan.groups  # type: ignore[attr-defined]
                    ],
                    "owned_requirements": [
                        _requirement_fact(index, requirements)
                        for index in owned_requirements
                    ],
                    "owned_responsibilities": [
                        _responsibility_fact(index, responsibilities)
                        for index in owned_responsibilities
                    ],
                }
                assignment_context = {
                    "owned_requirement_indices": owned_requirements,
                    "owned_responsibility_indices": owned_responsibilities,
                    "valid_group_ids": sorted(group_ids),
                }
                assignment_result = self._provider.complete(
                    response_model=CapabilityAssignmentPartitionV8,
                    system_prompt=_ASSIGNMENT_PROMPT,
                    user_payload=assignment_payload,
                    validation_context=assignment_context,
                    max_tokens=min(self._max_tokens, 2048),
                    seed=100 + partition_index,
                )
                stage_requests.append(assignment_result.request_body)
                stage_responses.append(assignment_result.raw_response)
                assignment = _validated_stage(
                    assignment_result,
                    CapabilityAssignmentPartitionV8,
                    context=assignment_context,
                )
                for item in assignment.requirement_assignments:  # type: ignore[attr-defined]
                    requirement_groups[item.index].update(item.group_ids)
                for item in assignment.responsibility_assignments:  # type: ignore[attr-defined]
                    responsibility_groups[item.index].update(item.group_ids)

            used_group_ids = {
                group_id
                for values in [*requirement_groups.values(), *responsibility_groups.values()]
                for group_id in values
            }
            if (
                len(capability_requirements) >= 12
                and len(responsibilities) >= 5
                and len(used_group_ids) < 2
            ):
                raise CapabilityIntelligenceError(
                    "Dense Capability v8 assignment collapsed all source facts into one group"
                )

            capabilities: list[dict[str, Any]] = []
            profile_uncertainties: list[str] = []
            for group_offset, group in enumerate(plan.groups):  # type: ignore[attr-defined]
                if group.group_id not in used_group_ids:
                    continue
                group_requirement_indices = sorted(
                    index
                    for index, values in requirement_groups.items()
                    if group.group_id in values
                )
                group_responsibility_indices = sorted(
                    index
                    for index, values in responsibility_groups.items()
                    if group.group_id in values
                )
                group_catalog = _group_evidence_catalog(
                    full_evidence_catalog,
                    group_requirement_indices,
                    group_responsibility_indices,
                )
                profile_payload = {
                    "source_job_id": source.source_job_id,
                    "group": group.model_dump(mode="json"),
                    "requirements": [
                        _requirement_fact(index, requirements)
                        for index in group_requirement_indices
                    ],
                    "responsibilities": [
                        _responsibility_fact(index, responsibilities)
                        for index in group_responsibility_indices
                    ],
                    "evidence_reference_ids": sorted(group_catalog),
                    "evidence_references": evidence_reference_payload(group_catalog),
                }
                profile_context = {
                    "analysis_fields": analysis_fields,
                    "evidence_catalog": group_catalog,
                }
                profile_result = self._provider.complete(
                    response_model=CapabilityProfileReasoningV8,
                    system_prompt=_PROFILE_PROMPT,
                    user_payload=profile_payload,
                    validation_context=profile_context,
                    max_tokens=min(self._max_tokens, 4096),
                    seed=200 + group_offset,
                )
                stage_requests.append(profile_result.request_body)
                stage_responses.append(profile_result.raw_response)
                profile = _validated_stage(
                    profile_result,
                    CapabilityProfileReasoningV8,
                    context=profile_context,
                )
                profile_uncertainties.extend(profile.uncertainties)  # type: ignore[attr-defined]
                capabilities.append(
                    {
                        "capability_label": group.capability_label,
                        "summary": profile.summary,  # type: ignore[attr-defined]
                        "source_requirement_indices": group_requirement_indices,
                        "source_responsibility_indices": group_responsibility_indices,
                        "requirement_strength": "unspecified",
                        "depth_signals": [
                            item.model_dump(mode="json")
                            for item in profile.depth_signals  # type: ignore[attr-defined]
                        ],
                        "work_activities": [
                            item.model_dump(mode="json")
                            for item in profile.work_activities  # type: ignore[attr-defined]
                        ],
                        "sub_capabilities": [
                            item.model_dump(mode="json")
                            for item in profile.sub_capabilities  # type: ignore[attr-defined]
                        ],
                        "underlying_knowledge": [
                            item.model_dump(mode="json")
                            for item in profile.underlying_knowledge  # type: ignore[attr-defined]
                        ],
                        "operational_practices": [
                            item.model_dump(mode="json")
                            for item in profile.operational_practices  # type: ignore[attr-defined]
                        ],
                        "independence_expectation": None,
                        "operational_context": [
                            item.model_dump(mode="json")
                            for item in profile.operational_context  # type: ignore[attr-defined]
                        ],
                        "unknown_scope": [
                            item.model_dump(mode="json")
                            for item in profile.unknown_scope  # type: ignore[attr-defined]
                        ],
                        "overall_confidence": profile.overall_confidence,  # type: ignore[attr-defined]
                    }
                )

            draft_payload = {
                "role_interpretation": plan.role_interpretation,  # type: ignore[attr-defined]
                "capabilities": capabilities,
                "cross_capability_observations": [],
                "uncertainties": list(
                    dict.fromkeys(
                        [
                            *plan.uncertainties,  # type: ignore[attr-defined]
                            *profile_uncertainties,
                        ]
                    )
                ),
            }
            draft = self._reasoning_draft_model.model_validate(
                draft_payload,
                context={
                    "analysis_fields": analysis_fields,
                    "evidence_catalog": full_evidence_catalog,
                    "accepted_extraction": accepted,
                },
            )
            reconciled = self._reconciler(
                draft,
                accepted_extraction=accepted,
                analysis_fields=analysis_fields,
                evidence_catalog=full_evidence_catalog,
            )
            intelligence = reconciled.model_dump(mode="json")
            artifact_id = self._capability_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                intelligence=intelligence,
                request_body={
                    "architecture": "source-led-group-plan-assignment-profile-v8",
                    "stages": stage_requests,
                },
                raw_response={"stages": stage_responses},
                created_at=attempted_at,
            )
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

        artifact = self._capability_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Capability v8 artifact disappeared after persistence")
        return _result(artifact, outcome="completed")


def build_capability_v8_candidate_service(settings: Settings) -> CapabilityIntelligenceServiceV8:
    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for the accepted English extraction")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    source_store = TranslationStore(settings.database_path)
    return CapabilityIntelligenceServiceV8(
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


__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceServiceV8",
    "build_capability_v8_candidate_service",
]
