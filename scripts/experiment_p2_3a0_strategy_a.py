"""Run the non-authoritative P2.3A-0 composition experiment on local evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    build_canonical_registry_review_reader,
)
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.p2_3a0_evaluation import (
    P23A0JobEvaluation,
    evaluate_p23a0_job,
    summarize_p23a0_evaluations,
)
from jobhunter.p2_3a0_profile_experiment import (
    P23A0StrategyAComposition,
    P23A0StrategyBComposition,
    compose_p23a0_strategy_a_for_job,
    compose_p23a0_strategy_b_from_public_capability,
)

DEFAULT_JOB_IDS = ("tvMm", "tNVe", "tmvA", "tjgi", "t7ck", "t7Ay")


def _claim_payload(claim: CanonicalClaimReviewItem) -> dict[str, Any]:
    mapping = claim.mapping
    return {
        "analysis_artifact_id": claim.analysis_artifact_id,
        "job_detail_version_id": claim.job_detail_version_id,
        "translation_artifact_id": claim.translation_artifact_id,
        "claim_kind": claim.claim_kind,
        "claim_index": claim.claim_index,
        "source_text": claim.source_text,
        "evidence": claim.evidence,
        "concept_type": claim.concept_type,
        "strength": claim.strength,
        "depth_signal": claim.depth_signal,
        "registry_state": claim.mapping_state,
        "canonical_concept_id": (
            mapping.canonical_concept_id if mapping is not None else None
        ),
    }


def _strategy_a_payload(composition: P23A0StrategyAComposition) -> dict[str, Any]:
    return {
        "measurements": {
            "claim_count": composition.claim_count,
            "requirement_claim_count": composition.requirement_claim_count,
            "responsibility_claim_count": composition.responsibility_claim_count,
            "mapped_claim_count": composition.mapped_claim_count,
            "bucket_count": len(composition.buckets),
            "canonical_bucket_count": composition.canonical_bucket_count,
            "source_local_bucket_count": composition.source_local_bucket_count,
            "deterministic_grouping_savings": composition.deterministic_grouping_savings,
        },
        "buckets": [
            {
                "key": bucket.key,
                "basis": bucket.basis,
                "canonical_concept_id": bucket.canonical_concept_id,
                "claims": [_claim_payload(claim) for claim in bucket.claims],
            }
            for bucket in composition.buckets
        ],
    }


def _strategy_b_payload(composition: P23A0StrategyBComposition) -> dict[str, Any]:
    return {
        "status": "available_from_explicit_public_capability_v9",
        "capability_artifact_id": composition.capability_artifact_id,
        "capability_model": composition.capability_model,
        "measurements": {
            "group_count": len(composition.groups),
            "grouped_distinct_claim_count": composition.grouped_claim_count,
            "ungrouped_claim_count": len(composition.ungrouped_claims),
            "reviewed_canonical_concept_count": len(composition.canonical_concept_ids),
            "suppressed_work_activity_count": composition.suppressed_work_activity_count,
        },
        "reviewed_canonical_concept_ids": list(composition.canonical_concept_ids),
        "groups": [
            {
                "job_local_label": group.job_local_label,
                "summary": group.summary,
                "canonical_concept_ids_from_exact_mapped_claims": list(
                    group.canonical_concept_ids
                ),
                "requirement_strength": group.requirement_strength,
                "requirement_claim_count": group.requirement_claim_count,
                "responsibility_claim_count": group.responsibility_claim_count,
                "claims": [_claim_payload(claim) for claim in group.claims],
                "depth_signals": list(group.depth_signals),
                "work_activities": list(group.work_activities),
                "suppressed_work_activity_count": group.suppressed_work_activity_count,
                "sub_capabilities": list(group.sub_capabilities),
                "underlying_knowledge": list(group.underlying_knowledge),
                "operational_practices": list(group.operational_practices),
                "operational_context": list(group.operational_context),
                "unknown_scope": list(group.unknown_scope),
                "independence_expectation": group.independence_expectation,
                "overall_confidence": group.overall_confidence,
            }
            for group in composition.groups
        ],
        "ungrouped_claims": [
            _claim_payload(claim) for claim in composition.ungrouped_claims
        ],
    }


def run(
    config_path: Path,
    job_ids: tuple[str, ...],
    *,
    corpus_root: Path = Path("corpus"),
    include_strategy_b: bool = True,
) -> dict[str, Any]:
    settings = Settings.load(config_path)
    reader = build_canonical_registry_review_reader(settings)
    jobs: list[dict[str, Any]] = []
    evaluations: list[P23A0JobEvaluation] = []

    for job_id in job_ids:
        composition = compose_p23a0_strategy_a_for_job(reader, job_id)
        strategy_b: P23A0StrategyBComposition | None = None
        job_payload: dict[str, Any] = {
            "source_job_id": composition.source_job_id,
            "strategy_a": _strategy_a_payload(composition),
        }
        if include_strategy_b:
            capability_path = corpus_root / "jobs" / job_id / "capability.json"
            if capability_path.is_file():
                public_capability = json.loads(capability_path.read_text(encoding="utf-8"))
                strategy_b = compose_p23a0_strategy_b_from_public_capability(
                    composition,
                    public_capability,
                )
                job_payload["strategy_b"] = _strategy_b_payload(strategy_b)
            else:
                job_payload["strategy_b"] = {
                    "status": "unavailable_no_accepted_public_capability_v9",
                }

        evaluation = evaluate_p23a0_job(composition, strategy_b)
        evaluations.append(evaluation)
        job_payload["evaluation"] = evaluation.to_payload()
        jobs.append(job_payload)

    return {
        "experiment": "P2.3A-0",
        "strategies": {
            "A": "deterministic accepted/current P1.6 + reviewed Registry projection",
            "B": (
                "Strategy A + explicit accepted/current public Capability-v9 job-local "
                "organization when available"
            ),
        },
        "authority": "experimental_non_authoritative",
        "persistence": "none",
        "model_calls": 0,
        "evaluation_summary": summarize_p23a0_evaluations(tuple(evaluations)),
        "jobs": jobs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export read-only P2.3A-0 Strategy A and optional accepted-public "
            "Capability-v9 Strategy B composition plus deterministic evaluation "
            "metrics. This does not mutate Registry or authorize P2.3."
        )
    )
    parser.add_argument(
        "job_ids",
        nargs="*",
        help="Source job ids; defaults to the six snapshot-15 acceptance jobs.",
    )
    parser.add_argument("--config", type=Path, default=Path("jobhunter.toml"))
    parser.add_argument("--corpus-root", type=Path, default=Path("corpus"))
    parser.add_argument(
        "--strategy-a-only",
        action="store_true",
        help="Do not overlay an accepted public Capability-v9 projection.",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    job_ids = tuple(args.job_ids) if args.job_ids else DEFAULT_JOB_IDS
    try:
        payload = run(
            args.config,
            job_ids,
            corpus_root=args.corpus_root,
            include_strategy_b=not args.strategy_a_only,
        )
    except (ConfigLoadError, OSError, ValueError, LookupError, json.JSONDecodeError) as exc:
        parser.exit(1, f"P2.3A-0 composition experiment failed: {exc}\n")

    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output is None:
        print(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
