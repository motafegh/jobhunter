"""Run the non-authoritative P2.3A-0 Strategy A composition on local evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    build_canonical_registry_review_reader,
)
from jobhunter.config import Settings
from jobhunter.p2_3a0_profile_experiment import compose_p23a0_strategy_a_for_job

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


def run(config_path: Path, job_ids: tuple[str, ...]) -> dict[str, Any]:
    settings = Settings.load(config_path)
    reader = build_canonical_registry_review_reader(settings)
    jobs: list[dict[str, Any]] = []

    for job_id in job_ids:
        composition = compose_p23a0_strategy_a_for_job(reader, job_id)
        jobs.append(
            {
                "source_job_id": composition.source_job_id,
                "measurements": {
                    "claim_count": composition.claim_count,
                    "requirement_claim_count": composition.requirement_claim_count,
                    "responsibility_claim_count": composition.responsibility_claim_count,
                    "mapped_claim_count": composition.mapped_claim_count,
                    "bucket_count": len(composition.buckets),
                    "canonical_bucket_count": composition.canonical_bucket_count,
                    "source_local_bucket_count": composition.source_local_bucket_count,
                    "deterministic_grouping_savings": (
                        composition.deterministic_grouping_savings
                    ),
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
        )

    return {
        "experiment": "P2.3A-0",
        "strategy": "A — deterministic P1.6 + reviewed Registry projection",
        "authority": "experimental_non_authoritative",
        "persistence": "none",
        "model_calls": 0,
        "jobs": jobs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export the read-only P2.3A-0 Strategy A composition for accepted/current "
            "P1.6 claims. This does not mutate Registry or authorize P2.3."
        )
    )
    parser.add_argument(
        "job_ids",
        nargs="*",
        help="Source job ids; defaults to the six snapshot-15 acceptance jobs.",
    )
    parser.add_argument("--config", type=Path, default=Path("jobhunter.toml"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    job_ids = tuple(args.job_ids) if args.job_ids else DEFAULT_JOB_IDS
    try:
        payload = run(args.config, job_ids)
    except (OSError, ValueError, LookupError) as exc:
        parser.exit(1, f"P2.3A-0 Strategy A failed: {exc}\n")

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
