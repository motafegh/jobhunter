#!/usr/bin/env python3
"""Read-only verifier for the sealed, *exposed* B2v2 regression comparison.

Historical B2v1 failure evidence and B4v5 candidate presentation are not
regenerated. No provider, HTTP, production database or acceptance writes.
"""

from __future__ import annotations

import hashlib
import json
import runpy
from pathlib import Path

from jobhunter.source_item_candidate_b2_v2 import (
    B2V2_ENGINE,
    build_candidate_eligibility_logic_v2,
    interpret_original_source_candidate_v2,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
RESULT = PRIVATE / "B5_B2V2_EXPOSED_COMPARISON.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify() -> dict:
    historical = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_source_gate.py"))["verify"]()
    if historical["status"] != "PASS_REPLAY_OF_B5_UPSTREAM_SEMANTIC_BLOCKER":
        raise ValueError("Old B2v1 source gate was mutated")
    old = load(PRIVATE / "B5_B2_SOURCE_GATE_RESULT.json")
    new = load(RESULT)
    if new["engine"] != B2V2_ENGINE or new["fresh_unseen_evaluation"] is not False:
        raise ValueError("Exposed B2v2 evidence mislabeled as unseen validation")
    if new["original_parser_source_sha256"] != sha(
        ROOT / "src/jobhunter/source_item_candidate_b2.py"
    ):
        raise ValueError("Historical B2v1 parser was altered")
    if new["new_parser_source_sha256"] != sha(
        ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"
    ):
        raise ValueError("B2v2 parser changed after candidate regression sealed")
    if new["old_b2v1_gate_hash_sha256"] != sha(PRIVATE / "B5_B2_SOURCE_GATE_RESULT.json"):
        raise ValueError("Old B2v1 B5 decision changed after new candidate")
    if new["old_counts"] != old["counts"]:
        raise ValueError("Historical B2v1 comparison counts no longer align")
    if new["frozen_original_source_snapshot_sha256"] != sha(
        PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    ):
        raise ValueError("Original B5 source snapshot no longer frozen")
    if new["sealed_source_review_sha256"] != sha(
        PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"
    ):
        raise ValueError("Original-source-first review changed")
    preflight = load(PRIVATE / "PREFLIGHT.json")
    if sha(ROOT / "data/jobhunter.sqlite3") != preflight["snapshot_source_database_sha256"]:
        raise ValueError("B2v2 altered production database")
    selected = load(PRIVATE / "B5_SELECTION_FROZEN.json")
    if selected["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json"):
        raise ValueError("B2v2 altered committed public corpus")
    frozen = load(PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    store = TranslationStore(PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3")
    versions = {}
    for j in [x["source_job_id"] for x in selected["selected_primary"]]:
        version = store.latest_source_version(j)
        if version is None:
            raise ValueError(f"Source evidence missing: {j}")
        versions[j] = version
    evaluator = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    replay = evaluator(
        frozen=selected,
        review=frozen,
        source_versions=versions,
        engine=interpret_original_source_candidate_v2,
    )
    # Evaluation timestamp is intentionally not a deterministic result.
    replay.pop("evaluation_time_utc")
    stored = dict(new["full_new_selected_anchor_comparison"])
    stored.pop("evaluation_time_utc")
    if stored != replay:
        raise ValueError("B2v2 per-anchor regression replay changed")
    if replay["counts"] != new["new_counts"]:
        raise ValueError("B2v2 counter regression")
    preserved = []
    for item in new["prior_B0_graph_regressions"]:
        job = item["source_job_id"]
        source = TranslationStore(
            ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/"
            "frozen/exposed_original_snapshot.sqlite3"
        ).latest_source_version(job)
        if source is None or source.semantic_sha256 != item["source_semantic_sha256"]:
            raise ValueError(f"Previous B0 original changed: {job}")
        candidate = interpret_original_source_candidate_v2(source)
        logic = build_candidate_eligibility_logic_v2(source, candidate)
        if [g.graph_id for g in logic.graphs] != item["revised_graph_names"] or sum(
            c.category == "work_duty" for c in candidate.items
        ) != item["revised_duty_count"]:
            raise ValueError(f"Previous accepted bounded B0 regression changed: {job}")
        preserved.append(job)
    safety = {
        "status": "PASS_EXPOSED_B2V2_REGRESSION_REPLAY_NOT_B5_ACCEPTANCE",
        "selected_source_job_count": len(versions),
        "selected_source_first_anchor_count": new["new_counts"]["frozen_source_first_anchor_count"],
        "old_role_category_matches": new["old_counts"]["candidate_role_match_anchor_count"],
        "new_role_category_matches": new["new_counts"]["candidate_role_match_anchor_count"],
        "new_role_category_mismatches": new["new_counts"]["candidate_role_mismatch_anchor_count"],
        "new_false_required_optional_count": new["new_counts"][
            "optional_or_negative_required_overstatement_count"
        ],
        "new_missing_explicit_duty_anchor_count": new["new_counts"][
            "explicit_duty_missed_anchor_count"
        ],
        "previous_B0_regression_jobs_preserved": len(preserved),
        "new_full_unseen_B5_verification": False,
        "B6_promotion": "not_authorized",
        "source_or_model_network_calls": 0,
        "production_database_unchanged": True,
    }
    if (
        safety["new_false_required_optional_count"]
        or safety["new_missing_explicit_duty_anchor_count"]
    ):
        raise ValueError("Safety-critical exposed source regression")
    return safety


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
