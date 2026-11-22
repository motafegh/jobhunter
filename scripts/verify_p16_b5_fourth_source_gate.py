"""Read-only verification of the failed FOURTH prospective B5 DOM source gate.

Replays source-first comparisons without translation, provider calls, accepted
writes or post-failure tuning. The original source-only review and alternative
supplement must both predate the initial frozen result. Private original HTML
is required; CI skips its optional integration fixture on clean clones.
"""

from __future__ import annotations

import hashlib
import json
import runpy
import sqlite3
from pathlib import Path

from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.jobinja_details import parse_jobinja_detail
from jobhunter.source_item_candidate_b2_v4_dom import interpret_original_source_candidate_v4
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/fourth-source-cohort-v1"
FROZEN = PRIVATE / "FROZEN_METADATA_SELECTION.json"
FETCH = PRIVATE / "PRIVATE_FETCH_RECEIPT.json"
ORIGINAL = PRIVATE / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json"
REVIEW = PRIVATE / "SOURCE_FIRST_ASSISTANT_REVIEW_SEALED.json"
OPTIONS = PRIVATE / "SOURCE_FIRST_EXPLICIT_OR_SUPPLEMENT_SEALED.json"
RESULT = PRIVATE / "B5_FOURTH_FROZEN_PROSPECTIVE_SOURCE_GATE_RESULT.json"
DB = PRIVATE / "isolated-fourth-cohort.sqlite3"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid immutable B5 evidence: {path}")
    return data


