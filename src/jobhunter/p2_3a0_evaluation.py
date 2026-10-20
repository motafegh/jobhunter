"""Deterministic measurements for the non-authoritative P2.3A-0 experiment.

These metrics describe composition behavior; they do not select an architecture,
promote P2.3 authority, or replace semantic/usefulness review.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jobhunter.p2_3a0_profile_experiment import (
    P23A0StrategyAComposition,
    P23A0StrategyBComposition,
)


@dataclass(frozen=True, slots=True)
class P23A0StrategyAEvaluation:
    claim_count: int
    requirement_claim_count: int
    responsibility_claim_count: int
    mapped_claim_count: int
    mapped_requirement_claim_count: int
    mapped_responsibility_claim_count: int
    bucket_count: int
    canonical_bucket_count: int
    source_local_bucket_count: int
    deterministic_grouping_savings: int
    canonical_mapping_coverage_ratio: float | None
    requirement_mapping_coverage_ratio: float | None
    responsibility_mapping_coverage_ratio: float | None
    bucket_per_claim_ratio: float | None
    exact_claim_recoverability: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "claim_count": self.claim_count,
            "requirement_claim_count": self.requirement_claim_count,
            "responsibility_claim_count": self.responsibility_claim_count,
            "mapped_claim_count": self.mapped_claim_count,
            "mapped_requirement_claim_count": self.mapped_requirement_claim_count,
            "mapped_responsibility_claim_count": self.mapped_responsibility_claim_count,
            "bucket_count": self.bucket_count,
            "canonical_bucket_count": self.canonical_bucket_count,
            "source_local_bucket_count": self.source_local_bucket_count,
            "deterministic_grouping_savings": self.deterministic_grouping_savings,
            "canonical_mapping_coverage_ratio": self.canonical_mapping_coverage_ratio,
            "requirement_mapping_coverage_ratio": self.requirement_mapping_coverage_ratio,
            "responsibility_mapping_coverage_ratio": (
                self.responsibility_mapping_coverage_ratio
            ),
            "bucket_per_claim_ratio": self.bucket_per_claim_ratio,
            "exact_claim_recoverability": self.exact_claim_recoverability,
        }


@dataclass(frozen=True, slots=True)
class P23A0StrategyBEvaluation:
    base_claim_count: int
    base_requirement_claim_count: int
    base_responsibility_claim_count: int
    grouped_distinct_claim_count: int
    grouped_requirement_claim_count: int
    grouped_responsibility_claim_count: int
    ungrouped_claim_count: int
    group_count: int
    reviewed_canonical_concept_count: int
    grouped_claim_coverage_ratio: float | None
    grouped_requirement_coverage_ratio: float | None
    grouped_responsibility_coverage_ratio: float | None
    group_per_grouped_claim_ratio: float | None
    semantic_grouping_savings: int
    requirement_only_group_count: int
    responsibility_backed_group_count: int
    exposed_work_activity_count: int
    suppressed_work_activity_count: int
    duplicate_group_membership_count: int
    exact_partition_ok: bool
    work_activity_boundary_ok: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "base_claim_count": self.base_claim_count,
            "base_requirement_claim_count": self.base_requirement_claim_count,
            "base_responsibility_claim_count": self.base_responsibility_claim_count,
            "grouped_distinct_claim_count": self.grouped_distinct_claim_count,
            "grouped_requirement_claim_count": self.grouped_requirement_claim_count,
            "grouped_responsibility_claim_count": self.grouped_responsibility_claim_count,
            "ungrouped_claim_count": self.ungrouped_claim_count,
            "group_count": self.group_count,
            "reviewed_canonical_concept_count": self.reviewed_canonical_concept_count,
            "grouped_claim_coverage_ratio": self.grouped_claim_coverage_ratio,
            "grouped_requirement_coverage_ratio": self.grouped_requirement_coverage_ratio,
            "grouped_responsibility_coverage_ratio": (
                self.grouped_responsibility_coverage_ratio
            ),
            "group_per_grouped_claim_ratio": self.group_per_grouped_claim_ratio,
            "semantic_grouping_savings": self.semantic_grouping_savings,
            "requirement_only_group_count": self.requirement_only_group_count,
            "responsibility_backed_group_count": self.responsibility_backed_group_count,
            "exposed_work_activity_count": self.exposed_work_activity_count,
            "suppressed_work_activity_count": self.suppressed_work_activity_count,
            "duplicate_group_membership_count": self.duplicate_group_membership_count,
            "exact_partition_ok": self.exact_partition_ok,
            "work_activity_boundary_ok": self.work_activity_boundary_ok,
        }


@dataclass(frozen=True, slots=True)
class P23A0JobEvaluation:
    source_job_id: str
    strategy_a: P23A0StrategyAEvaluation
    strategy_b: P23A0StrategyBEvaluation | None

    def to_payload(self) -> dict[str, Any]:
        return {
            "source_job_id": self.source_job_id,
            "strategy_a": self.strategy_a.to_payload(),
            "strategy_b": (
                self.strategy_b.to_payload() if self.strategy_b is not None else None
            ),
        }


def evaluate_strategy_a(
    composition: P23A0StrategyAComposition,
) -> P23A0StrategyAEvaluation:
    """Measure deterministic Strategy-A coverage and fragmentation."""

    claims = composition.claims
    claim_count = composition.claim_count
    requirement_claim_count = composition.requirement_claim_count
    responsibility_claim_count = composition.responsibility_claim_count
    mapped_requirement_claim_count = sum(
        claim.claim_kind == "requirement" and claim.mapping_state == "mapped"
        for claim in claims
    )
    mapped_responsibility_claim_count = sum(
        claim.claim_kind == "responsibility" and claim.mapping_state == "mapped"
        for claim in claims
    )
    bucket_count = len(composition.buckets)
    return P23A0StrategyAEvaluation(
        claim_count=claim_count,
        requirement_claim_count=requirement_claim_count,
        responsibility_claim_count=responsibility_claim_count,
        mapped_claim_count=composition.mapped_claim_count,
        mapped_requirement_claim_count=mapped_requirement_claim_count,
        mapped_responsibility_claim_count=mapped_responsibility_claim_count,
        bucket_count=bucket_count,
        canonical_bucket_count=composition.canonical_bucket_count,
        source_local_bucket_count=composition.source_local_bucket_count,
        deterministic_grouping_savings=composition.deterministic_grouping_savings,
        canonical_mapping_coverage_ratio=_ratio(
            composition.mapped_claim_count,
            claim_count,
        ),
        requirement_mapping_coverage_ratio=_ratio(
            mapped_requirement_claim_count,
            requirement_claim_count,
        ),
        responsibility_mapping_coverage_ratio=_ratio(
            mapped_responsibility_claim_count,
            responsibility_claim_count,
        ),
        bucket_per_claim_ratio=_ratio(bucket_count, claim_count),
        exact_claim_recoverability=(len(claims) == claim_count),
    )


def evaluate_strategy_b(
    composition: P23A0StrategyBComposition,
) -> P23A0StrategyBEvaluation:
    """Measure Strategy-B grouping coverage without treating labels as authority."""

    grouped_occurrences = [
        _claim_identity(claim)
        for group in composition.groups
        for claim in group.claims
    ]
    grouped_distinct = set(grouped_occurrences)
    duplicate_group_membership_count = len(grouped_occurrences) - len(grouped_distinct)
    ungrouped_identities = {_claim_identity(claim) for claim in composition.ungrouped_claims}
    base_identities = {_claim_identity(claim) for claim in composition.base.claims}

    requirement_only_groups = [
        group for group in composition.groups if group.responsibility_claim_count == 0
    ]
    responsibility_backed_groups = [
        group for group in composition.groups if group.responsibility_claim_count > 0
    ]
    exposed_work_activity_count = sum(
        len(group.work_activities) for group in composition.groups
    )
    work_activity_boundary_ok = all(
        not group.work_activities for group in requirement_only_groups
    )
    exact_partition_ok = (
        duplicate_group_membership_count == 0
        and grouped_distinct.isdisjoint(ungrouped_identities)
        and grouped_distinct | ungrouped_identities == base_identities
    )

    grouped_claim_count = len(grouped_distinct)
    grouped_requirement_claim_count = sum(
        identity[1] == "requirement" for identity in grouped_distinct
    )
    grouped_responsibility_claim_count = sum(
        identity[1] == "responsibility" for identity in grouped_distinct
    )
    group_count = len(composition.groups)
    return P23A0StrategyBEvaluation(
        base_claim_count=composition.base.claim_count,
        base_requirement_claim_count=composition.base.requirement_claim_count,
        base_responsibility_claim_count=composition.base.responsibility_claim_count,
        grouped_distinct_claim_count=grouped_claim_count,
        grouped_requirement_claim_count=grouped_requirement_claim_count,
        grouped_responsibility_claim_count=grouped_responsibility_claim_count,
        ungrouped_claim_count=len(composition.ungrouped_claims),
        group_count=group_count,
        reviewed_canonical_concept_count=len(composition.canonical_concept_ids),
        grouped_claim_coverage_ratio=_ratio(
            grouped_claim_count,
            composition.base.claim_count,
        ),
        grouped_requirement_coverage_ratio=_ratio(
            grouped_requirement_claim_count,
            composition.base.requirement_claim_count,
        ),
        grouped_responsibility_coverage_ratio=_ratio(
            grouped_responsibility_claim_count,
            composition.base.responsibility_claim_count,
        ),
        group_per_grouped_claim_ratio=_ratio(group_count, grouped_claim_count),
        semantic_grouping_savings=grouped_claim_count - group_count,
        requirement_only_group_count=len(requirement_only_groups),
        responsibility_backed_group_count=len(responsibility_backed_groups),
        exposed_work_activity_count=exposed_work_activity_count,
        suppressed_work_activity_count=composition.suppressed_work_activity_count,
        duplicate_group_membership_count=duplicate_group_membership_count,
        exact_partition_ok=exact_partition_ok,
        work_activity_boundary_ok=work_activity_boundary_ok,
    )


def evaluate_p23a0_job(
    strategy_a: P23A0StrategyAComposition,
    strategy_b: P23A0StrategyBComposition | None = None,
) -> P23A0JobEvaluation:
    """Evaluate one job while preserving Strategy-B optionality."""

    if strategy_b is not None and strategy_b.base.source_job_id != strategy_a.source_job_id:
        raise ValueError("Strategy A/B evaluations must describe the same source job")
    if strategy_b is not None and strategy_b.base.claims != strategy_a.claims:
        raise ValueError("Strategy B must be derived from the exact Strategy-A composition")

    return P23A0JobEvaluation(
        source_job_id=strategy_a.source_job_id,
        strategy_a=evaluate_strategy_a(strategy_a),
        strategy_b=evaluate_strategy_b(strategy_b) if strategy_b is not None else None,
    )


def summarize_p23a0_evaluations(
    evaluations: tuple[P23A0JobEvaluation, ...],
) -> dict[str, Any]:
    """Aggregate mechanical experiment measurements across heterogeneous jobs."""

    strategy_b_evaluations = [
        evaluation.strategy_b
        for evaluation in evaluations
        if evaluation.strategy_b is not None
    ]
    total_a_claims = sum(evaluation.strategy_a.claim_count for evaluation in evaluations)
    total_a_requirements = sum(
        evaluation.strategy_a.requirement_claim_count for evaluation in evaluations
    )
    total_a_responsibilities = sum(
        evaluation.strategy_a.responsibility_claim_count for evaluation in evaluations
    )
    total_a_mapped = sum(
        evaluation.strategy_a.mapped_claim_count for evaluation in evaluations
    )
    total_a_mapped_requirements = sum(
        evaluation.strategy_a.mapped_requirement_claim_count
        for evaluation in evaluations
    )
    total_a_mapped_responsibilities = sum(
        evaluation.strategy_a.mapped_responsibility_claim_count
        for evaluation in evaluations
    )
    total_a_buckets = sum(evaluation.strategy_a.bucket_count for evaluation in evaluations)
    total_b_base_claims = sum(
        evaluation.base_claim_count for evaluation in strategy_b_evaluations
    )
    total_b_base_requirements = sum(
        evaluation.base_requirement_claim_count for evaluation in strategy_b_evaluations
    )
    total_b_base_responsibilities = sum(
        evaluation.base_responsibility_claim_count for evaluation in strategy_b_evaluations
    )
    total_b_grouped_claims = sum(
        evaluation.grouped_distinct_claim_count for evaluation in strategy_b_evaluations
    )
    total_b_grouped_requirements = sum(
        evaluation.grouped_requirement_claim_count for evaluation in strategy_b_evaluations
    )
    total_b_grouped_responsibilities = sum(
        evaluation.grouped_responsibility_claim_count
        for evaluation in strategy_b_evaluations
    )
    has_strategy_a_evidence = bool(evaluations)
    has_strategy_b_evidence = bool(strategy_b_evaluations)

    return {
        "job_count": len(evaluations),
        "strategy_b_available_job_count": len(strategy_b_evaluations),
        "strategy_a": {
            "total_claim_count": total_a_claims,
            "total_requirement_claim_count": total_a_requirements,
            "total_responsibility_claim_count": total_a_responsibilities,
            "total_mapped_claim_count": total_a_mapped,
            "total_mapped_requirement_claim_count": total_a_mapped_requirements,
            "total_mapped_responsibility_claim_count": total_a_mapped_responsibilities,
            "total_bucket_count": total_a_buckets,
            "canonical_mapping_coverage_ratio": _ratio(total_a_mapped, total_a_claims),
            "requirement_mapping_coverage_ratio": _ratio(
                total_a_mapped_requirements,
                total_a_requirements,
            ),
            "responsibility_mapping_coverage_ratio": _ratio(
                total_a_mapped_responsibilities,
                total_a_responsibilities,
            ),
            "bucket_per_claim_ratio": _ratio(total_a_buckets, total_a_claims),
            "all_exact_claims_recoverable": (
                all(
                    evaluation.strategy_a.exact_claim_recoverability
                    for evaluation in evaluations
                )
                if has_strategy_a_evidence
                else None
            ),
        },
        "strategy_b": {
            "total_base_claim_count": total_b_base_claims,
            "total_base_requirement_claim_count": total_b_base_requirements,
            "total_base_responsibility_claim_count": total_b_base_responsibilities,
            "total_grouped_distinct_claim_count": total_b_grouped_claims,
            "total_grouped_requirement_claim_count": total_b_grouped_requirements,
            "total_grouped_responsibility_claim_count": total_b_grouped_responsibilities,
            "grouped_claim_coverage_ratio": _ratio(
                total_b_grouped_claims,
                total_b_base_claims,
            ),
            "grouped_requirement_coverage_ratio": _ratio(
                total_b_grouped_requirements,
                total_b_base_requirements,
            ),
            "grouped_responsibility_coverage_ratio": _ratio(
                total_b_grouped_responsibilities,
                total_b_base_responsibilities,
            ),
            "total_suppressed_work_activity_count": sum(
                evaluation.suppressed_work_activity_count
                for evaluation in strategy_b_evaluations
            ),
            "total_duplicate_group_membership_count": sum(
                evaluation.duplicate_group_membership_count
                for evaluation in strategy_b_evaluations
            ),
            "all_exact_partitions_ok": (
                all(
                    evaluation.exact_partition_ok
                    for evaluation in strategy_b_evaluations
                )
                if has_strategy_b_evidence
                else None
            ),
            "all_work_activity_boundaries_ok": (
                all(
                    evaluation.work_activity_boundary_ok
                    for evaluation in strategy_b_evaluations
                )
                if has_strategy_b_evidence
                else None
            ),
        },
        "decision_authority": "none_mechanical_measurements_only",
    }


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 6)


def _claim_identity(claim: Any) -> tuple[int, str, int]:
    return claim.analysis_artifact_id, claim.claim_kind, claim.claim_index


__all__ = [
    "P23A0JobEvaluation",
    "P23A0StrategyAEvaluation",
    "P23A0StrategyBEvaluation",
    "evaluate_p23a0_job",
    "evaluate_strategy_a",
    "evaluate_strategy_b",
    "summarize_p23a0_evaluations",
]
