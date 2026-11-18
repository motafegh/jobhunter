"""Reconcile a bounded, candidate-only B2 source inventory milestone.

This verifies exact reproducibility and frozen exposed-case regression boundaries.
It does not certify employer semantics, generalization, or production authority.
Raw original-source and candidate text stays in ignored local data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import tempfile
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import (
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from diagnose_stage_b2_candidate import b1_design_from_b2  # noqa: E402
from validate_stage_b1_design import validate_bundle  # noqa: E402

EXPECTED_DATABASE_SHA256 = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
JOBS = ("tNhZ", "tMps", "tNDx", "tMjm")
EXPECTED_DUTIES = {"tNhZ": 6, "tMps": 11, "tNDx": 5, "tMjm": 0}
EXPECTED_CONFLICTS = {
    "tNhZ": {"board_vs_employer_strength", "board_vs_employer_arrangement"},
    "tMps": {"board_vs_employer_experience"},
    "tNDx": {"board_vs_employer_compensation"},
    "tMjm": set(),
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False, sort_keys=True))


def _read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path.name}")
    return value


def _contains(candidate: Any, text: str, *, category: str | None = None) -> bool:
    return any(
        text.casefold() in item.anchor.exact_text.casefold()
        and (category is None or item.category == category)
        for item in candidate.items
    )


def reconcile(database: Path, private_dir: Path) -> dict[str, Any]:
    if not (ROOT / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter repository root")
    if not database.resolve().is_relative_to(ROOT / "data/local-acceptance"):
        raise ValueError("Frozen source input must remain under ignored local data")
    if not private_dir.resolve().is_relative_to(ROOT / "data/local-acceptance"):
        raise ValueError("Full candidate output must remain under ignored local data")
    private_path = private_dir / "PRIVATE_B2_CANDIDATES.json"
    metrics_path = private_dir / "SAFE_METRICS.json"
    if not database.is_file() or not private_path.is_file() or not metrics_path.is_file():
        raise ValueError("Missing frozen database or diagnostic outputs")

    database_sha = _sha(database)
    if database_sha != EXPECTED_DATABASE_SHA256:
        raise ValueError("B2 candidate milestone must use the exact frozen B0 database")
    private = _read(private_path)
    metrics = _read(metrics_path)
    if (
        metrics.get("contract") != "jobhunter-b2-private-first-run-summary-v1"
        or metrics.get("source_database_sha256") != database_sha
        or metrics.get("job_count") != len(JOBS)
        or metrics.get("model_calls") != 0
        or metrics.get("new_source_acquisitions") != 0
        or metrics.get("persistent_accepted_artifacts") != 0
        or metrics.get("production_route_changed") is not False
        or metrics.get("source_only_candidate") is not True
        or metrics.get("b1_design_structural_verification_only") is not True
        or metrics.get("semantics_independently_accepted") is not False
        or metrics.get("b2_gate_closed") is not False
        or set(metrics.get("cases", {})) != set(JOBS)
        or set(private) != set(JOBS)
    ):
        raise ValueError("Source, scope, or non-promotion evidence mismatch")

    per_case: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-milestone-") as temp:
        copied = Path(temp) / "source.sqlite3"
        with (
            sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as source_db,
            sqlite3.connect(copied) as copy_db,
        ):
            source_db.backup(copy_db)
            if copy_db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Frozen B0 SQLite integrity check failed")
            if copy_db.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Frozen B0 SQLite foreign-key check failed")
        store = TranslationStore(copied)

        for job in JOBS:
            source = store.latest_source_version(job)
            if source is None:
                raise ValueError(f"Missing frozen source for {job}")
            candidate = interpret_original_source_candidate(source)
            verify_b2_candidate(candidate, source)
            logic = build_candidate_eligibility_logic(source, candidate)
            draft = b1_design_from_b2(candidate, source)
            validate_bundle(draft, source=source)

            saved = private[job]
            if _canonical(asdict(candidate)) != saved.get(
                "original_candidate"
            ) or draft != saved.get("b1_compatible_draft"):
                raise ValueError(f"Private candidate output is not reproducible for {job}")

            duty_count = sum(item.category == "work_duty" for item in candidate.items)
            if duty_count != EXPECTED_DUTIES[job]:
                raise ValueError(f"Unexpected duty candidate count for {job}")
            conflict_types = {item["type"] for item in draft["conflicts"]}
            if conflict_types != EXPECTED_CONFLICTS[job]:
                raise ValueError(f"Board conflict projection mismatch for {job}")
            if (
                draft["authority"] != "candidate_only_no_downstream_reuse"
                or draft["review_events"] != []
                or draft["brief"]["state"] != "candidate_only"
                or draft["brief"]["analysis_outcome"] != "not_run"
                or draft["brief"]["selected_item_ids"] != []
                or draft["brief"]["downstream_authority"] != "none"
                or any(item["semantic_review"] != "candidate_unreviewed" for item in draft["items"])
            ):
                raise ValueError(f"Candidate authority fence changed for {job}")

            if job == "tNhZ":
                if not _contains(candidate, "LLM", category="candidate_qualification"):
                    raise ValueError("tNhZ LLM familiarity candidate is missing")
                if not any(
                    item.employer_strength == "preferred" and "LLM" in item.anchor.exact_text
                    for item in candidate.items
                ):
                    raise ValueError("tNhZ explicit optional LLM familiarity was not preserved")
                if not any(item.capability == "LLM" for item in candidate.work_capability_links):
                    raise ValueError("tNhZ duty-implied LLM capability hint is missing")
                if not any(
                    item.kind == "board_employment_mode_may_hide_prose_alternative"
                    for item in candidate.signals
                ):
                    raise ValueError("tNhZ employment-mode scope signal is missing")
            elif job == "tMps":
                if not any(
                    item.employer_strength == "required"
                    and all(term in item.anchor.exact_text for term in ("Vector", "Reranking"))
                    for item in candidate.items
                ):
                    raise ValueError("tMps vector-search requirement candidate is missing")
                if (
                    len(logic.graphs) != 1
                    or logic.graphs[0].graph_id != "candidate_middle_or_senior"
                ):
                    raise ValueError("tMps Middle/Senior candidate graph is missing")
                projected_leaves = sum(
                    node["operator"] == "item" for node in draft["eligibility_graphs"][0]["nodes"]
                )
                if projected_leaves != 9:
                    raise ValueError("tMps nested candidate leaf count changed")
                if not any(
                    item.kind == "one_of_technical_domains" for item in candidate.alternatives
                ):
                    raise ValueError("tMps one-of domain candidate is missing")
            elif job == "tNDx":
                if not any(
                    item.employer_strength == "preferred" and "روحیه" in item.anchor.exact_text
                    for item in candidate.items
                ):
                    raise ValueError("tNDx explicit teamwork preference was not preserved")
                for marker in ("Kaspersky", "دولتی"):
                    if not any(
                        marker in item.anchor.exact_text and item.employer_strength == "unresolved"
                        for item in candidate.items
                    ):
                        raise ValueError(f"tNDx unresolved strength for {marker} changed")
                if (
                    len(logic.graphs) != 1
                    or logic.graphs[0].graph_id != "candidate_certificate_or_knowledge"
                ):
                    raise ValueError("tNDx certificate/equivalent candidate graph is missing")
                if not any(
                    item.kind == "board_prose_compensation_values_materially_differ"
                    for item in candidate.signals
                ):
                    raise ValueError("tNDx salary discrepancy signal is missing")
            elif job == "tMjm":
                if duty_count != 0:
                    raise ValueError("tMjm applicant capabilities were converted to work duties")
                if not _contains(candidate, "OWASP", category="candidate_qualification"):
                    raise ValueError("tMjm explicit pentesting qualification is missing")
                if not _contains(candidate, "دورکاری", category="work_arrangement"):
                    raise ValueError("tMjm remote arrangement is missing")
                if not _contains(candidate, "وظیفه شناس", category="behavioral_expectation"):
                    raise ValueError("tMjm behavioral expectation is missing")

            safe_case = metrics["cases"][job]
            expected_metrics = {
                "source_semantic_sha256": source.semantic_sha256,
                "item_count": len(candidate.items),
                "board_value_count": len(candidate.board_values),
                "work_capability_hint_count": len(candidate.work_capability_links),
                "b1_candidate_eligibility_graph_count": len(draft["eligibility_graphs"]),
                "b1_candidate_eligibility_leaf_count": sum(
                    node["operator"] == "item"
                    for graph in draft["eligibility_graphs"]
                    for node in graph["nodes"]
                ),
                "b1_conflict_count": len(draft["conflicts"]),
                "b1_conflict_types": sorted(conflict_types),
            }
            if any(safe_case.get(key) != value for key, value in expected_metrics.items()):
                raise ValueError(f"Safe aggregate does not match recomputed candidate for {job}")
            per_case[job] = {
                "source_semantic_sha256": source.semantic_sha256,
                "source_item_count": len(candidate.items),
                "board_value_count": len(candidate.board_values),
                "work_duty_candidate_count": duty_count,
                "work_capability_hint_count": len(candidate.work_capability_links),
                "candidate_alternative_group_count": len(candidate.alternatives),
                "candidate_eligibility_graph_count": len(draft["eligibility_graphs"]),
                "candidate_eligibility_leaf_count": expected_metrics[
                    "b1_candidate_eligibility_leaf_count"
                ],
                "board_conflict_types": sorted(conflict_types),
                "semantic_review": "candidate_unreviewed",
            }

    aggregate = {
        "source_item_count": sum(x["source_item_count"] for x in per_case.values()),
        "board_value_count": sum(x["board_value_count"] for x in per_case.values()),
        "work_duty_candidate_count": sum(x["work_duty_candidate_count"] for x in per_case.values()),
        "work_capability_hint_count": sum(
            x["work_capability_hint_count"] for x in per_case.values()
        ),
        "candidate_alternative_group_count": sum(
            x["candidate_alternative_group_count"] for x in per_case.values()
        ),
        "candidate_eligibility_graph_count": sum(
            x["candidate_eligibility_graph_count"] for x in per_case.values()
        ),
        "candidate_eligibility_leaf_count": sum(
            x["candidate_eligibility_leaf_count"] for x in per_case.values()
        ),
        "board_conflict_count": sum(len(x["board_conflict_types"]) for x in per_case.values()),
    }
    expected_aggregate = {
        "source_item_count": 78,
        "board_value_count": 53,
        "work_duty_candidate_count": 22,
        "work_capability_hint_count": 10,
        "candidate_alternative_group_count": 3,
        "candidate_eligibility_graph_count": 2,
        "candidate_eligibility_leaf_count": 11,
        "board_conflict_count": 4,
    }
    if aggregate != expected_aggregate:
        raise ValueError(f"Aggregate B2 candidate evidence changed: {aggregate}")

    conflict_counts = Counter(
        kind for row in per_case.values() for kind in row["board_conflict_types"]
    )
    return {
        "contract": "jobhunter-p16-b2-bounded-candidate-milestone-v1",
        "source_database_sha256": database_sha,
        "private_candidate_sha256": _sha(private_path),
        "safe_diagnostic_metrics_sha256": _sha(metrics_path),
        "source_item_candidate_code_sha256": _sha(
            ROOT / "src/jobhunter/source_item_candidate_b2.py"
        ),
        "eligibility_candidate_code_sha256": _sha(
            ROOT / "src/jobhunter/source_eligibility_candidate_b2.py"
        ),
        "b1_draft_projection_code_sha256": _sha(ROOT / "scripts/diagnose_stage_b2_candidate.py"),
        "schema_sha256": _sha(
            ROOT / "docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json"
        ),
        "source_cohort": "four frozen, previously exposed A1 development ads; not a holdout",
        "candidate_milestone": "PASS_BOUNDED_EXPOSED_COHORT",
        "b2_full_semantic_generalization": "NOT_ESTABLISHED",
        "candidate_semantic_review": "candidate_unreviewed",
        "model_generated_source_reference_route": "RESEARCH_ONLY_NO_PROMOTION",
        "independent_accuracy_claim": False,
        "b1_structural_and_source_reference_validation": "PASS",
        "production_route_changed": False,
        "accepted_employer_facts_promoted": 0,
        "downstream_authority": "none",
        "aggregate": aggregate,
        "board_conflict_type_counts": dict(sorted(conflict_counts.items())),
        "per_case": per_case,
        "limitations": [
            (
                "The four original ads are previously exposed development cases, "
                "not independent holdout evidence."
            ),
            (
                "Exact source spans and B1 references establish provenance and structure, "
                "not semantic correctness."
            ),
            (
                "Candidate category and strength labels remain unreviewed and have no "
                "downstream authority."
            ),
            (
                "Unsupported eligibility syntax remains unresolved; the two admitted "
                "graphs are candidate-only."
            ),
            (
                "The model-generated source-reference route remains research-only because "
                "material semantic errors persisted."
            ),
            (
                "B3 item translation, B4 usefulness, B5 unseen generalization, and B6 "
                "production promotion remain separate gates."
            ),
        ],
        "next_stage": "B3_SOURCE_BOUND_ITEM_TRANSLATION_CANDIDATE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--private-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    safe_root = ROOT / "docs/working-memory/2026-11-17_p16_b2"
    if not out.is_relative_to(safe_root) or out.exists():
        raise ValueError("Safe milestone output must be new and remain in the dated review folder")
    report = reconcile(args.database, args.private_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "candidate_milestone": report["candidate_milestone"],
                "aggregate": report["aggregate"],
                "b2_full_semantic_generalization": report["b2_full_semantic_generalization"],
                "downstream_authority": report["downstream_authority"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
