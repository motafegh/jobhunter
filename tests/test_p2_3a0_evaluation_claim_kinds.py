from __future__ import annotations

from jobhunter.canonical_registry import JobClaimMapping, MappingDisposition
from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.p2_3a0_evaluation import evaluate_strategy_a, evaluate_strategy_b
from jobhunter.p2_3a0_profile_experiment import (
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_b_from_public_capability,
)


def _claim(*, kind: str, index: int, text: str, mapped: bool) -> CanonicalClaimReviewItem:
    mapping = None
    if mapped:
        mapping = JobClaimMapping(
            id=index + (1 if kind == "requirement" else 100),
            analysis_artifact_id=101,
            source_job_id="job-1",
            job_detail_version_id=201,
            translation_artifact_id=301,
            claim_kind=kind,
            claim_index=index,
            source_text=text,
            normalized_source_text=text.casefold(),
            canonical_concept_id=f"{kind}:canonical-test",
            disposition=MappingDisposition.MAPPED.value,
            reviewed_at="2026-10-20T12:00:00+00:00",
            review_note="test",
        )
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


def test_strategy_a_reports_requirement_and_responsibility_mapping_separately() -> None:
    composition = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(kind="requirement", index=0, text="Python", mapped=True),
            _claim(kind="requirement", index=1, text="PyTorch", mapped=False),
            _claim(kind="responsibility", index=0, text="Build APIs", mapped=True),
        ),
    )

    evaluation = evaluate_strategy_a(composition)

    assert evaluation.requirement_claim_count == 2
    assert evaluation.responsibility_claim_count == 1
    assert evaluation.mapped_requirement_claim_count == 1
    assert evaluation.mapped_responsibility_claim_count == 1
    assert evaluation.requirement_mapping_coverage_ratio == 0.5
    assert evaluation.responsibility_mapping_coverage_ratio == 1.0


def test_strategy_b_reports_grouped_requirement_and_responsibility_coverage() -> None:
    composition = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(kind="requirement", index=0, text="Python", mapped=False),
            _claim(kind="responsibility", index=0, text="Build APIs", mapped=False),
        ),
    )
    public_capability = {
        "analysis_artifact_id": 101,
        "artifact_id": 401,
        "capability_schema_version": "job-capability-intelligence-v5",
        "intelligence": {
            "capabilities": [
                {
                    "capability_label": "Python",
                    "summary": "Python qualification",
                    "requirement_strength": "required",
                    "source_requirement_indices": [0],
                    "source_responsibility_indices": [],
                    "depth_signals": [],
                    "work_activities": [],
                    "sub_capabilities": [],
                    "underlying_knowledge": [],
                    "operational_practices": [],
                    "operational_context": [],
                    "unknown_scope": [],
                    "independence_expectation": None,
                    "overall_confidence": "medium",
                }
            ]
        },
        "job_detail_version_id": 201,
        "model": "accepted-local-model",
        "prompt_version": "job-capability-intelligence-v9",
        "schema_version": "jobhunter-public-corpus-v1",
        "source_job_id": "job-1",
        "stage": "capability",
        "translation_artifact_id": 301,
    }
    strategy_b = compose_p23a0_strategy_b_from_public_capability(
        composition,
        public_capability,
    )

    evaluation = evaluate_strategy_b(strategy_b)

    assert evaluation.base_requirement_claim_count == 1
    assert evaluation.base_responsibility_claim_count == 1
    assert evaluation.grouped_requirement_claim_count == 1
    assert evaluation.grouped_responsibility_claim_count == 0
    assert evaluation.grouped_requirement_coverage_ratio == 1.0
    assert evaluation.grouped_responsibility_coverage_ratio == 0.0
