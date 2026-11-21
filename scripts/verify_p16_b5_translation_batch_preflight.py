#!/usr/bin/env python3
"""Replay B5 candidate-only source-bound batching plan over frozen exposed jobs."""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    B5_BATCH_CANDIDATE_VERSION,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
SAFE = (
    ROOT
    / "docs/working-memory/2026-11-21_p16_b5_translation_batch"
    / "SAFE_EXPOSED_TRANSLATION_BATCH_PREFLIGHT.json"
)
PREFLIGHT = PRIVATE / "B5_TRANSLATION_BATCH_PREFLIGHT.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify() -> dict:
    b2 = runpy.run_path(str(ROOT / "scripts/verify_p16_b2v2_exposed_regressions.py"))["verify"]()
    if b2["status"] != "PASS_EXPOSED_B2V2_REGRESSION_REPLAY_NOT_B5_ACCEPTANCE":
        raise ValueError("B2v2 historical exposed comparison changed")
    record = read(PREFLIGHT)
    safe = read(SAFE)
    if record["contract"] != B5_BATCH_CANDIDATE_VERSION:
        raise ValueError("Translation batching contract changed")
    if safe["private_plan_receipt_sha256"] != sha(PREFLIGHT):
        raise ValueError("Private planner receipt changed")
    for path, field in (
        (
            ROOT / "src/jobhunter/source_bound_translation_batch_b5.py",
            "batch_candidate_engine_sha256",
        ),
        (ROOT / "src/jobhunter/source_item_candidate_b2_v2.py", "B2v2_engine_sha256"),
        (ROOT / "src/jobhunter/source_item_candidate_b2.py", "original_parser_sha256"),
        (ROOT / "data/jobhunter.sqlite3", "production_db_sha256"),
        (ROOT / "corpus/manifest.json", "public_corpus_manifest_sha256"),
        (PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3", "source_snapshot_sha256"),
        (
            ROOT / "docs/working-memory/2026-11-14_p16_b0/EVALUATION_PROTOCOL.json",
            "B0_original_protocol_sha256",
        ),
    ):
        if record[field] != sha(path):
            raise ValueError(f"Frozen batching input or production SHA drift: {field}")
    if any(
        record[key] != 0
        for key in (
            "model_calls_issued",
            "http_requests_issued",
            "production_writes",
            "source_job_acquisition",
        )
    ):
        raise ValueError("A dry-run cannot claim live translation")
    selected = read(PRIVATE / "B5_SELECTION_FROZEN.json")
    source_store = TranslationStore(PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3")
    originals = []
    for case in selected["selected_primary"]:
        source = source_store.latest_source_version(case["source_job_id"])
        if source is None:
            raise ValueError("Missing frozen source")
        candidate = interpret_original_source_candidate_v2(source)
        selected_items = select_b3_items(source.source_job_id, candidate.items)
        originals.extend(prepare_source_batch_items(source, selected_items.translate_items))
    if len(originals) != record["eligible_logical_translation_items"]:
        raise ValueError("Original translation denominator changed")
    batches = plan_source_batches(originals, max_batch_items=3, max_batch_characters=1200)
    if (
        batches.plan_sha256 != record["selected_candidate_plan_sha256"]
        or len(batches.batches) != record["selected_candidate_physical_batches"]
        or batches.deferred_oversized
    ):
        raise ValueError("Batch planner produced different result")
    saved = record["selected_batch_sources"]
    if [b.batch_id for b in batches.batches] != [x["batch_id"] for x in saved]:
        raise ValueError("Batch membership identity changed")
    for planned, receipt in zip(batches.batches, saved, strict=True):
        if (
            [x.source_anchor_id for x in planned.items] != receipt["member_anchor_ids"]
            or [x.source_span_sha256 for x in planned.items] != receipt["member_source_span_sha256"]
            or [x.category for x in planned.items] != receipt["member_categories"]
            or [x.strength for x in planned.items] != receipt["member_strengths"]
        ):
            raise ValueError("Batch member original source/strength association drifted")
    for setting in (1, 2, 3, 4):
        plan = plan_source_batches(originals, max_batch_items=setting, max_batch_characters=1200)
        metric = next(
            row
            for row in record["physical_batch_candidates"]
            if row["max_items_per_request"] == setting
        )
        if (
            plan.plan_sha256 != metric["plan_sha256"]
            or len(plan.batches) != metric["planned_physical_request_batches"]
            or plan.total_logical_items != metric["logical_items"]
        ):
            raise ValueError("Alternative batching strategy preflight drifted")
    if (
        record["eligible_logical_translation_items"] != 142
        or len(batches.batches) != 74
        or record["B5_translation_model_budget"] != "NOT_YET_SEPARATELY_APPROVED"
        or record["unseen_B5_or_B6_acceptance"] is not False
    ):
        raise ValueError("Unseen inference/acceptance or logical budget overclaim")
    return {
        "status": "PASS_OFFLINE_BATCH_PREFLIGHT_REPLAY_NOT_MODEL_QUALITY",
        "logical_source_items": len(originals),
        "candidate_physical_batches_at_3": len(batches.batches),
        "deferred_originals": len(batches.deferred_oversized),
        "all_source_anchor_and_strength_mappings_verified": True,
        "local_model_calls": 0,
        "B5_unseen_claim": False,
        "production_state_unchanged": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
