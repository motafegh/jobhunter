"""Verify sealed B5 source-first gate using unchanged B2 and untouched source database.

No network access, translation, LLM, baseline inference or persistence writes.
"""

from __future__ import annotations

import hashlib
import json
import runpy
import sqlite3
from pathlib import Path

from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def verify() -> dict:
    preflight = load(PRIVATE / "PREFLIGHT.json")
    selection = load(PRIVATE / "B5_SELECTION_FROZEN.json")
    source = load(PRIVATE / "B5_SOURCE_FROZEN_BEFORE_REVIEW.json")
    review = load(PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    result = load(PRIVATE / "B5_B2_SOURCE_GATE_RESULT.json")
    snapshot = PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    expected = {
        "selection_file_sha256": sha(PRIVATE / "B5_SELECTION_FROZEN.json"),
        "snapshot_database_sha256": sha(snapshot),
        "source_review_sha256": sha(PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"),
        "code_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2.py"),
    }
    if source["selection_file_sha256"] != expected["selection_file_sha256"]:
        raise ValueError("Selected job list was modified after original details")
    if review["frozen_selection_sha256"] != expected["selection_file_sha256"]:
        raise ValueError("Source-first assessment was not tied to frozen selected jobs")
    if source["snapshot_database_sha256"] != expected["snapshot_database_sha256"]:
        raise ValueError("Original source backup changed")
    if review["frozen_source_snapshot_sha256"] != expected["snapshot_database_sha256"]:
        raise ValueError("Source-first review evaluated a different original database")
    if review["frozen_source_manifest_sha256"] != sha(
        PRIVATE / "B5_SOURCE_FROZEN_BEFORE_REVIEW.json"
    ):
        raise ValueError("Source manifest changed after review")
    for key, path in (
        ("frozen_selection_sha256", "B5_SELECTION_FROZEN.json"),
        ("frozen_source_review_sha256", "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"),
        ("frozen_snapshot_sha256", "B5_8_SOURCE_SNAPSHOT.sqlite3"),
    ):
        if result[key] != sha(PRIVATE / path):
            raise ValueError(f"B5 evaluation input fingerprint changed: {key}")
    if result["b2_code_sha256"] != expected["code_sha256"]:
        raise ValueError("Frozen B5 B2 evaluator implementation changed")
    if preflight["snapshot_source_database_sha256"] != sha(ROOT / "data/jobhunter.sqlite3"):
        raise ValueError("Production application database drifted during B5")
    if selection["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json"):
        raise ValueError("Production public corpus drifted during B5")
    if selection["B0_exclusion_sha256"] != sha(
        ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/"
        "frozen/EXCLUSION_KNOWN_JOB_IDS_PRIVATE.json"
    ):
        raise ValueError("Known-exposure source index changed")
    with sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True) as con:
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("B5 isolated snapshot integrity error")
        if con.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("B5 isolated snapshot FK error")
        if con.execute("select count(*) from job_detail_versions").fetchone()[0] != 8:
            raise ValueError("B5 snapshot has wrong count of original pages")
        if con.execute("select count(*) from job_analysis_artifacts").fetchone()[0]:
            raise ValueError("B5 source snapshot contains candidate analysis artifacts")
    if (
        review["job_count"] != 8
        or review["anchor_count"] != 93
        or review["model_results_inspected_before_review"] is not False
        or review["source_only_reviewed_before_any_B5_candidate_inference"] is not True
        or review["independent_blind_human_review"] is not False
        or review["full_statement_denominator_established"] is not False
    ):
        raise ValueError("B5 source-only review authority or denominator drifted")
    if selection["total_original_detail_pages_fetched_before_selection"] != 0:
        raise ValueError("Source details viewed before metadata-based selection")
    store = TranslationStore(snapshot)
    versions = {}
    for rec in source["entries"]:
        job_id = rec["source_job_id"]
        version = store.latest_source_version(job_id)
        if version is None or version.semantic_sha256 != rec["source_semantic_sha256"]:
            raise ValueError(f"B5 original changed: {job_id}")
        versions[job_id] = version
    evaluator = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))
    replay = evaluator["evaluate_source_gate"](
        frozen=selection,
        review=review,
        source_versions=versions,
        engine=interpret_original_source_candidate,
    )
    frozen_result = {
        k: v
        for k, v in result.items()
        if k
        not in {
            "evaluation_time_utc",
            "frozen_selection_sha256",
            "frozen_source_review_sha256",
            "frozen_snapshot_sha256",
            "b2_code_sha256",
        }
    }
    replay_result = {k: v for k, v in replay.items() if k != "evaluation_time_utc"}
    if replay_result != frozen_result:
        raise ValueError("B5 frozen source-first/B2 evaluation replay differs")
    counts = result["counts"]
    if (
        result["disposition"] != "BLOCKED_UPSTREAM_SOURCE_SEMANTICS"
        or counts["frozen_source_first_anchor_count"] != 93
        or counts["source_type_anchor_count"] != 86
        or counts["candidate_role_match_anchor_count"] != 25
        or counts["candidate_role_mismatch_anchor_count"] != 58
        or counts["explicit_duty_missed_anchor_count"] != 19
        or counts["optional_or_negative_required_overstatement_count"] != 2
        or counts["multi_specialty_alternative_structure_missing_jobs"] != 1
        or counts["job_count_with_critical_structural_or_category_gaps"] != 7
        or result["new_b3_translation_requests"] != 0
        or result["new_b4_analysis_requests"] != 0
        or result["new_v30_baseline_requests"] != 0
        or result["accepted_facts_promoted"] != 0
        or result["production_database_written"] is not False
    ):
        raise ValueError("B5 safety/stop thresholds changed")
    return {
        "status": "PASS_REPLAY_OF_B5_UPSTREAM_SEMANTIC_BLOCKER",
        "promotion": "BLOCKED",
        "case_count": 8,
        "original_html_verified": source["source_files_verified"],
        "sealed_source_only_anchors": review["anchor_count"],
        "selected_frozen_source_sha256": sha(snapshot),
        "source_role_mismatches": counts["candidate_role_mismatch_anchor_count"],
        "false_required_optional_anchors": (
            counts["optional_or_negative_required_overstatement_count"]
        ),
        "missing_specialty_alternative_jobs": (
            counts["multi_specialty_alternative_structure_missing_jobs"]
        ),
        "production_database_unchanged": True,
        "unseen_evaluation_exposed_after_comparison": True,
        "next_validation_requires_new_fresh_cohort": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
