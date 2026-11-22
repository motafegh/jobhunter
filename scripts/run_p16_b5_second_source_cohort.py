#!/usr/bin/env python3
"""B5 second fresh-source cohort: metadata-only freeze, isolated fetch, SHA seal.

No candidate B2/B3/B4 inference is permitted here. Selection uses only
pre-existing 2026-11-21 Jobinja search metadata; this is a *fresh original
source assessment cohort*, not a claim that the ads were newly posted or that
their titles were unknown. Fetch source only via approved JobinjaClient; do not
invoke CLI hooks that regenerate the tracked public corpus.

Modes must run in order: --freeze-selection, --capture, --freeze-sources.
Files under ignored local-acceptance are private and one-write immutable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.evidence import EvidenceStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_detail_service import (
    JobinjaDetailService,
    _semantic_sha256,
)
from jobhunter.jobinja_details import parse_jobinja_detail
from jobhunter.sources.jobinja import JobinjaAcquisitionError, JobinjaClient
from jobhunter.storage import JobHunterStore
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen"
OUT = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-22/second-source-cohort-v1"
SELECTION = OUT / "FROZEN_METADATA_SELECTION.json"
FETCH = OUT / "PRIVATE_FETCH_RECEIPT.json"
ORIGINAL = OUT / "ORIGINAL_SOURCES_FROZEN_BEFORE_REVIEW.json"
CATALOG = PREVIOUS / "B5_SELECTION_CATALOG_SNAPSHOT.sqlite3"
DATABASE = OUT / "isolated-second-cohort.sqlite3"
# Explicit title/metadata-only strata; no source descriptions evaluated.
PRIMARY: dict[str, tuple[str, ...]] = {
    "python_backend_software": ("tT2O", "tEA4"),
    "applied_ai_llm_agents": ("tHga", "t11I", "tMXH"),
    "security_network_assessment": ("t1QT", "tMZa", "t1Uc"),
}
RESERVE: dict[str, tuple[str, ...]] = {
    "python_backend_software": ("tu4K",),
    "applied_ai_llm_agents": ("t1RL",),
    "security_network_assessment": ("tPah",),
}
MAX_PHYSICAL_SOURCE_PAGES = 11
# Explicit proposed translation-only resource ceiling; not the old 80-call
# paired B4/v30 budget, and never automatically executes translation.
PROPOSED_TRANSLATION_BUDGET = {
    "candidate_translation_max_physical_http_attempts": 80,
    "candidate_translation_max_active_wall_seconds": 7200,
    "candidate_translation_max_items_per_batch": 3,
    "candidate_translation_max_characters_per_batch": 1200,
    "candidate_translation_max_retries_per_logical_invocation": 1,
    "candidate_translation_session_max_physical_http_attempts": 8,
    "candidate_translation_session_max_wall_seconds": 900,
    "treatment_of_deferred_oversized_items": "untranslated_unresolved_no_truncation",
    "on_budget_reached": "halt_no_unapproved_extra_requests",
    "analysis_paired_budget_independent": 80,
    "no_model_calls_until_original_source_first_semantic_gate": True,
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("Invalid frozen B5 metadata")
    return obj


def write_once(path: Path, value: dict) -> None:
    if path.exists():
        raise ValueError(f"Existing frozen file: {path}")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    try:
        with temp.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temp.chmod(0o600)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def metadata_selection(
    pool: dict[str, Any],
    old: dict[str, Any],
    known: list[str],
    corpus: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    """Predeclared roles, no details; exclude prior seen/related identities."""
    records = pool["records"]
    lookup = {r["source_job_id"]: r for r in records}
    if len(lookup) != len(records):
        raise ValueError("Ambiguous duplicate metadata posting identity")
    prior = [x["metadata"] for role in ("selected_primary", "reserve_order") for x in old[role]]
    already_known_ids = set(known)
    # Full public corpus names may include historical observations absent B0.
    corpus_ids = {
        row["source_job_id"]
        for row in corpus.get("jobs", [])
        if isinstance(row, dict) and "source_job_id" in row
    }
    prior_ids = {x["source_job_id"] for x in prior}
    prior_companies = {x["company_slug"] for x in prior}
    prior_name_pairs = {
        (x["company_slug"], " ".join(x["title_observed"].casefold().split())) for x in prior
    }
    selected_companies: set[str] = set()
    planned: list[dict[str, Any]] = []
    spare: list[dict[str, Any]] = []
    for destination, table in ((planned, PRIMARY), (spare, RESERVE)):
        for stratum, job_ids in table.items():
            for job in job_ids:
                rec = lookup.get(job)
                if rec is None:
                    raise ValueError(f"Metadata-only selected job not in source pool: {job}")
                pair = (
                    rec["company_slug"],
                    " ".join(rec["title_observed"].casefold().split()),
                )
                if (
                    rec["exclusion_reasons"]
                    or rec["selection_role"] != "not_selected"
                    or job in already_known_ids | corpus_ids | prior_ids
                    or rec["company_slug"] in prior_companies | selected_companies
                    or pair in prior_name_pairs
                    or rec["previous_same_company_different_title_count"] > 3
                ):
                    raise ValueError(f"Metadata candidate was known, related or ineligible: {job}")
                selected_companies.add(rec["company_slug"])
                destination.append(
                    {
                        "stratum": stratum,
                        "source_job_id": job,
                        "metadata": rec,
                    }
                )
    if len(planned) != 8 or len(spare) != 3:
        raise ValueError("B5 fixed 2/3/3 primary and three backup strata missing")
    if len({x["source_job_id"] for x in planned + spare}) != 11:
        raise ValueError("Duplicate selected/reserve original source identity")
    excluded = sum(bool(rec["exclusion_reasons"]) for rec in records)
    return (
        planned,
        spare,
        {
            "pool_total": len(records),
            "ineligible_original_pool": excluded,
            "selected_primary": len(planned),
            "declared_reserves": len(spare),
        },
    )


def freeze_selection() -> dict:
    if SELECTION.exists() or OUT.exists():
        raise ValueError("B5 second cohort is already initialized")
    pool = read(PREVIOUS / "B5_METADATA_SELECTION_POOL.json")
    old = read(PREVIOUS / "B5_SELECTION_FROZEN.json")
    known = json.loads((B0 / "EXCLUSION_KNOWN_JOB_IDS_PRIVATE.json").read_text(encoding="utf-8"))
    if not isinstance(known, list) or not all(isinstance(x, str) for x in known):
        raise ValueError("B0 known exposure index not a string list")
    corpus = read(ROOT / "corpus/manifest.json")
    primary, reserves, counts = metadata_selection(pool, old, known, corpus)
    assert sha(CATALOG) == old["frozen_pre_detail_catalog_sqlite_sha256"]
    snapshot = {
        "contract": "jobhunter-p16-b5-second-cohort-metadata-freeze-v1",
        "frozen_at_utc": datetime.now(UTC).isoformat(),
        "source_search_metadata_captured_on": "2026-11-21",
        "source_posts_newly_posted": "not_claimed",
        "source_contents_seen_before_selection": False,
        "source_assessment_or_model_output_seen_before_selection": False,
        "assistant_reviewer_blind_to_prior_research": False,
        "selection_method": "fixed_title_metadata_strata_2_backend_3_ai_3_security",
        "primary": primary,
        "reserve": reserves,
        "counts": counts,
        "old_known_metadata_pool_sha256": sha(PREVIOUS / "B5_METADATA_SELECTION_POOL.json"),
        "old_primary_reserve_selection_sha256": sha(PREVIOUS / "B5_SELECTION_FROZEN.json"),
        "B0_known_exclusions_sha256": sha(B0 / "EXCLUSION_KNOWN_JOB_IDS_PRIVATE.json"),
        "public_corpus_manifest_sha256": sha(ROOT / "corpus/manifest.json"),
        "pre_details_catalog_database_sha256": sha(CATALOG),
        "production_database_sha256": sha(ROOT / "data/jobhunter.sqlite3"),
        "hard_max_source_page_requests_or_retries": MAX_PHYSICAL_SOURCE_PAGES,
        "only_approved_source_adapter": "JobinjaClient",
        "candidate_translation_resource_policy_separate_from_analysis": PROPOSED_TRANSLATION_BUDGET,
        "candidate_version": "B2v2_frozen_original_source_parser",
        "candidate_B2v2_source_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"),
        "existing_B4v5_status": "unchanged_candidate_only",
        "no_analysis_or_model_inference_before_source_first_review": True,
        "B5": "evaluation_pending",
        "B6": "not_authorized",
    }
    write_once(SELECTION, snapshot)
    return snapshot


def capture() -> dict:
    if not SELECTION.exists() or FETCH.exists() or ORIGINAL.exists() or DATABASE.exists():
        raise ValueError("B5 second cohort prerequisite/destination unexpected")
    frozen = read(SELECTION)
    if (
        frozen["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json")
        or frozen["production_database_sha256"] != sha(ROOT / "data/jobhunter.sqlite3")
        or frozen["pre_details_catalog_database_sha256"] != sha(CATALOG)
        or frozen["candidate_B2v2_source_sha256"]
        != sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py")
    ):
        raise ValueError("Production/reference drift before source acquisition")
    # Isolated snapshot from metadata catalog predating the first cohort's details.
    shutil.copyfile(CATALOG, DATABASE)
    store = JobHunterStore(DATABASE)
    observations = JobDetailObservationStore(DATABASE)
    service = JobinjaDetailService(
        client=JobinjaClient(
            user_agent="JobHunter/0.1 (local personal career research)",
            timeout_seconds=30,
            max_retries=0,
            use_env_proxy=False,
        ),
        evidence_store=EvidenceStore(OUT / "evidence"),
        store=store,
        observation_store=observations,
    )
    attempted: list[dict] = []
    primary, reserves = frozen["primary"], frozen["reserve"]
    successful: list[dict] = []
    for stratum, total in (
        ("python_backend_software", 2),
        ("applied_ai_llm_agents", 3),
        ("security_network_assessment", 3),
    ):
        choices = [x for x in primary + reserves if x["stratum"] == stratum]
        for choice in choices:
            if sum(x["stratum"] == stratum for x in successful) >= total:
                break
            if len(attempted) >= MAX_PHYSICAL_SOURCE_PAGES:
                break
            job = choice["source_job_id"]
            try:
                detail = service.fetch(job)
                status = detail.parse_status
                ok = status == "parsed"
                attempted.append(
                    {
                        "source_job_id": job,
                        "stratum": stratum,
                        "fetch_status": "parsed" if ok else "not_parsed",
                        "detail_version_id": detail.version_id,
                        "parse_status": status,
                        "source_title": detail.title,
                    }
                )
                if ok:
                    successful.append(choice)
            except JobinjaAcquisitionError as exc:
                attempted.append(
                    {
                        "source_job_id": job,
                        "stratum": stratum,
                        "fetch_status": exc.classification,
                        "retryable": exc.retryable,
                        "status_code": exc.status_code,
                    }
                )
                if exc.classification in {"challenge", "auth_required", "rate_limited"}:
                    # No bypass or trying a different path when source restricts access.
                    break
            if len(attempted) < MAX_PHYSICAL_SOURCE_PAGES:
                time.sleep(1.0)
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert not conn.execute("PRAGMA foreign_key_check").fetchall()
        row_count = conn.execute("SELECT COUNT(*) FROM job_detail_versions").fetchone()[0]
    receipt = {
        "contract": "jobhunter-p16-b5-second-cohort-isolated-acquisition-v1",
        "capture_finished_at_utc": datetime.now(UTC).isoformat(),
        "frozen_selection_sha256": sha(SELECTION),
        "attempts": attempted,
        "successful_source_list": successful,
        "selected_after_capture": len(successful),
        "source_detail_rows_in_isolated_database": row_count,
        "isolated_source_database_sha256": sha(DATABASE),
        "production_database_unchanged": frozen["production_database_sha256"]
        == sha(ROOT / "data/jobhunter.sqlite3"),
        "public_corpus_unchanged": frozen["public_corpus_manifest_sha256"]
        == sha(ROOT / "corpus/manifest.json"),
        "no_B2_B3_B4_v30_model_calls": True,
        "original_source_only_review_still_required": True,
        "B5": "pending_source_first_review",
        "B6": "not_authorized",
    }
    write_once(FETCH, receipt)
    return receipt


def freeze_sources() -> dict:
    if not FETCH.exists() or ORIGINAL.exists():
        raise ValueError("B5 source capture needs a single frozen manifest")
    frozen = read(SELECTION)
    fetched = read(FETCH)
    if fetched["selected_after_capture"] != 8:
        raise ValueError("No eight available sources; do not weaken source-first quota")
    if sha(DATABASE) != fetched["isolated_source_database_sha256"]:
        raise ValueError("Source evidence SQLite mutated before manifest freeze")
    if frozen["production_database_sha256"] != sha(ROOT / "data/jobhunter.sqlite3"):
        raise ValueError("Production DB changed after independent fetch")
    if frozen["public_corpus_manifest_sha256"] != sha(ROOT / "corpus/manifest.json"):
        raise ValueError("Public corpus changed after independent fetch")
    with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Isolated SQLite integrity error")
        if conn.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Isolated source SQLite FK check failed")
        rows = conn.execute(
            "SELECT p.source_job_id,v.id,v.content_sha256,v.semantic_sha256,"
            "v.evidence_path,v.metadata_path,v.fields_json,v.parse_status,"
            "v.parser_version FROM job_detail_versions AS v "
            "JOIN job_postings AS p ON p.id=v.job_posting_id "
            "ORDER BY v.id"
        ).fetchall()
        if len(rows) != 8:
            raise ValueError("Only eight isolated original-source versions may be frozen")
    source_by_id = {r["source_job_id"]: r for r in rows}
    store = TranslationStore(DATABASE)
    entries = []
    for selected in fetched["successful_source_list"]:
        job = selected["source_job_id"]
        r = source_by_id[job]
        raw = Path(r["evidence_path"])
        metadata = Path(r["metadata_path"])
        raw_reparsed = parse_jobinja_detail(raw.read_text(encoding="utf-8"))
        fields = json.loads(r["fields_json"])
        parsed = raw_reparsed.to_dict()
        if (
            sha(raw) != r["content_sha256"]
            or _semantic_sha256(parsed) != r["semantic_sha256"]
            or _semantic_sha256(fields) != r["semantic_sha256"]
            or store.latest_source_version(job).semantic_sha256 != r["semantic_sha256"]
        ):
            raise ValueError("Raw HTML / parsed original SHA mismatch")
        entries.append(
            {
                "source_job_id": job,
                "stratum": selected["stratum"],
                "original_semantic_sha256": r["semantic_sha256"],
                "raw_html_sha256": r["content_sha256"],
                "raw_metadata_sha256": sha(metadata),
                "private_raw_html_path": str(raw),
                "private_raw_metadata_path": str(metadata),
                "original_description_length": len(fields["description"]),
                "language_hint": fields.get("language"),
                "job_detail_version_id": r["id"],
                "parser_version": r["parser_version"],
                "parse_status": r["parse_status"],
            }
        )
    receipt = {
        "contract": "jobhunter-p16-b5-second-cohort-original-source-seal-v1",
        "sealed_at_utc": datetime.now(UTC).isoformat(),
        "frozen_pre_detail_selection_sha256": sha(SELECTION),
        "frozen_fetch_receipt_sha256": sha(FETCH),
        "frozen_isolated_source_database_sha256": sha(DATABASE),
        "source_only_original_reading": "not_started",
        "original_source_review_before_candidate_output": True,
        "model_requests": 0,
        "original_html_sha_verified": len(entries),
        "source_statement_review": "unstarted",
        "independent_human_blind_review": False,
        "prior_history_blindness": False,
        "source_posts_newly_posted": "not_claimed",
        "production_database_unchanged": True,
        "public_corpus_unchanged": True,
        "entries": entries,
        "B5": "pending_original_source_only_assessment",
        "B6": "not_authorized",
    }
    write_once(ORIGINAL, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--freeze-selection", action="store_true")
    modes.add_argument("--capture", action="store_true")
    modes.add_argument("--freeze-sources", action="store_true")
    args = parser.parse_args()
    obj = (
        freeze_selection()
        if args.freeze_selection
        else capture()
        if args.capture
        else freeze_sources()
    )
    if args.freeze_selection:
        print(
            json.dumps(
                {
                    "status": "FROZEN_METADATA_BEFORE_SOURCE_DETAILS",
                    "selected_ids": [x["source_job_id"] for x in obj["primary"]],
                    "reserve_ids": [x["source_job_id"] for x in obj["reserve"]],
                    "strata": [x["stratum"] for x in obj["primary"]],
                    "no_model_calls": True,
                }
            )
        )
    elif args.capture:
        print(
            json.dumps(
                {
                    "status": "ISOLATED_SOURCE_CAPTURE",
                    "selected_source_count": obj["selected_after_capture"],
                    "fetch_attempts": len(obj["attempts"]),
                    "source_db_unchanged": obj["production_database_unchanged"],
                    "public_corpus_unchanged": obj["public_corpus_unchanged"],
                }
            )
        )
    else:
        print(
            json.dumps(
                {
                    "status": "FROZEN_ORIGINAL_SOURCE_BEFORE_SOURCE_REVIEW",
                    "original_sources_verified": obj["original_html_sha_verified"],
                    "no_model_calls": True,
                    "source_first_review_done": False,
                }
            )
        )


if __name__ == "__main__":
    main()
