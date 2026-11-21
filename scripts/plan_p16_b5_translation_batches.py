#!/usr/bin/env python3
"""Private dry-run B5 translation batching preflight on EXPOSED development ads.

Does not fetch jobs, translate, run inference or write production data.
The historical B2v1 failure and B2v2 development replayers must pass first.
The private output includes source identifiers and MUST NOT be committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    B5_BATCH_CANDIDATE_VERSION,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import (
    interpret_original_source_candidate_v2,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
OUTPUT = PRIVATE / "B5_TRANSLATION_BATCH_PREFLIGHT.json"
SAFE_OUTPUT = (
    ROOT / "docs/working-memory/2026-11-21_p16_b5_translation_batch/"
    "SAFE_EXPOSED_TRANSLATION_BATCH_PREFLIGHT.json"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ValueError(f"B5 batch preflight already sealed: {path}")
    path.write_text(
        json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run() -> dict:
    old_verifier = runpy.run_path(str(ROOT / "scripts/verify_p16_b2v2_exposed_regressions.py"))[
        "verify"
    ]
    passed = old_verifier()
    if passed["status"] != "PASS_EXPOSED_B2V2_REGRESSION_REPLAY_NOT_B5_ACCEPTANCE":
        raise ValueError("The exact exposed B2v2 candidate has changed")
    prior = _load(PRIVATE / "B5_B2V2_B1_TRANSLATION_PREFLIGHT.json")
    b5_selection = _load(PRIVATE / "B5_SELECTION_FROZEN.json")
    b0_protocol = _load(ROOT / "docs/working-memory/2026-11-14_p16_b0/EVALUATION_PROTOCOL.json")
    snapshot = PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    if prior["frozen_candidate_engine_sha256"] != _sha(
        ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"
    ):
        raise ValueError("B2v2 candidate changed after frozen eight-job preflight")
    if b0_protocol["model_budget"]["B5_max_logical_paired_evaluation_calls"] != 80:
        raise ValueError("B5 paired analysis call budget changed")
    store = TranslationStore(snapshot)
    all_translatable = []
    native_total = excluded_total = total_items = 0
    per_case = []
    for selected in b5_selection["selected_primary"]:
        source_job_id = selected["source_job_id"]
        source = store.latest_source_version(source_job_id)
        if source is None:
            raise ValueError(f"Missing frozen source version: {source_job_id}")
        candidate = interpret_original_source_candidate_v2(source)
        selected_items = select_b3_items(source_job_id, candidate.items)
        translatable = prepare_source_batch_items(source, selected_items.translate_items)
        all_translatable.extend(translatable)
        native_total += len(selected_items.native_identity_items)
        excluded_total += len(selected_items.excluded_items)
        total_items += len(candidate.items)
        per_case.append(
            {
                "source_job_id": source_job_id,
                "source_semantic_sha256": source.semantic_sha256,
                "all_source_items": len(candidate.items),
                "translation_eligible_logical_items": len(translatable),
                "native_original_language_items": len(selected_items.native_identity_items),
                "excluded_context_items": len(selected_items.excluded_items),
            }
        )
    if (
        len(all_translatable) != prior["candidate_total_counts"]["translation_eligible_items"]
        or native_total != prior["candidate_total_counts"]["native_source_identity_items"]
        or excluded_total != prior["candidate_total_counts"]["excluded_context_items"]
        or total_items != prior["candidate_total_counts"]["all_items"]
    ):
        raise ValueError("Original exposed source item inventory changed")
    metrics = []
    plans = {}
    for max_items in (1, 2, 3, 4):
        plan = plan_source_batches(
            all_translatable,
            max_batch_items=max_items,
            max_batch_characters=1200,
        )
        plans[max_items] = plan
        counter = Counter(len(batch.items) for batch in plan.batches)
        metrics.append(
            {
                "max_items_per_request": max_items,
                "max_source_chars_per_request": 1200,
                "logical_items": plan.total_logical_items,
                "planned_physical_request_batches": len(plan.batches),
                "deferred_oversized_source_items": len(plan.deferred_oversized),
                "number_of_batches_by_cardinality": dict(sorted(counter.items())),
                "plan_sha256": plan.plan_sha256,
                "planned_count_not_observed_model_calls": True,
            }
        )
    selected_plan = plans[3]
    if (
        len(selected_plan.batches) != 74
        or selected_plan.total_logical_items != 142
        or selected_plan.deferred_oversized
    ):
        raise ValueError("B5 exposed preflight expectation drifted")
    # Batch boundaries must remain within each source, modality and heading.
    for batch in selected_plan.batches:
        keys = {
            (x.source_job_id, x.source_semantic_sha256, x.category, x.strength, x.heading_sha256)
            for x in batch.items
        }
        if len(keys) != 1:
            raise ValueError("Source or strength crossing in planned local batch")
    private_result = {
        "contract": B5_BATCH_CANDIDATE_VERSION,
        "preflight_at_utc": datetime.now(UTC).isoformat(),
        "cohort_status": "EXPOSED_DEVELOPMENT_CASES_NOT_UNSEEN",
        "model_calls_issued": 0,
        "http_requests_issued": 0,
        "production_writes": 0,
        "source_job_acquisition": 0,
        "per_case": per_case,
        "candidate_source_items": total_items,
        "native_identity_items": native_total,
        "excluded_context_items": excluded_total,
        "eligible_logical_translation_items": len(all_translatable),
        "physical_batch_candidates": metrics,
        "selected_candidate_batch_max_items": 3,
        "selected_candidate_plan_sha256": selected_plan.plan_sha256,
        "selected_candidate_physical_batches": len(selected_plan.batches),
        "selected_candidate_logical_items": selected_plan.total_logical_items,
        "selected_batch_sources": [
            {
                "batch_id": batch.batch_id,
                "source_job_id": batch.source_job_id,
                "member_anchor_ids": [x.source_anchor_id for x in batch.items],
                "member_source_span_sha256": [x.source_span_sha256 for x in batch.items],
                "member_source_semantic_sha256": [x.source_semantic_sha256 for x in batch.items],
                "member_categories": [x.category for x in batch.items],
                "member_strengths": [x.strength for x in batch.items],
                "member_heading_sha256": [x.heading_sha256 for x in batch.items],
                "total_source_chars": batch.total_source_characters,
            }
            for batch in selected_plan.batches
        ],
        "historical_B3_64_logical_source_item_limit": (
            b0_protocol["model_budget"]["B3_max_logical_source_item_calls"]
        ),
        "B5_80_paired_analysis_calls_not_translation_budget": (
            b0_protocol["model_budget"]["B5_max_logical_paired_evaluation_calls"]
        ),
        "B5_translation_model_budget": "NOT_YET_SEPARATELY_APPROVED",
        "unseen_B5_or_B6_acceptance": False,
        "original_parser_sha256": _sha(ROOT / "src/jobhunter/source_item_candidate_b2.py"),
        "B2v2_engine_sha256": _sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"),
        "batch_candidate_engine_sha256": _sha(
            ROOT / "src/jobhunter/source_bound_translation_batch_b5.py"
        ),
        "source_snapshot_sha256": _sha(snapshot),
        "B0_original_protocol_sha256": _sha(
            ROOT / "docs/working-memory/2026-11-14_p16_b0/EVALUATION_PROTOCOL.json"
        ),
        "production_db_sha256": _sha(ROOT / "data/jobhunter.sqlite3"),
        "public_corpus_manifest_sha256": _sha(ROOT / "corpus/manifest.json"),
    }
    _json_write(OUTPUT, private_result)
    safe = {
        key: value
        for key, value in private_result.items()
        if key not in {"per_case", "selected_batch_sources", "source_snapshot_sha256"}
    }
    safe["private_plan_receipt_sha256"] = _sha(OUTPUT)
    safe["source_provenance_private_not_committed"] = True
    safe["no_sample_model_quality_claim"] = True
    safe["next_gate"] = (
        "bound_one_small_live_local_exposed_pilot_if_provider_available;"
        "assess_translation_semantic_fidelity_and_failure_rates;"
        "explicit_translation_budget_then_new_unseen_B5"
    )
    _json_write(SAFE_OUTPUT, safe)
    return safe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    safe = run()
    print(
        json.dumps(
            {
                "status": "PASS_OFFLINE_BATCH_PLANNING_EXPOSED_NO_MODEL",
                "cohort_status": safe["cohort_status"],
                "model_calls_issued": safe["model_calls_issued"],
                "eligible_logical_translation_items": safe["eligible_logical_translation_items"],
                "candidate_batch_options": safe["physical_batch_candidates"],
                "selected_candidate_physical_batches": safe["selected_candidate_physical_batches"],
                "B5_translation_model_budget": safe["B5_translation_model_budget"],
            },
            sort_keys=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
