from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from jobhunter.capability_service_v9 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    _CapabilityInferenceV9Adapter,
    _CapabilityStoreV9Adapter,
)
from jobhunter.capability_v8_models import CapabilityProfileReasoningV8
from jobhunter.capability_v9_models import (
    CapabilityGroupPlanV9,
    CapabilityProfileReasoningV9,
    build_v9_intelligence,
)


def test_v9_group_plan_allows_deep_learning_but_rejects_added_depth() -> None:
    accepted = {
        "role_interpretation": (
            "The role combines machine learning and deep learning with manufacturing analytics."
        ),
        "groups": [
            {
                "group_id": 0,
                "capability_label": "Machine learning and modeling",
                "summary": "Combines model development with manufacturing analytics work.",
            }
        ],
        "uncertainties": [],
    }
    CapabilityGroupPlanV9.model_validate(accepted)

    rejected = dict(accepted)
    rejected["role_interpretation"] = (
        "The role combines advanced machine learning with manufacturing analytics."
    )
    with pytest.raises(ValueError, match="may not add technical depth"):
        CapabilityGroupPlanV9.model_validate(rejected)


def _profile_context(*, requirement_type: str = "preferred") -> dict:
    evidence = "industrial / edge deployment a plus"
    return {
        "analysis_fields": {"description": evidence},
        "evidence_catalog": {"p1:requirements:0": evidence},
        "assigned_requirements": [
            {
                "index": 0,
                "concept": "Industrial / edge deployment",
                "concept_type": "domain",
                "requirement_type": requirement_type,
                "depth_signal": None,
                "evidence": [evidence],
                "confidence": "high",
            }
        ],
        "assigned_responsibilities": [],
    }


def _profile_payload() -> dict:
    return {
        "summary": "The capability covers deployment-related operational context.",
        "depth_signals": [],
        "work_activities": [],
        "sub_capabilities": [
            {
                "statement": "Industrial deployment context",
                "evidence_status": "strongly_implied_by_work",
                "evidence": ["p1:requirements:0"],
                "rationale": "The listed deployment context supports this bounded interpretation.",
                "confidence": "high",
            }
        ],
        "underlying_knowledge": [],
        "operational_practices": [],
        "operational_context": [],
        "unknown_scope": [],
        "overall_confidence": "high",
        "uncertainties": [],
    }


def test_v9_profile_summary_inflation_remains_hard_failure() -> None:
    context = _profile_context()
    payload = _profile_payload()
    payload["summary"] = "The capability covers end-to-end deployment operations."
    with pytest.raises(ValueError, match="may not infer ownership"):
        CapabilityProfileReasoningV9.model_validate(payload, context=context)


def test_v9_discards_one_unsafe_derived_expectation_without_failing_profile() -> None:
    context = _profile_context()
    payload = _profile_payload()
    payload["sub_capabilities"][0]["rationale"] = (
        "The listed deployment context requires this capability."
    )

    profile = CapabilityProfileReasoningV9.model_validate(payload, context=context)

    assert profile.sub_capabilities == []
    assert any(
        "discarded 1 optional model-derived expectation" in item
        for item in profile.uncertainties
    )


def test_v9_discards_preferred_only_prerequisite_instead_of_retrying_profile() -> None:
    context = _profile_context(requirement_type="preferred")
    payload = _profile_payload()
    payload["sub_capabilities"][0]["evidence_status"] = "model_inferred_prerequisite"

    profile = CapabilityProfileReasoningV9.model_validate(payload, context=context)

    assert profile.sub_capabilities == []
    assert any(
        "discarded 1 optional model-derived expectation" in item
        for item in profile.uncertainties
    )


def test_v9_discards_obligation_in_derived_depth_but_keeps_safe_depth() -> None:
    context = _profile_context(requirement_type="required")
    payload = _profile_payload()
    payload["sub_capabilities"] = []
    payload["depth_signals"] = [
        {
            "statement": "Practical implementation across multiple machine learning approaches.",
            "evidence_status": "strongly_implied_by_work",
            "evidence": ["p1:requirements:0"],
            "rationale": (
                "The bounded evidence supports this implementation-oriented interpretation."
            ),
            "confidence": "medium",
        },
        {
            "statement": "This is a necessary component of the capability.",
            "evidence_status": "strongly_implied_by_work",
            "evidence": ["p1:requirements:0"],
            "rationale": "It is a prerequisite for the supported work.",
            "confidence": "medium",
        },
    ]

    profile = CapabilityProfileReasoningV9.model_validate(payload, context=context)

    assert len(profile.depth_signals) == 1
    assert profile.depth_signals[0].statement.startswith("Practical implementation")
    assert any(
        "discarded 1 optional model-derived expectation" in item
        for item in profile.uncertainties
    )


