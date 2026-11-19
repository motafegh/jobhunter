"""Verify the sealed, private P1.6 B4 bounded source-only/partial milestone.

No model calls and no production database writes. Reports only safe counts.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/local-acceptance/p16-stage-b4-2026-11-19/primary-v4c"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
B2 = ROOT / (
    "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5/"
    "PRIVATE_B2_CANDIDATES.json"
)
B3 = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1/PRIVATE_B3_CANDIDATES.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Expected JSON object: {path.name}")
    return obj


def verify() -> dict:
    manifest = read(OUT / "run_manifest.json")
    metrics = read(OUT / "B4_SAFE_METRICS.json")
    audit = read(OUT / "B4_FINAL_AUDIT.json")
    records = read(OUT / "PRIVATE_B4_CANDIDATES.json")
    comparison = read(OUT / "B4_BASELINE_COMPARISON.json")
    expected_hashes = {
        "source_database_sha256": digest(B0),
        "b2_candidate_sha256": digest(B2),
        "b3_candidate_sha256": digest(B3),
        "run_manifest_sha256": digest(OUT / "run_manifest.json"),
        "private_candidate_sha256": digest(OUT / "PRIVATE_B4_CANDIDATES.json"),
        "baseline_comparison_sha256": digest(OUT / "B4_BASELINE_COMPARISON.json"),
        "safe_metrics_sha256": digest(OUT / "B4_SAFE_METRICS.json"),
        "briefs_markdown_sha256": digest(OUT / "B4_BRIEFS.md"),
        "comparison_database_sha256": digest(OUT / "comparison.sqlite3"),
    }
    for name, expected in expected_hashes.items():
        if audit.get(name) != expected:
            raise ValueError(f"Final-audit hash mismatch: {name}")
    for name, filename in (
        ("runner", "scripts/run_p16_b4_job_understanding.py"),
        ("module", "src/jobhunter/source_job_understanding_b4.py"),
        ("schema", "docs/contracts/p16-stage-b4/job_understanding_response.schema.json"),
    ):
        if manifest["code_sha256"][name] != digest(ROOT / filename):
            raise ValueError(f"Historical B4 code/schema fingerprint drifted: {name}")

    expected_cases = ("tNhZ", "tMps", "tNDx", "tMjm")
    if tuple(case["source_job_id"] for case in records["cases"]) != expected_cases:
        raise ValueError("B4 case inventory changed")
    expected_outcomes = {
        "tNhZ": ("completed", "partial_candidate"),
        "tMps": ("failed", "failed"),
        "tNDx": ("completed", "partial_candidate"),
        "tMjm": ("skipped", "source_only_candidate"),
    }
    for case in records["cases"]:
        job_id = case["source_job_id"]
        brief = case["candidate"]
        if (case["attempt_outcome"], brief["analysis_outcome"]) != expected_outcomes[job_id]:
            raise ValueError(f"B4 attempt/outcome changed: {job_id}")
        if brief["downstream_authority"] != "none":
            raise ValueError("Unexpected downstream authority")
        all_ids = {item["item_id"] for item in brief["items"]}
        selected = {item["item_id"] for item in brief["items"] if item["translation"] is not None}
        source_only = brief["source_only_brief"]
        fallback_ids = {
            item["source_item_id"]
            for items in source_only["category_groups"].values()
            for item in items
        }
        if selected != fallback_ids or source_only["item_count"] != len(selected):
            raise ValueError(f"B4 source-only coverage drifted: {job_id}")
        if brief["brief"] is not None:
            candidate = brief["brief"]
            if candidate["source_reference_state"] != "canonical_source_item_ids_resolved":
                raise ValueError("Model references were not restored to canonical IDs")
            if set(candidate["referenced_item_ids"]) - selected:
                raise ValueError("Model brief cites unknown or excluded source item")
            for section in (
                "work_activities",
                "expectation_summaries",
                "work_implied_capabilities",
                "open_questions",
            ):
                for claim in candidate[section]:
                    if set(claim["source_item_ids"]) - selected:
                        raise ValueError(f"Invalid source citation in {section}")
            if set(candidate["role_summary"]["source_item_ids"]) - selected:
                raise ValueError("Invalid role-summary citation")
        if any(item["item_id"] not in all_ids for item in brief["coverage_ledger"]):
            raise ValueError("Coverage ledger cites unowned item")
        if len(brief["coverage_ledger"]) != len(brief["items"]):
            raise ValueError("Incomplete source coverage ledger")
    if metrics["model_requests_started"] != 3 or metrics["model_requests_validated"] != 2:
        raise ValueError("Expected model request/validation counts changed")
    if (
        metrics["source_only_cases_without_model_call"] != 1
        or metrics["quarantined_model_fragments"] != 4
        or metrics["accepted_facts_promoted"] != 0
        or metrics["production_database_written"] is not False
        or metrics["unseen_generalization_established"] is not False
        or metrics["reasoning_content_retained"] is not False
    ):
        raise ValueError("B4 authority or filter boundary changed")
    if metrics["baseline_counts"] != {
        "v30_failed_no_artifact": 3,
        "v30_rejected_no_valid_artifact": 1,
        "v9_artifact_present": 1,
    }:
        raise ValueError("Frozen v30/v9 comparison changed")
    if len(comparison) != 4:
        raise ValueError("Baseline per-case denominator changed")
    for suffix in ("-wal", "-shm"):
        if Path(f"{OUT / 'comparison.sqlite3'}{suffix}").exists():
            raise ValueError("Comparison database is not standalone")
    with sqlite3.connect(f"file:{OUT / 'comparison.sqlite3'}?mode=ro", uri=True) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign = conn.execute("PRAGMA foreign_key_check").fetchall()
        journal = conn.execute("PRAGMA journal_mode").fetchone()[0]
        row_count = conn.execute("SELECT COUNT(*) FROM p16_b4_candidate_briefs").fetchone()[0]
        attempt_count = conn.execute("SELECT COUNT(*) FROM p16_b4_attempts").fetchone()[0]
    if integrity != "ok" or foreign or journal != "delete" or (row_count, attempt_count) != (4, 4):
        raise ValueError("B4 comparison SQLite integrity/rows/journal failed")
    if not audit["standalone_database_modified"] or digest(B0) == digest(
        OUT / "comparison.sqlite3"
    ):
        raise ValueError("B4 comparison database is not an isolated modified copy")
    return {
        "status": "PASS_ENGINEERING_BOUNDARIES_SEMANTIC_GATE_OPEN",
        "case_count": 4,
        "model_requests": 3,
        "source_validated_model_candidates": 2,
        "source_only_candidates": 1,
        "failed_model_cases": 1,
        "quarantined_fragments": 4,
        "source_items": metrics["source_item_count"],
        "comparison_integrity": "ok",
        "production_promotion": 0,
        "unseen_generalization_established": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
