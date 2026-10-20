from __future__ import annotations

from typing import Any

from jobhunter.canonical_registry import JobClaimMapping, MappingDisposition
from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.p2_3a0_evaluation import (
    evaluate_p23a0_job,
    evaluate_strategy_a,
    evaluate_strategy_b,
    summarize_p23a0_evaluations,
)
from jobhunter.p2_3a0_profile_experiment import (
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_b_from_public_capability,
)


def _mapping(*, claim_index: int, source_text: str) -> JobClaimMapping:
    return JobClaimMapping(
        id=claim_index + 1,
        analysis_artifact_id=101,
        source_job_id="job-1",
        job_detail_version_id=201,
        translation_artifact_id=301,
        claim_kind="requirement",
        claim_index=claim_index,
        source_text=source_text,
        normalized_source_text=source_text.casefold(),
        canonical_concept_id="skill:python",
        disposition=MappingDisposition.MAPPED.value,
        reviewed_at="2026-10-20T12:00:00+00:00",
        review_note="test",
    )


def _claim(
    *,
    kind: str,
    index: int,
    text: str,
    mapping: JobClaimMapping | None = None,
) -> CanonicalClaimReviewItem:
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
        mapping=mapping,
    )


def _profile(
    *,
    label: str,
    requirements: list[int],
    responsibilities: list[int] | None = None,
) -> dict[str, Any]:
    return {
        "capability_label": label,
        "summary": f"Accepted group {label}",
        "requirement_strength": "required",
        "source_requirement_indices": requirements,
        "source_responsibility_indices": responsibilities or [],
        "depth_signals": [],
        "work_activities": [
            {
                "statement": "Implement Python services",
                "evidence_status": "strongly_implied_by_work",
                "evidence": [],
                "rationale": "test",
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


def _public_capability(profiles: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "analysis_artifact_id": 101,
        "artifact_id": 401,
        "capability_schema_version": "job-capability-intelligence-v5",
        "intelligence": {"capabilities": profiles},
        "job_detail_version_id": 201,
        "model": "accepted-local-model",
        "prompt_version": "job-capability-intelligence-v9",
        "schema_version": "jobhunter-public-corpus-v1",
        "source_job_id": "job-1",
        "stage": "capability",
        "translation_artifact_id": 301,
    }


def test_strategy_a_evaluation_quantifies_mapping_and_fragmentation() -> None:
    first = "Python proficiency"
    second = "Strong Python programming"
    third = "PyTorch familiarity"
    strategy_a = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(
                kind="requirement",
                index=0,
                text=first,
                mapping=_mapping(claim_index=0, source_text=first),
            ),
            _claim(
                kind="requirement",
                index=1,
                text=second,
                mapping=_mapping(claim_index=1, source_text=second),
            ),
            _claim(kind="requirement", index=2, text=third),
        ),
    )

    evaluation = evaluate_strategy_a(strategy_a)

    assert evaluation.claim_count == 3
    assert evaluation.mapped_claim_count == 2
    assert evaluation.bucket_count == 2
    assert evaluation.deterministic_grouping_savings == 1
    assert evaluation.canonical_mapping_coverage_ratio == 0.666667
    assert evaluation.bucket_per_claim_ratio == 0.666667
    assert evaluation.exact_claim_recoverability is True


def test_strategy_b_evaluation_measures_coverage_and_work_guard() -> None:
    strategy_a = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(kind="requirement", index=0, text="Python proficiency"),
            _claim(kind="requirement", index=1, text="PyTorch familiarity"),
        ),
    )
    strategy_b = compose_p23a0_strategy_b_from_public_capability(
        strategy_a,
        _public_capability([_profile(label="Python", requirements=[0])]),
    )

    evaluation = evaluate_strategy_b(strategy_b)

    assert evaluation.base_claim_count == 2
    assert evaluation.grouped_distinct_claim_count == 1
    assert evaluation.ungrouped_claim_count == 1
    assert evaluation.grouped_claim_coverage_ratio == 0.5
    assert evaluation.requirement_only_group_count == 1
    assert evaluation.responsibility_backed_group_count == 0
    assert evaluation.exposed_work_activity_count == 0
    assert evaluation.suppressed_work_activity_count == 1
    assert evaluation.duplicate_group_membership_count == 0
    assert evaluation.exact_partition_ok is True
    assert evaluation.work_activity_boundary_ok is True


def test_strategy_b_evaluation_detects_duplicate_cross_group_membership() -> None:
    strategy_a = compose_p23a0_strategy_a(
        "job-1",
        (_claim(kind="requirement", index=0, text="Python proficiency"),),
    )
    strategy_b = compose_p23a0_strategy_b_from_public_capability(
        strategy_a,
        _public_capability(
            [
                _profile(label="Python", requirements=[0]),
                _profile(label="Programming", requirements=[0]),
            ]
        ),
    )

    evaluation = evaluate_strategy_b(strategy_b)

    assert evaluation.grouped_distinct_claim_count == 1
    assert evaluation.duplicate_group_membership_count == 1
    assert evaluation.exact_partition_ok is False


def test_job_and_cross_job_summary_preserve_unevaluated_strategy_b() -> None:
    strategy_a = compose_p23a0_strategy_a(
        "job-1",
        (_claim(kind="requirement", index=0, text="Python proficiency"),),
    )
    job_evaluation = evaluate_p23a0_job(strategy_a)

    summary = summarize_p23a0_evaluations((job_evaluation,))

    assert job_evaluation.strategy_b is None
    assert summary["job_count"] == 1
    assert summary["strategy_b_available_job_count"] == 0
    assert summary["strategy_a"]["all_exact_claims_recoverable"] is True
    assert summary["strategy_b"]["all_exact_partitions_ok"] is None
    assert summary["strategy_b"]["all_work_activity_boundaries_ok"] is None
    assert summary["decision_authority"] == "none_mechanical_measurements_only"


def test_empty_summary_preserves_unevaluated_state() -> None:
    summary = summarize_p23a0_evaluations(())

    assert summary["job_count"] == 0
    assert summary["strategy_a"]["all_exact_claims_recoverable"] is None
    assert summary["strategy_b"]["all_exact_partitions_ok"] is None
    assert summary["strategy_b"]["all_work_activity_boundaries_ok"] is None