def _legacy_intelligence() -> dict:
    return {
        "source_truth": {
            "role_purpose": [],
            "requirements": [
                {
                    "index": 0,
                    "concept": "Python",
                    "concept_type": "tool",
                    "requirement_type": "required",
                    "depth_signal": "expert",
                    "evidence": ["Python (expert)"],
                    "confidence": "high",
                },
                {
                    "index": 1,
                    "concept": "Professional experience",
                    "concept_type": "experience",
                    "requirement_type": "required",
                    "depth_signal": "three to six years",
                    "evidence": ["three to six years"],
                    "confidence": "high",
                },
                {
                    "index": 2,
                    "concept": "Master's degree",
                    "concept_type": "education",
                    "requirement_type": "required",
                    "depth_signal": None,
                    "evidence": ["Master's degree"],
                    "confidence": "high",
                },
            ],
            "responsibilities": [],
            "capability_requirement_indices": [0],
            "role_level_requirement_indices": [1, 2],
            "linked_requirement_indices": [0],
            "unlinked_capability_requirement_indices": [],
            "linked_responsibility_indices": [],
            "unlinked_responsibility_indices": [],
            "explicit_depth_requirement_indices": [0, 1],
            "linked_explicit_depth_requirement_indices": [0],
            "unlinked_explicit_depth_requirement_indices": [1],
        }
    }


def test_v9_source_truth_separates_role_level_depth_from_capability_depth() -> None:
    result = build_v9_intelligence(_legacy_intelligence())
    source_truth = result["source_truth"]
    assert source_truth["all_explicit_depth_requirement_indices"] == [0, 1]
    assert source_truth["capability_explicit_depth_requirement_indices"] == [0]
    assert source_truth["linked_capability_explicit_depth_requirement_indices"] == [0]
    assert source_truth["unlinked_capability_explicit_depth_requirement_indices"] == []
    assert source_truth["role_level_explicit_depth_requirement_indices"] == [1]
    assert "unlinked_explicit_depth_requirement_indices" not in source_truth


class _StoreDelegate:
    def __init__(self) -> None:
        self.recorded: dict = {}

    def record_artifact(self, **kwargs) -> int:
        self.recorded = kwargs
        return 42


def test_v9_store_adapter_records_distinct_contract_and_accounting() -> None:
    delegate = _StoreDelegate()
    adapter = _CapabilityStoreV9Adapter(delegate)  # type: ignore[arg-type]
    artifact_id = adapter.record_artifact(
        job_detail_version_id=1,
        translation_artifact_id=2,
        analysis_artifact_id=36,
        model="model",
        prompt_version="job-capability-intelligence-v8",
        schema_version="job-capability-intelligence-v4",
        intelligence=_legacy_intelligence(),
        request_body={"architecture": "source-led-group-plan-assignment-profile-v8"},
        raw_response={},
        created_at=datetime(2026, 8, 15, tzinfo=UTC),
    )
    assert artifact_id == 42
    assert delegate.recorded["prompt_version"] == CAPABILITY_PROMPT_VERSION
    assert delegate.recorded["schema_version"] == CAPABILITY_SCHEMA_VERSION
    assert delegate.recorded["request_body"]["architecture"].endswith("-v9")
    assert delegate.recorded["intelligence"]["source_truth"][
        "role_level_explicit_depth_requirement_indices"
    ] == [1]


class _InferenceDelegate:
    def __init__(self) -> None:
        self.kwargs: dict = {}

    def complete(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(intelligence={})


def test_v9_inference_adapter_swaps_profile_model_and_adds_assignment_context() -> None:
    delegate = _InferenceDelegate()
    adapter = _CapabilityInferenceV9Adapter(delegate)  # type: ignore[arg-type]
    result = adapter.complete(
        response_model=CapabilityProfileReasoningV8,
        system_prompt="old",
        user_payload={
            "requirements": [{"index": 3}],
            "responsibilities": [{"index": 4}],
        },
        validation_context={"analysis_fields": {}},
    )
    assert result.intelligence == {}
    assert delegate.kwargs["response_model"] is CapabilityProfileReasoningV9
    assert delegate.kwargs["validation_context"]["assigned_requirements"] == [{"index": 3}]
    assert delegate.kwargs["validation_context"]["assigned_responsibilities"] == [{"index": 4}]
