#!/usr/bin/env python3
"""Verify second B5 source-first gate and optional B2v3 EXPOSED regression seal.

Read-only; no Jobinja/LM Studio HTTP, no acceptance writes. The first B5
cohort and old B2v2 are immutable and replayed separately.

--seal: once, capture *post-failure exposed regression* comparison under
ignored private storage; this is never a valid fresh-B5 acceptance verdict.
Default: verify sealed evidence, source hashes and production identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import sqlite3
from pathlib import Path
from typing import Any

from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.jobinja_details import parse_jobinja_detail
from jobhunter.source_bound_translation_b3 import select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.source_item_candidate_b2_v3 import (
    B2V3_ENGINE,
    build_candidate_eligibility_logic_v3,
    interpret_original_source_candidate_v3,
)
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
NEW = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/second-source-cohort-v1"
OLD = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen"
SEALED = NEW / "B5_SECOND_B2V3_EXPOSED_REPLAY.json"
FIRST = (
    "B5_SELECTION_FROZEN.json",
    "B5_SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
    "B5_8_SOURCE_SNAPSHOT.sqlite3",
)
SECOND = (
    "FROZEN_METADATA_SELECTION.json",
    "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json",
    "isolated-second-cohort.sqlite3",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Frozen expected object: {path.name}")
    return value


def sources(dir_: Path, filenames: tuple[str, str, str]):
    selection = load(dir_ / filenames[0])
    reviewed = load(dir_ / filenames[1])
    selected = selection.get("selected_primary", selection.get("primary"))
    if not isinstance(selected, list):
        raise ValueError("Missing source-only metadata selection")
    if [x["source_job_id"] for x in selected] != [x["source_job_id"] for x in reviewed["entries"]]:
        raise ValueError("Original source-review order does not match selected metadata")
    store = TranslationStore(dir_ / filenames[2])
    versions = {}
    for item in selected:
        job = item["source_job_id"]
        source = store.latest_source_version(job)
        assert source is not None
        entry = next(x for x in reviewed["entries"] if x["source_job_id"] == job)
        if source.semantic_sha256 != entry["source_semantic_sha256"]:
            raise ValueError("Source review used different semantic SHA")
        for anchor in entry["reviewed_original_anchors"]:
            a, b = anchor["original_description_start"], anchor["original_description_end"]
            if (
                source.fields["description"][a:b] != anchor["original_quote"]
                or hashlib.sha256(anchor["original_quote"].encode()).hexdigest()
                != anchor["quote_sha256"]
            ):
                raise ValueError("Original assistant source quote no longer exact")
        versions[job] = source
    return selected, reviewed, versions


def replay() -> dict[str, Any]:
    # Required frozen predecessor remains independently verifiable.
    historical = runpy.run_path(str(ROOT / "scripts/verify_p16_b5_source_gate.py"))["verify"]()
    if historical["status"] != "PASS_REPLAY_OF_B5_UPSTREAM_SEMANTIC_BLOCKER":
        raise ValueError("B5 first cohort original failure integrity changed")
    b2v2 = runpy.run_path(str(ROOT / "scripts/verify_p16_b2v2_exposed_regressions.py"))["verify"]()
    if b2v2["status"] != "PASS_EXPOSED_B2V2_REGRESSION_REPLAY_NOT_B5_ACCEPTANCE":
        raise ValueError("B5v2 previous selected development comparison changed")
    selection = load(NEW / "FROZEN_METADATA_SELECTION.json")
    manifest = load(NEW / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json")
    fetch = load(NEW / "PRIVATE_FETCH_RECEIPT.json")
    review = load(NEW / "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json")
    repair = load(NEW / "REVIEW_FREEZE_FORMAT_REPAIR_RECEIPT.json")
    first = load(OLD / "B5_SELECTION_FROZEN.json")
    second_v2 = load(NEW / "B5_SECOND_SOURCE_B2V2_GATE_RESULT.json")
    snapshot = NEW / SECOND[2]
    if (
        selection["source_contents_seen_before_selection"] is not False
        or selection["source_assessment_or_model_output_seen_before_selection"] is not False
        or manifest["frozen_pre_detail_selection_sha256"] != sha(NEW / SECOND[0])
        or manifest["frozen_fetch_receipt_sha256"] != sha(NEW / "PRIVATE_FETCH_RECEIPT.json")
        or manifest["frozen_isolated_source_database_sha256"] != sha(snapshot)
        or review["frozen_source_manifest_sha256"]
        != sha(NEW / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json")
        or review["frozen_source_snapshot_sha256"] != sha(snapshot)
        or review["frozen_selection_sha256"] != sha(NEW / SECOND[0])
        or review["source_only_reviewed_before_any_B5_candidate_inference"] is not True
        or review["model_results_inspected_before_review"] is not False
        or repair["original_source_first_meaning_or_quote_changed"] is not False
        or repair["B2v2_candidate_output_seen_before_repair"] is not False
        or repair["new_sha256"] != sha(NEW / SECOND[1])
        or repair["old_sha256"]
        != hashlib.sha256((NEW / SECOND[1]).read_bytes() + b"\\n").hexdigest()
        or manifest["model_requests"] != 0
        or second_v2["frozen_selection_sha256"] != sha(NEW / SECOND[0])
        or second_v2["frozen_source_first_review_sha256"] != sha(NEW / SECOND[1])
        or second_v2["frozen_source_snapshot_sha256"] != sha(snapshot)
        or second_v2["frozen_b2v2_parser_sha256"]
        != sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py")
        or second_v2["second_cohort_now_exposed_after_comparison"] is not True
        or second_v2["B5_paired_translation_or_v30_analysis_requested"] is not False
    ):
        raise ValueError("Second cohort source-first freeze order/integrity breached")
    if (
        selection["production_database_sha256"] != sha(ROOT / "data/jobhunter.sqlite3")
        or selection["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json")
        or fetch["production_database_unchanged"] is not True
        or fetch["public_corpus_unchanged"] is not True
        or len(fetch["successful_source_list"]) != 8
        or len(fetch["attempts"]) != 8
        or manifest["original_html_sha_verified"] != 8
        or review["anchor_count"] != 91
        or review["job_count"] != 8
    ):
        raise ValueError("B5 cohort/production DB/corpus unsafe")
    original_selected = {
        x["source_job_id"] for role in ("selected_primary", "reserve_order") for x in first[role]
    }
    new_selected = {x["source_job_id"] for x in selection["primary"]}
    new_companies = {x["metadata"]["company_slug"] for x in selection["primary"]}
    old_companies = {
        x["metadata"]["company_slug"]
        for role in ("selected_primary", "reserve_order")
        for x in first[role]
    }
    if (
        new_selected & original_selected
        or new_companies & old_companies
        or len(new_selected) != 8
        or len(new_companies) != 8
    ):
        raise ValueError("B5 second cohort is not distinct from previous exposure")
    with sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True) as db:
        if (
            db.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
            or db.execute("PRAGMA foreign_key_check").fetchall()
            or db.execute("SELECT COUNT(*) FROM job_detail_versions").fetchone()[0] != 8
            or db.execute("SELECT COUNT(*) FROM job_analysis_artifacts").fetchone()[0] != 0
        ):
            raise ValueError("Second B5 source-only database corrupted or analysis leaked")
    for entry in manifest["entries"]:
        raw = Path(entry["private_raw_html_path"])
        meta = Path(entry["private_raw_metadata_path"])
        if (
            not raw.resolve().is_relative_to(NEW.resolve())
            or not meta.resolve().is_relative_to(NEW.resolve())
            or sha(raw) != entry["raw_html_sha256"]
            or sha(meta) != entry["raw_metadata_sha256"]
            or _semantic_sha256(parse_jobinja_detail(raw.read_text(encoding="utf-8")).to_dict())
            != entry["original_semantic_sha256"]
        ):
            raise ValueError("Private original raw HTML / parsed semantics did not verify")

    evaluate = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    second_ids, second_review, second_versions = sources(NEW, SECOND)
    old_ids, old_review, old_versions = sources(OLD, FIRST)

    def score(ids, evidence, versions, engine):
        value = evaluate(
            frozen={"selected_primary": ids},
            review=evidence,
            source_versions=versions,
            engine=engine,
        )
        value.pop("evaluation_time_utc", None)
        return value

    baseline = score(
        second_ids, second_review, second_versions, interpret_original_source_candidate_v2
    )
    # Old frozen B2v2 result has additional evidence SHA fields.
    original_view = dict(second_v2)
    for k in (
        "evaluation_time_utc",
        "frozen_selection_sha256",
        "frozen_original_manifest_sha256",
        "frozen_source_first_review_sha256",
        "frozen_source_snapshot_sha256",
        "frozen_b2v2_parser_sha256",
        "candidate_role_interpretation",
        "second_cohort_now_exposed_after_comparison",
        "B5_paired_translation_or_v30_analysis_requested",
        "accepted_employer_facts_promoted",
        "B6_promotion",
    ):
        original_view.pop(k, None)
    if baseline != original_view:
        raise ValueError("Initial B2v2 source-failure verdict changed")
    revised_new = score(
        second_ids, second_review, second_versions, interpret_original_source_candidate_v3
    )
    revised_old = score(old_ids, old_review, old_versions, interpret_original_source_candidate_v3)
    if (
        revised_new["counts"]["candidate_role_match_anchor_count"] < 79
        or revised_new["counts"]["explicit_duty_missed_anchor_count"]
        or revised_new["counts"]["optional_or_negative_required_overstatement_count"]
        or revised_new["counts"]["multi_specialty_alternative_structure_missing_jobs"]
        or revised_old["counts"]["candidate_role_match_anchor_count"] < 82
        or revised_old["counts"]["explicit_duty_missed_anchor_count"]
        or revised_old["counts"]["optional_or_negative_required_overstatement_count"]
    ):
        raise ValueError("B2v3 did not repair exposed duties while preserving old data")
    # Original four B0 contract conditions are a distinct regression boundary.
    b0_store = TranslationStore(B0 / "exposed_original_snapshot.sqlite3")
    preserved = []
    for job in ("tNhZ", "tMps", "tNDx", "tMjm"):
        source = b0_store.latest_source_version(job)
        if source is None:
            raise ValueError("Missing historical B0 original source")
        old_candidate = interpret_original_source_candidate_v2(source)
        new_candidate = interpret_original_source_candidate_v3(source)
        old_logic = build_candidate_eligibility_logic(source, old_candidate)
        new_logic = build_candidate_eligibility_logic_v3(source, new_candidate)
        if {x.graph_id for x in old_logic.graphs} != {x.graph_id for x in new_logic.graphs} or sum(
            i.category == "work_duty" for i in old_candidate.items
        ) != sum(i.category == "work_duty" for i in new_candidate.items):
            raise ValueError("B0 old graph or duties damaged in experimental B2v3")
        preserved.append(job)
    b1 = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"]
    validate = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))["validate_bundle"]
    all_translate = []
    planned = {"source_items": 0, "translation_items": 0, "native_items": 0, "excluded_items": 0}
    for job, source in second_versions.items():
        candidate = interpret_original_source_candidate_v3(source)
        bundle = b1(candidate, source)
        validate(bundle, source=source)
        selection = select_b3_items(job, candidate.items)
        plan_items = prepare_source_batch_items(source, selection.translate_items)
        all_translate.extend(plan_items)
        planned["source_items"] += len(candidate.items)
        planned["translation_items"] += len(plan_items)
        planned["native_items"] += len(selection.native_identity_items)
        planned["excluded_items"] += len(selection.excluded_items)
    batches = plan_source_batches(all_translate, max_batch_items=3)
    if (
        len(preserved) != 4
        or planned["source_items"]
        != sum(planned[k] for k in ("translation_items", "native_items", "excluded_items"))
        or batches.deferred_oversized
    ):
        raise ValueError("B3 plan coverage or previous conditional graphs failed")
    return {
        "contract": (
            "jobhunter-p16-b5-second-original-source-failure-and-b2v3-exposed-regression-v1"
        ),
        "versioned_candidate": B2V3_ENGINE,
        "first_cohort_status": "already_exposed_original",
        "second_cohort_status": "exposed_after_B2v2_first_comparison",
        "new_unseen_B5_result": "SOURCE_SEMANTIC_GATE_BLOCKED_FOR_UNMODIFIED_B2v2",
        "new_B5_paired_model_or_translation_requests": 0,
        "B2v3_replay_is_fresh_unseen": False,
        "B6_promotion": False,
        "accepted_employer_facts_promoted": 0,
        "old_original_source_first_assertions": old_review["anchor_count"],
        "second_original_source_first_assertions": second_review["anchor_count"],
        "older_B2v2_counts": baseline["counts"],
        "revised_v3_second_counts": revised_new["counts"],
        "revised_v3_first_counts": revised_old["counts"],
        "older_B2v2_frozen_result_sha256": sha(NEW / "B5_SECOND_SOURCE_B2V2_GATE_RESULT.json"),
        "second_frozen_selection_sha256": sha(NEW / SECOND[0]),
        "second_frozen_original_review_sha256": sha(NEW / SECOND[1]),
        "second_original_source_manifest_sha256": sha(
            NEW / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json"
        ),
        "second_source_snapshot_sha256": sha(NEW / SECOND[2]),
        "new_B2v3_source_code_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2_v3.py"),
        "first_cohort_revised_score": revised_old,
        "second_cohort_revised_score": revised_new,
        "previous_B0_graphs_and_duties_preserved": len(preserved),
        "second_cohort_B1_schema_passed": len(second_versions),
        "second_cohort_translation_preflight": {
            **planned,
            "planned_physical_batches_max_three": len(batches.batches),
            "actually_executed_translation_model_calls": 0,
            "translation_attempt_and_wall_budget": (
                "separate_preselected_80_attempt_7200s_NOT_ACTIVATED"
            ),
        },
        "unresolved_role_assertions_are_not_reported_as_correct": True,
        "source_heading_spanning_reviews_are_not_automatically_semantic_success": True,
        "full_B5_independent_evaluation": False,
        "production_state_unchanged": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    data = replay()
    if args.seal:
        if SEALED.exists():
            raise ValueError("B5 second cohort exposed replay is sealed, no overwrite")
        SEALED.write_text(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
        SEALED.chmod(0o600)
        print("FROZEN_EXPOSED_REPLAY_SHA256", sha(SEALED))
    elif data != load(SEALED):
        raise ValueError("Sealed B2v3 exposed replay has drifted since capture")
    print(
        json.dumps(
            {
                "status": "PASS_REPLAY_SECOND_B5_SOURCE_BLOCKER_AND_B2V3_EXPOSED_REPAIR",
                "second_case_count": 8,
                "second_source_first_assertions": data["second_original_source_first_assertions"],
                "initial_v2_role_matches": data["older_B2v2_counts"][
                    "candidate_role_match_anchor_count"
                ],
                "exposed_v3_role_matches": data["revised_v3_second_counts"][
                    "candidate_role_match_anchor_count"
                ],
                "exposed_v3_missing_explicit_duties": data["revised_v3_second_counts"][
                    "explicit_duty_missed_anchor_count"
                ],
                "previous_four_B0_graphs_preserved": data[
                    "previous_B0_graphs_and_duties_preserved"
                ],
                "B1_contract_passed": data["second_cohort_B1_schema_passed"],
                "new_model_requests": 0,
                "unseen_B5_acceptance": False,
                "production_state_unchanged": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
