from __future__ import annotations

from typing import Any

from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.p2_3a0_profile_experiment import (
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_b_from_public_capability,
)


def _claim(*, kind: str, index: int, text: str) -> CanonicalClaimReviewItem:
    return CanonicalClaimReviewItem(
        analysis_artifact_id=101,
        source_job_id="job-1",
        job_detail_version_id=201,
        translation_artifact_id=301,
        claim_kind=kind,
        claim_index=index,
        source_text=text,
        evidence=None,
        concept_type=None,
        strength=None,
        depth_signal=None,
        mapping=None,
    )


def _public_capability(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "analysis_artifact_id": 101,
        "artifact_id": 401,
        "capability_schema_version": "job-capability-intelligence-v5",
        "intelligence": {"capabilities": [profile]},
        "job_detail_version_id": 201,
        "model": "accepted-local-model",
        "prompt_version": "job-capability-intelligence-v9",
        "schema_version": "jobhunter-public-corpus-v1",
        "source_job_id": "job-1",
        "stage": "capability",
        "translation_artifact_id": 301,
    }


def _profile(*, include_responsibility: bool) -> dict[str, Any]:
    return {
        "capability_label": "Python",
        "summary": "Accepted job-local Python capability.",
        "requirement_strength": "required",
        "source_requirement_indices": [0],
        "source_responsibility_indices": [0] if include_responsibility else [],
        "depth_signals": [],
        "work_activities": [
            {
                "statement": "Implement production Python services.",
                "evidence_status": "strongly_implied_by_work",
                "evidence": ["Python proficiency"],
                "rationale": "Accepted Capability-v9 interpretation.",
                "confidence": "medium",
            }
        ],
        "sub_capabilities": [],
        "underlying_knowledge": [],
        "operational_practices": [],
        "operational_context": [],
        "unknown_scope": [],
        "independence_expectation": None,
        "overall_confidence": "medium",
    }


def test_strategy_b_suppresses_work_activities_without_exact_responsibility() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (_claim(kind="requirement", index=0, text="Python proficiency"),),
    )

    result = compose_p23a0_strategy_b_from_public_capability(
        base,
        _public_capability(_profile(include_responsibility=False)),
    )

    assert result.base.responsibility_claim_count == 0
    assert result.suppressed_work_activity_count == 1
    assert len(result.groups) == 1
    assert result.groups[0].responsibility_claim_count == 0
    assert result.groups[0].work_activities == ()
    assert result.groups[0].suppressed_work_activity_count == 1


def test_strategy_b_preserves_work_activities_with_exact_responsibility() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(kind="requirement", index=0, text="Python proficiency"),
            _claim(kind="responsibility", index=0, text="Build Python services"),
        ),
    )

    result = compose_p23a0_strategy_b_from_public_capability(
        base,
        _public_capability(_profile(include_responsibility=True)),
    )

    assert result.base.responsibility_claim_count == 1
    assert result.suppressed_work_activity_count == 0
    assert len(result.groups[0].work_activities) == 1
    assert result.groups[0].suppressed_work_activity_count == 0