def verify() -> dict:
    frozen = load(FROZEN)
    fetch = load(FETCH)
    original = load(ORIGINAL)
    review = load(REVIEW)
    options = load(OPTIONS)
    result = load(RESULT)
    if (
        frozen["candidate_version"] != "B2v4_DOM_frozen_original_source_parser"
        or frozen["candidate_B2v4_source_sha256"]
        != sha(ROOT / "src/jobhunter/source_item_candidate_b2_v4_dom.py")
        or frozen["fourth_pre_source_candidate_freeze_commit"] != "f2e396a"
        or frozen["production_database_sha256"] != sha(ROOT / "data/jobhunter.sqlite3")
        or frozen["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json")
        or frozen["pre_details_catalog_database_sha256"]
        != sha(
            ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1/"
            "B5_SELECTION_CATALOG_SNAPSHOT.sqlite3"
        )
        or fetch["frozen_selection_sha256"] != sha(FROZEN)
        or fetch["selected_after_capture"] != 8
        or len(fetch["attempts"]) != 8
        or original["frozen_fetch_receipt_sha256"] != sha(FETCH)
        or original["frozen_pre_detail_selection_sha256"] != sha(FROZEN)
        or original["frozen_isolated_source_database_sha256"] != sha(DB)
        or original["original_html_sha_verified"] != 8
        or original["model_requests"] != 0
        or review["frozen_selection_sha256"] != sha(FROZEN)
        or review["frozen_source_manifest_sha256"] != sha(ORIGINAL)
        or review["frozen_source_snapshot_sha256"] != sha(DB)
        or review["source_only_reviewed_before_any_B5_candidate_inference"] is not True
        or review["model_results_inspected_before_review"] is not False
        or review["anchor_count"] != 76
        or options["original_review_sha256"] != sha(REVIEW)
        or options["source_snapshot_sha256"] != sha(DB)
        or options["model_or_candidate_outputs_inspected_before_supplement"] is not False
        or len(options["alternative_anchors"]) != 4
        or result["frozen_selection_sha256"] != sha(FROZEN)
        or result["original_manifest_sha256"] != sha(ORIGINAL)
        or result["original_review_sha256"] != sha(REVIEW)
        or result["original_alternatives_supplement_sha256"] != sha(OPTIONS)
        or result["source_snapshot_sha256"] != sha(DB)
        or result["frozen_candidate_source_sha256"] != frozen["candidate_B2v4_source_sha256"]
        or result["fresh_cohort_now_exposed"] is not True
        or result["B3_translation_requests"] != 0
        or result["B4_analysis_requests"] != 0
        or result["v30_requests"] != 0
        or result["accepted_employer_facts"] != 0
    ):
        raise ValueError("Fourth frozen/source-first sequence, code or production drift")
    selected = frozen["primary"]
    if (
        len(selected) != 8
        or len({x["source_job_id"] for x in selected}) != 8
        or [x["source_job_id"] for x in selected] != [x["source_job_id"] for x in review["entries"]]
        or [x["source_job_id"] for x in selected]
        != [x["source_job_id"] for x in original["entries"]]
    ):
        raise ValueError("Fourth source order was changed")
    with sqlite3.connect(f"file:{DB.resolve()}?mode=ro", uri=True) as con:
        if (
            con.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
            or con.execute("PRAGMA foreign_key_check").fetchall()
            or con.execute("SELECT COUNT(*) FROM job_detail_versions").fetchone()[0] != 8
            or con.execute("SELECT COUNT(*) FROM job_analysis_artifacts").fetchone()[0] != 0
        ):
            raise ValueError("Fourth isolated source SQLite no longer clean")
    source_store = TranslationStore(DB)
    source_versions = {}
    originals = {x["source_job_id"]: x for x in original["entries"]}
    for job in (x["source_job_id"] for x in selected):
        src = source_store.latest_source_version(job)
        rec = originals[job]
        if src is None or src.semantic_sha256 != rec["original_semantic_sha256"]:
            raise ValueError("Fourth original source SHA drift")
        raw = Path(rec["private_raw_html_path"])
        if (
            not raw.resolve().is_relative_to(PRIVATE.resolve())
            or sha(raw) != rec["raw_html_sha256"]
            or _semantic_sha256(parse_jobinja_detail(raw.read_bytes().decode()).to_dict())
            != src.semantic_sha256
        ):
            raise ValueError("Fourth raw HTML or parsed source fingerprint changed")
        source_versions[job] = src
    reviewed = json.loads(json.dumps(review))
    for extra in options["alternative_anchors"]:
        reviewed_job = next(
            x for x in reviewed["entries"] if x["source_job_id"] == extra["source_job_id"]
        )
        reviewed_job["reviewed_original_anchors"].append(
            {k: v for k, v in extra.items() if k != "source_job_id"}
        )
    reviewed["anchor_count"] += len(options["alternative_anchors"])

    def engine(src):
        rec = originals[src.source_job_id]
        return interpret_original_source_candidate_v4(
            src,
            raw_job_page=Path(rec["private_raw_html_path"]).read_bytes(),
            expected_html_sha256=rec["raw_html_sha256"],
        )

    evaluate = runpy.run_path(str(ROOT / "scripts/evaluate_p16_b5_source_gate.py"))[
        "evaluate_source_gate"
    ]
    replay = evaluate(
        frozen={"selected_primary": selected},
        review=reviewed,
        source_versions=source_versions,
        engine=engine,
    )
    ignored = {
        "evaluation_time_utc",
        "frozen_selection_sha256",
        "original_manifest_sha256",
        "original_review_sha256",
        "original_alternatives_supplement_sha256",
        "source_snapshot_sha256",
        "frozen_candidate_source_sha256",
        "selected_before_source_review_commit",
        "fresh_cohort_now_exposed",
        "B3_translation_requests",
        "B4_analysis_requests",
        "v30_requests",
        "accepted_employer_facts",
        "B6_promotion_authorized",
    }
    if {k: v for k, v in replay.items() if k not in ignored} != {
        k: v for k, v in result.items() if k not in ignored
    }:
        raise ValueError("Fourth prospectively frozen failure replay drifted")
    counts = result["counts"]
    if (
        result["disposition"] != "BLOCKED_UPSTREAM_SOURCE_SEMANTICS"
        or counts["frozen_source_first_anchor_count"] != 80
        or counts["candidate_role_match_anchor_count"] != 56
        or counts["candidate_role_mismatch_anchor_count"] != 13
        or counts["explicit_duty_missed_anchor_count"] != 1
        or counts["optional_or_negative_required_overstatement_count"] != 0
        or counts["multi_specialty_alternative_structure_missing_jobs"] != 1
    ):
        raise ValueError("Fourth critical source failure was hidden or altered")
    return {
        "status": "PASS_REPLAY_FOURTH_UNSEEN_SOURCE_GATE_FAILURE_NOT_B5_ACCEPTANCE",
        "source_jobs": 8,
        "selected_original_assertions": 80,
        "role_mismatches": 13,
        "explicit_duties_missed": 1,
        "unrepresented_alternatives_jobs": 1,
        "candidate_frozen_pre_source": True,
        "source_cohort_now_exposed": True,
        "new_model_requests": 0,
        "production_database_unchanged": True,
        "B5_accepted": False,
        "B6_activated": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
