"""Run private B2 original-source diagnostics and B1 draft compatibility checks.

Example, from repository root (on a frozen read-only diagnostic database):
  python scripts/diagnose_stage_b2_candidate.py --database data/local-acceptance/\
p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3 \
--jobs tNhZ tMps tNDx tMjm \
--out data/local-acceptance/p16-stage-b2-2026-11-15/first-candidate

No model calls, scraping, production writes, accepted-artifact promotion, or
source/translation edits. Full source text and board values stay local-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from time import perf_counter
from typing import Any

from jobhunter.source_item_candidate_b2 import (
    B2SourceCandidate,
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore


def b1_design_from_b2(
    candidate: B2SourceCandidate, source: TranslationSourceVersion
) -> dict[str, Any]:
    """Non-authoritative B1-compatible *structural* projection.

    The B2 alternative ledger may retain more possible logic than can be
    proved as a B1 eligibility graph. Only clearly scoped seniority tracks
    are projected here; undecomposed OR clauses are intentionally withheld.
    """
    verify_b2_candidate(candidate, source)
    tracks = [
        group
        for group in candidate.alternatives
        if group.kind == "seniority_tracks" and len(group.source_anchor_ids) >= 2
    ]
    conditional_ids = set()
    for group in tracks:
        conditional_ids.update(group.source_anchor_ids)
    items = []
    source_ids: dict[str, str] = {}
    for unit in candidate.items:
        anchor = unit.anchor
        iid = "s_" + anchor.anchor_id[:40]
        source_ids[anchor.anchor_id] = iid
        scope = (
            "alternative_path"
            if anchor.anchor_id in conditional_ids
            else "standalone"
            if unit.category in {"candidate_qualification", "behavioral_expectation"}
            else "not_applicable"
        )
        items.append(
            {
                "item_id": iid,
                "source_ref": {
                    "kind": "original_description_span",
                    "anchor_id": anchor.anchor_id,
                    "field_path": anchor.field_path,
                    "field_sha256": anchor.field_sha256,
                    "text_sha256": anchor.text_sha256,
                    "char_start": anchor.char_start,
                    "char_end": anchor.char_end,
                },
                "meaning": {
                    "category": unit.category,
                    "employer_strength": unit.employer_strength,
                    "basis": unit.evidence_basis,
                    "qualifier_status": unit.qualifier,
                    "scope": scope,
                },
                "semantic_review": "candidate_unreviewed",
            }
        )
    board_ids = {}
    for board in candidate.board_values:
        iid = "b_" + hashlib.sha256(board.selector.encode()).hexdigest()[:32]
        board_ids[board.selector] = iid
        cat = {
            "skills": "candidate_qualification",
            "minimum_experience": "candidate_qualification",
            "education": "candidate_qualification",
            "employment_type": "work_arrangement",
            "salary": "compensation",
            "location": "work_arrangement",
            "job_category": "context",
        }.get(board.field_path, "context")
        items.append(
            {
                "item_id": iid,
                "source_ref": {
                    "kind": "structured_board_value",
                    "field_path": board.field_path,
                    "selector": board.selector,
                    "field_json_sha256": board.field_json_sha256,
                    "selected_value_json_sha256": board.value_json_sha256,
                },
                "meaning": {
                    "category": cat,
                    "employer_strength": "unresolved"
                    if cat == "candidate_qualification"
                    else "not_applicable",
                    "basis": "board_metadata_only",
                    "qualifier_status": "unresolved"
                    if cat == "candidate_qualification"
                    else "not_applicable",
                    "scope": "not_applicable",
                },
                "semantic_review": "candidate_unreviewed",
            }
        )
    graphs = []
    for index, group in enumerate(tracks):
        leaf_ids = [source_ids[aid] for aid in group.source_anchor_ids]
        node_ids = [f"track_{index}_{i}" for i in range(len(leaf_ids))]
        graphs.append(
            {
                "graph_id": f"source_track_choice_{index}",
                "root_id": f"track_root_{index}",
                "review_state": "candidate",
                "basis_item_ids": leaf_ids,
                "nodes": [
                    {"id": f"track_root_{index}", "operator": "any_of", "children": node_ids},
                    *[
                        {"id": nid, "operator": "item", "item_id": iid}
                        for nid, iid in zip(node_ids, leaf_ids, strict=True)
                    ],
                ],
            }
        )
    conflicts = []
    for signal in candidate.signals:
        if (
            signal.kind == "board_skill_tag_vs_preferred_prose"
            and signal.source_anchor_id in source_ids
            and signal.board_selector in board_ids
        ):
            conflicts.append(
                {
                    "item_id_a": source_ids[signal.source_anchor_id],
                    "item_id_b": board_ids[signal.board_selector],
                    "type": "board_vs_employer_strength",
                    "resolution": "unresolved",
                }
            )
    return {
        "contract_version": "jobhunter-stage-b1-source-evidence-bundle-draft-v1",
        "authority": "candidate_only_no_downstream_reuse",
        "source_version": {
            "source_job_id": source.source_job_id,
            "job_detail_version_id": source.job_detail_version_id,
            "semantic_sha256": source.semantic_sha256,
            "parser_version": source.fields.get("parser_version", "jobinja-detail-v2"),
        },
        "items": items,
        "alignments": [],
        "eligibility_graphs": graphs,
        "conflicts": conflicts,
        "review_events": [],
        "brief": {
            "state": "candidate_only",
            "analysis_outcome": "not_run",
            "selected_item_ids": [],
            "unresolved_item_ids": [],
            "downstream_authority": "none",
        },
    }


def diagnose(database: Path, jobs: tuple[str, ...], out: Path) -> dict[str, Any]:
    """Validate a private frozen snapshot, save full outputs only under ignored data."""
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter repository root")
    if not out.resolve().is_relative_to(root / "data/local-acceptance"):
        raise ValueError("Private source diagnostics must stay in ignored local data")
    if not 1 <= len(jobs) <= 8 or len(jobs) != len(set(jobs)):
        raise ValueError("Provide one to eight distinct source IDs")
    if not database.is_file() or out.exists():
        raise ValueError("Missing frozen input or refusing output overwrite")
    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-") as temp:
        copied = Path(temp) / "source.sqlite3"
        read_only = "file:" + str(database.resolve()) + "?mode=ro"
        with (
            sqlite3.connect(read_only, uri=True) as read,
            sqlite3.connect(copied) as write,
        ):
            read.backup(write)
            if write.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Frozen source SQLite integrity failed")
            if write.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Frozen source SQLite foreign key failed")
        store = TranslationStore(copied)
        private = {}
        safe = {}
        for job in jobs:
            started = perf_counter()
            source = store.latest_source_version(job)
            if source is None:
                raise ValueError(f"Missing source version for {job}")
            candidate = interpret_original_source_candidate(source)
            verify_b2_candidate(candidate, source)
            design = b1_design_from_b2(candidate, source)
            from validate_stage_b1_design import validate_bundle

            validate_bundle(design, source=source)
            private[job] = {
                "original_candidate": asdict(candidate),
                "b1_compatible_draft": design,
            }
            counts = Counter(item.category for item in candidate.items)
            alternatives = Counter(group.kind for group in candidate.alternatives)
            safe[job] = {
                "source_semantic_sha256": source.semantic_sha256,
                "source_version_id": source.job_detail_version_id,
                "item_count": len(candidate.items),
                "elapsed_ms": round((perf_counter() - started) * 1000, 2),
                "categories": dict(sorted(counts.items())),
                "required_candidate_count": sum(
                    i.employer_strength == "required" for i in candidate.items
                ),
                "preferred_candidate_count": sum(
                    i.employer_strength == "preferred" for i in candidate.items
                ),
                "unresolved_strength_count": sum(
                    i.employer_strength == "unresolved" for i in candidate.items
                ),
                "board_value_count": len(candidate.board_values),
                "board_page_copy_warning_count": sum(
                    x.kind == "possible_page_copy_in_board_skills" for x in candidate.signals
                ),
                "board_preference_disagreement_count": sum(
                    x.kind == "board_skill_tag_vs_preferred_prose" for x in candidate.signals
                ),
                "board_possible_arrangement_scope_loss_count": sum(
                    x.kind == "board_employment_mode_may_hide_prose_alternative"
                    for x in candidate.signals
                ),
                "board_possible_seniority_scope_loss_count": sum(
                    x.kind == "board_experience_range_may_hide_seniority_alternatives"
                    for x in candidate.signals
                ),
                "alternative_groups_candidate": dict(sorted(alternatives.items())),
                "work_capability_hint_count": len(candidate.work_capability_links),
                "b1_compatibility": "schema_reference_valid_candidate_only",
                "b1_nested_alternatives_not_yet_proven": any(
                    a.kind != "seniority_tracks" for a in candidate.alternatives
                ),
            }
    out.mkdir(parents=True)
    (out / "PRIVATE_B2_CANDIDATES.json").write_text(
        json.dumps(private, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    )
    report = {
        "contract": "jobhunter-b2-private-first-run-summary-v1",
        "job_count": len(jobs),
        "model_calls": 0,
        "new_source_acquisitions": 0,
        "persistent_accepted_artifacts": 0,
        "production_route_changed": False,
        "source_only_candidate": True,
        "b1_design_structural_verification_only": True,
        "semantics_independently_accepted": False,
        "b2_gate_closed": False,
        "cases": safe,
    }
    (out / "SAFE_METRICS.json").write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--jobs", required=True, nargs="+")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = diagnose(args.database, tuple(args.jobs), args.out)
    print("B2_PRIVATE_SOURCE_CANDIDATE_PASS", report["job_count"], "cases")
    for job, row in report["cases"].items():
        print(job, "items", row["item_count"], "source_refs", row["source_semantic_sha256"][:12])
    print("B2_ACCEPTANCE_GATE", "OPEN")


if __name__ == "__main__":
    main()
