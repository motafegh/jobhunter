#!/usr/bin/env python3
"""Replay B2v2 against the now-exposed eight-source B5 failure cohort.

This comparison is intentionally a DEVELOPMENT regression, never a fresh B5
holdout re-test or production promotion. The immutable B2v1 failure replayer is
run first. All real employer source and per-anchor diagnostics remain private.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.source_item_candidate_b2_v2 import (
    B2V2_ENGINE,
    build_candidate_eligibility_logic_v2,
    interpret_original_source_candidate_v2,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
PREVIOUS_B0 = (
    ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
)
B0_IDS = ("tNhZ", "tMps", "tNDx", "tMjm")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run() -> dict[str, Any]:
    frozen_verifier = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_source_gate.py"))["verify"]
    old_verdict = frozen_verifier()
    if old_verdict["status"] != "PASS_REPLAY_OF_B5_UPSTREAM_SEMANTIC_BLOCKER":
        raise ValueError("Historical B5 source failure changed")
    original_result = load(PRIVATE / "B5_B2_SOURCE_GATE_RESULT.json")
    selected = load(PRIVATE / "B5_SELECTION_FROZEN.json")
    reviewed = load(PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    source_manifest = load(PRIVATE / "B5_SOURCE_FROZEN_BEFORE_REVIEW.json")
    frozen_snapshot = PRIVATE / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    if source_manifest["snapshot_database_sha256"] != sha(frozen_snapshot):
        raise ValueError("Selected original source cohort changed")
    source_versions = {}
    store = TranslationStore(frozen_snapshot)
    for item in selected["selected_primary"]:
        job = item["source_job_id"]
        source = store.latest_source_version(job)
        expected = next(
            x["source_semantic_sha256"]
            for x in source_manifest["entries"]
            if x["source_job_id"] == job
        )
        if source is None or source.semantic_sha256 != expected:
            raise ValueError(f"Original source changed: {job}")
        source_versions[job] = source
    evaluator = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    new = evaluator(
        frozen=selected,
        review=reviewed,
        source_versions=source_versions,
        engine=interpret_original_source_candidate_v2,
    )
    if new["counts"]["frozen_source_first_anchor_count"] != 93:
        raise ValueError("Source-first anchor comparison denominator drifted")
    original_counts = original_result["counts"]
    revised_counts = new["counts"]
    if (
        revised_counts["candidate_role_match_anchor_count"]
        <= original_counts["candidate_role_match_anchor_count"]
        or revised_counts["explicit_duty_missed_anchor_count"]
        >= original_counts["explicit_duty_missed_anchor_count"]
        or revised_counts["optional_or_negative_required_overstatement_count"] != 0
        or revised_counts["multi_specialty_alternative_structure_missing_jobs"] != 0
    ):
        raise ValueError("B2v2 did not repair critical exposed source-gate failures")
    specialty = next(
        case for case in new["cases"] if case["frozen_review_alternative_anchor_count"]
    )
    s = source_versions[specialty["source_job_id"]]
    alternate_candidate = interpret_original_source_candidate_v2(s)
    alternative = [
        x
        for x in alternate_candidate.alternatives
        if x.kind == "one_or_more_separately_hired_specialties"
    ]
    alternative_logic = build_candidate_eligibility_logic_v2(s, alternate_candidate)
    if (
        len(alternative) != 1
        or alternative_logic.graphs
        or alternative[0].kind not in alternative_logic.unresolved_group_kinds
    ):
        raise ValueError("Ambiguous specialty paths were wrongly granted Boolean graph authority")
    # Ensure the historical B0 developer cases retain conditional trees.
    b0_store = TranslationStore(PREVIOUS_B0)
    graph_regressions = []
    for job in B0_IDS:
        source = b0_store.latest_source_version(job)
        if source is None:
            raise ValueError(f"Frozen exposed B0 source missing: {job}")
        old_candidate = interpret_original_source_candidate(source)
        updated_candidate = interpret_original_source_candidate_v2(source)
        old_logic = build_candidate_eligibility_logic(source, old_candidate)
        updated_logic = build_candidate_eligibility_logic_v2(source, updated_candidate)
        if {g.graph_id for g in old_logic.graphs} != {
            g.graph_id for g in updated_logic.graphs
        } or sum(i.category == "work_duty" for i in old_candidate.items) != sum(
            i.category == "work_duty" for i in updated_candidate.items
        ):
            raise ValueError(f"B0 regression in existing duty/eligibility scope: {job}")
        graph_regressions.append(
            {
                "source_job_id": job,
                "source_semantic_sha256": source.semantic_sha256,
                "baseline_duty_count": sum(i.category == "work_duty" for i in old_candidate.items),
                "revised_duty_count": sum(
                    i.category == "work_duty" for i in updated_candidate.items
                ),
                "baseline_graph_names": [g.graph_id for g in old_logic.graphs],
                "revised_graph_names": [g.graph_id for g in updated_logic.graphs],
            }
        )
    old_case_map = {c["source_job_id"]: c for c in original_result["cases"]}
    per_case = []
    for case in new["cases"]:
        old_case = old_case_map[case["source_job_id"]]
        per_case.append(
            {
                "source_job_id": case["source_job_id"],
                "source_semantic_sha256": case["source_semantic_sha256"],
                "old_item_count": old_case["source_b2_candidate_items"],
                "new_item_count": case["source_b2_candidate_items"],
                "old_role_match_count": old_case["candidate_role_match_anchor_count"],
                "new_role_match_count": case["candidate_role_match_anchor_count"],
                "old_role_mismatch_count": old_case["candidate_role_mismatch_anchor_count"],
                "new_role_mismatch_count": case["candidate_role_mismatch_anchor_count"],
                "old_not_contained_anchor_count": len(old_case["noncontained_anchor_ids"]),
                "new_not_contained_anchor_count": len(case["noncontained_anchor_ids"]),
                "missed_duty_count": case["missed_explicit_duty_anchor_count"],
                "false_required_count": case["optional_or_negative_required_overstatement_count"],
                "new_structured_alternative_count": case["b2_alternative_group_count"],
                "new_eligibility_graph_count": case["b2_nested_eligibility_graph_count"],
                "unresolved_issues": case["issues"],
            }
        )
    record = {
        "contract": "jobhunter-p16-b2v2-exposed-source-regression-replay-v1",
        "replayed_at_utc": datetime.now(UTC).isoformat(),
        "engine": B2V2_ENGINE,
        "source_cohort_status": "EIGHT_EXPOSED_DEVELOPMENT_CASES_NOT_UNSEEN",
        "outcome": "BOUNDED_SOURCE_ROLE_IMPROVEMENT_NOT_B5_ACCEPTANCE",
        "assistant_high_risk_anchor_review_not_full_ground_truth": True,
        "source_review_independent_blind_human": False,
        "fresh_unseen_evaluation": False,
        "unseen_B5_gate": "BLOCKED_AWAITING_NEW_COHORT_AND_PAIRED_MODEL_COMPARISON",
        "old_b2v1_gate_hash_sha256": sha(PRIVATE / "B5_B2_SOURCE_GATE_RESULT.json"),
        "frozen_original_source_snapshot_sha256": sha(frozen_snapshot),
        "sealed_source_review_sha256": sha(
            PRIVATE / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"
        ),
        "new_parser_source_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"),
        "original_parser_source_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2.py"),
        "old_counts": original_counts,
        "new_counts": revised_counts,
        "new_raw_source_or_model_requests": 0,
        "accepted_employer_facts_promoted": 0,
        "modified_accepted_P16_or_capability_or_market_state": False,
        "new_specialty_OR_graph_authorized": False,
        "new_specialty_option_scope_preserved_as_unresolved_candidate": True,
        "old_B0_regression_count": len(graph_regressions),
        "prior_B0_graph_regressions": graph_regressions,
        "per_case": per_case,
        "full_new_selected_anchor_comparison": new,
    }
    private = PRIVATE / "B5_B2V2_EXPOSED_COMPARISON.json"
    if private.exists():
        raise ValueError("B2v2 exposed comparison is sealed; do not overwrite")
    private.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-cases", action="store_true")
    args = parser.parse_args()
    result = run()
    output = {
        "outcome": result["outcome"],
        "old_counts": result["old_counts"],
        "new_counts": result["new_counts"],
        "prior_exposed_B0_regression_count": result["old_B0_regression_count"],
        "unseen_B5_gate": result["unseen_B5_gate"],
    }
    if args.print_cases:
        output["per_case"] = result["per_case"]
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
