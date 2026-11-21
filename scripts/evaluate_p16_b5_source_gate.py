"""B5 source-first gate: compare frozen original-source anchors to unchanged B2.

Read-only over eight selected held-out originals. Do not call translation/LLM,
accept source classifications, modify the production DB or claim a full truth
denominator from the assistant's selected risk anchors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import (
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
EXPECTED_ROLES = {
    "duty": "work_duty",
    "qualification": "candidate_qualification",
    "behavior": "behavioral_expectation",
    "arrangement": "work_arrangement",
}
OPTIONAL_MODALITIES = {
    "nice_to_have",
    "bonus_optional",
    "explicit_preferred",
    "explicit_special_advantage",
    "preferred_education",
    "preferred_tools",
    "preferred_programming",
    "preferred_certificates",
    "preferred_degree",
    "optional_relocation",
}
NEGATIVE_MODALITIES = {"explicit_not_required"}
MODELED_EXPECTATION_CLASSES = set(EXPECTED_ROLES)
ELIGIBILITY_SOURCE_CLASSES = {"alternative"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"B5 expected JSON object in {path}")
    return value


def match_source_anchor(anchor: dict[str, Any], candidate: Any) -> dict[str, Any]:
    """Check whether a reviewed exact source span is surfaced with matching B2 role."""
    a, b = anchor["original_description_start"], anchor["original_description_end"]
    if a < 0 or b <= a:
        raise ValueError("Invalid frozen source-first anchor coordinates")
    reviewed = anchor["original_quote"]
    if hashlib.sha256(reviewed.encode()).hexdigest() != anchor["quote_sha256"]:
        raise ValueError("Frozen review source quote SHA changed")
    matches = [
        item
        for item in candidate.items
        if item.anchor.char_start <= a and item.anchor.char_end >= b
    ]
    if len(matches) > 1:
        raise ValueError("B2 candidate source units overlap a reviewed exact anchor")
    item = matches[0] if matches else None
    expected = EXPECTED_ROLES.get(anchor["kind"])
    result = {
        "anchor_id": anchor["anchor_id"],
        "original_quote_sha256": anchor["quote_sha256"],
        "expected_review_kind": anchor["kind"],
        "expected_role": expected,
        "source_review_modality": anchor["modality_source_first"],
        "span_present_within_one_candidate": bool(matches),
        "candidate_role": item.category if item else None,
        "candidate_strength": item.employer_strength if item else None,
        "candidate_source_anchor_id": item.anchor.anchor_id if item else None,
        "candidate_semantic_role_match": (item.category == expected if item and expected else None),
        "optional_or_negative_strengthened_to_required": bool(
            item is not None
            and (anchor["modality_source_first"] in OPTIONAL_MODALITIES | NEGATIVE_MODALITIES)
            and item.employer_strength == "required"
        ),
        "verdict_state": (
            "covered_correctly_classified"
            if item and expected and item.category == expected
            else (
                "covered_category_mismatch"
                if item and expected
                else (
                    "covered_not_evaluated_for_category" if item else "not_contained_in_single_item"
                )
            )
        ),
    }
    return result


def evaluate_source_gate(
    *,
    frozen: dict[str, Any],
    review: dict[str, Any],
    source_versions: dict[str, Any],
    engine: Any,
) -> dict[str, Any]:
    """Evaluate predefined anchor scope once; never auto-repair or tune with held-out."""
    selected = [item["source_job_id"] for item in frozen["selected_primary"]]
    reviewed = [entry["source_job_id"] for entry in review["entries"]]
    if selected != reviewed:
        raise ValueError("Frozen B5 cohort order and source-first review inventory differ")
    if len(selected) < 6 or len(selected) > 8 or len(set(selected)) != len(selected):
        raise ValueError("B5 must use six to eight distinct preselected sources")
    entries = []
    for source_review in review["entries"]:
        job_id = source_review["source_job_id"]
        source = source_versions[job_id]
        if source.semantic_sha256 != source_review["source_semantic_sha256"]:
            raise ValueError(f"Source semantics changed before evaluation: {job_id}")
        candidate = engine(source)
        verify_b2_candidate(candidate, source)
        logic = build_candidate_eligibility_logic(source, candidate)
        anchor_scores = [
            match_source_anchor(anchor, candidate)
            for anchor in source_review["reviewed_original_anchors"]
        ]
        role_mismatches = [
            x["anchor_id"] for x in anchor_scores if x["candidate_semantic_role_match"] is False
        ]
        missing_anchoring = [
            x["anchor_id"] for x in anchor_scores if not x["span_present_within_one_candidate"]
        ]
        missing_duty = [
            x["anchor_id"]
            for x in anchor_scores
            if x["expected_review_kind"] == "duty"
            and x["candidate_semantic_role_match"] is not True
        ]
        optional_overstated = [
            x["anchor_id"]
            for x in anchor_scores
            if x["optional_or_negative_strengthened_to_required"]
        ]
        alternative_checks = [
            x for x in anchor_scores if x["expected_review_kind"] == "alternative"
        ]
        missing_grouped_alternatives = bool(
            alternative_checks and not (candidate.alternatives or logic.graphs)
        )
        counts = Counter(item.category for item in candidate.items)
        issues = []
        if missing_duty:
            issues.append("explicit_work_duties_not_classified")
        if optional_overstated:
            issues.append("optional_or_negated_claim_strengthened")
        if missing_grouped_alternatives:
            issues.append("multi_specialty_alternative_not_structured")
        if any(
            x["expected_review_kind"] == "qualification"
            and x["candidate_semantic_role_match"] is not True
            for x in anchor_scores
        ):
            issues.append("explicit_qualification_not_classified")
        if len(candidate.items) == 1 and len(source_review["reviewed_original_anchors"]) >= 5:
            issues.append("entire_description_as_one_candidate_item")
        if not any(i.category == "work_duty" for i in candidate.items) and any(
            x["expected_review_kind"] == "duty" for x in anchor_scores
        ):
            issues.append("no_duty_items_despite_explicit_work")
        entry = {
            "source_job_id": job_id,
            "source_semantic_sha256": source.semantic_sha256,
            "frozen_assistant_reference_anchor_count": len(anchor_scores),
            "source_b2_candidate_items": len(candidate.items),
            "b2_category_counts": dict(sorted(counts.items())),
            "b2_strength_counts": dict(
                sorted(Counter(item.employer_strength for item in candidate.items).items())
            ),
            "exact_anchor_containment_count": sum(
                x["span_present_within_one_candidate"] for x in anchor_scores
            ),
            "source_review_type_anchor_count": sum(
                x["expected_role"] is not None for x in anchor_scores
            ),
            "candidate_role_match_anchor_count": sum(
                x["candidate_semantic_role_match"] is True for x in anchor_scores
            ),
            "candidate_role_mismatch_anchor_count": len(role_mismatches),
            "missed_explicit_duty_anchor_count": len(missing_duty),
            "optional_or_negative_required_overstatement_count": len(optional_overstated),
            "b2_alternative_group_count": len(candidate.alternatives),
            "b2_nested_eligibility_graph_count": len(logic.graphs),
            "frozen_review_alternative_anchor_count": len(alternative_checks),
            "multi_specialty_alternative_structure_missing": missing_grouped_alternatives,
            "source_first_review_not_exhaustive": True,
            "issues": list(dict.fromkeys(issues)),
            "missed_explicit_duty_anchor_ids": missing_duty,
            "role_mismatch_anchor_ids": role_mismatches,
            "noncontained_anchor_ids": missing_anchoring,
            "optional_or_negative_overstatement_anchor_ids": optional_overstated,
            "anchor_diagnostics": anchor_scores,
            "candidate_authority": candidate.authority,
            "promotion": "not_allowed",
        }
        entries.append(entry)
    totals = {
        "frozen_source_first_anchor_count": sum(
            x["frozen_assistant_reference_anchor_count"] for x in entries
        ),
        "source_type_anchor_count": sum(x["source_review_type_anchor_count"] for x in entries),
        "candidate_role_match_anchor_count": sum(
            x["candidate_role_match_anchor_count"] for x in entries
        ),
        "candidate_role_mismatch_anchor_count": sum(
            x["candidate_role_mismatch_anchor_count"] for x in entries
        ),
        "explicit_duty_missed_anchor_count": sum(
            x["missed_explicit_duty_anchor_count"] for x in entries
        ),
        "optional_or_negative_required_overstatement_count": sum(
            x["optional_or_negative_required_overstatement_count"] for x in entries
        ),
        "multi_specialty_alternative_structure_missing_jobs": sum(
            x["multi_specialty_alternative_structure_missing"] for x in entries
        ),
        "job_count_with_critical_structural_or_category_gaps": sum(
            bool(x["issues"]) for x in entries
        ),
    }
    blocked = bool(
        totals["explicit_duty_missed_anchor_count"]
        or totals["multi_specialty_alternative_structure_missing_jobs"]
        or totals["optional_or_negative_required_overstatement_count"]
    )
    return {
        "contract": "jobhunter-p16-b5-frozen-source-gate-v1",
        "evaluation_time_utc": datetime.now(UTC).isoformat(),
        "stage": "source_first_original_statement_to_B2_diagnostic",
        "disposition": "BLOCKED_UPSTREAM_SOURCE_SEMANTICS" if blocked else "PASS_SOURCE_GATE_ONLY",
        "source_first_review_was_frozen_before_analysis": True,
        "source_review_authority": "assistant_source_first_not_independent_human",
        "statistical_generalization": "not_established",
        "exhaustive_source_statement_denominator": False,
        "new_b3_translation_requests": 0,
        "new_b4_analysis_requests": 0,
        "new_v30_baseline_requests": 0,
        "accepted_facts_promoted": 0,
        "production_database_written": False,
        "downstream_authority": "none",
        "next_gate_status": "B5_HALTED_BEFORE_BILINGUAL_AND_PAIRED_EVALUATION"
        if blocked
        else "SOURCE_GATE_READY_FOR_BILINGUAL_SHADOW",
        "counts": totals,
        "cases": entries,
    }


def run(root: Path = DEFAULT_ROOT) -> dict[str, Any]:
    frozen = read(root / "B5_SELECTION_FROZEN.json")
    review = read(root / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    source_freeze = read(root / "B5_SOURCE_FROZEN_BEFORE_REVIEW.json")
    if review["source_only_reviewed_before_any_B5_candidate_inference"] is not True:
        raise ValueError("B5 original-source reviewer freeze must predate model outputs")
    if review["frozen_source_manifest_sha256"] != digest(
        root / "B5_SOURCE_FROZEN_BEFORE_REVIEW.json"
    ):
        raise ValueError("B5 source freeze changed after source-only review")
    if source_freeze["selection_file_sha256"] != digest(root / "B5_SELECTION_FROZEN.json"):
        raise ValueError("B5 selected set changed after acquisition")
    snapshot = root / "B5_8_SOURCE_SNAPSHOT.sqlite3"
    if source_freeze["snapshot_database_sha256"] != digest(snapshot):
        raise ValueError("B5 isolated source snapshot changed")
    with sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True) as con:
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("B5 source snapshot SQLite integrity failed")
        if con.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("B5 source snapshot contains FK violations")
    store = TranslationStore(snapshot)
    versions: dict[str, Any] = {}
    for source in source_freeze["entries"]:
        job_id = source["source_job_id"]
        version = store.latest_source_version(job_id)
        if version is None or version.semantic_sha256 != source["source_semantic_sha256"]:
            raise ValueError(f"B5 frozen source version missing or changed: {job_id}")
        versions[job_id] = version
    result = evaluate_source_gate(
        frozen=frozen,
        review=review,
        source_versions=versions,
        engine=interpret_original_source_candidate,
    )
    result["frozen_selection_sha256"] = digest(root / "B5_SELECTION_FROZEN.json")
    result["frozen_source_review_sha256"] = digest(
        root / "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"
    )
    result["frozen_snapshot_sha256"] = digest(snapshot)
    result["b2_code_sha256"] = digest(ROOT / "src/jobhunter/source_item_candidate_b2.py")
    output = root / "B5_B2_SOURCE_GATE_RESULT.json"
    if output.exists():
        raise ValueError("Do not overwrite a sealed B5 source-gate evaluation")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    result = run(args.private_root)
    print(
        json.dumps(
            {
                "disposition": result["disposition"],
                "counts": result["counts"],
                "per_case": {
                    case["source_job_id"]: {
                        "source_items": case["source_b2_candidate_items"],
                        "missed_duties": case["missed_explicit_duty_anchor_count"],
                        "role_mismatches": case["candidate_role_mismatch_anchor_count"],
                        "alternatives_missing": case[
                            "multi_specialty_alternative_structure_missing"
                        ],
                        "issues": case["issues"],
                    }
                    for case in result["cases"]
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
