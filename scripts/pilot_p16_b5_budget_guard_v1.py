#!/usr/bin/env python3
"""One frozen, exposed B5 local translation budget pilot; never unseen acceptance.

--freeze records 5 preselected source-owned batches and the assistant's
original-source-only interpretation BEFORE any model outputs.
--execute issues at most seven actual local HTTP model attempts within 240s,
including retries and truncation recovery. Raw inputs and model outputs remain
under ignored data/local-acceptance/; only safe aggregate may be published.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.source_bound_translation_b3 import CapturingHTTPTransport, select_b3_items
from jobhunter.source_bound_translation_batch_b5 import (
    BoundedBatchLMStudioProvider,
    evaluate_batched_translation,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_bound_translation_budget_b5 import (
    B5_PHYSICAL_BUDGET_CONTRACT,
    B5PhysicalBudget,
    B5PhysicalBudgetTransport,
    B5WallBudgetExceeded,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
PILOT = BASE / "budgeted-variety-pilot-v1"
REVIEW = PILOT / "SOURCE_FIRST_ASSISTANT_REVIEW.json"
SCOPE = PILOT / "FROZEN_SCOPE.json"
RESULT = PILOT / "PRIVATE_RESULT.json"
# Five different semantic risk types spanning 3 already-exposed postings.
SAMPLE_BATCH_PREFIXES = (
    "6d1b95a8",  # backend duties
    "e149b068",  # required strength, familiarity and named entities
    "4599acef",  # specialty-recruiting and explicit negation
    "482619c0",  # one-or-more specialty priority
    "8ec4f898",  # advantageous/optional named technical tools
)
MODEL = "gemma-4-e2b-it"
ENDPOINT = "http://127.0.0.1:18080/v1"
MAX_ATTEMPTS = 7
WALL_SECONDS = 240.0


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return obj


def write_once(path: Path, value: dict) -> None:
    if path.exists():
        raise ValueError(f"Frozen evidence cannot be overwritten: {path}")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        tmp.chmod(0o600)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def chosen_batches():
    selected = read(BASE / "B5_SELECTION_FROZEN.json")
    store = TranslationStore(BASE / "B5_8_SOURCE_SNAPSHOT.sqlite3")
    items = []
    for row in selected["selected_primary"]:
        source = store.latest_source_version(row["source_job_id"])
        if source is None:
            raise ValueError("Missing frozen original source")
        candidate = interpret_original_source_candidate_v2(source)
        choice = select_b3_items(source.source_job_id, candidate.items)
        items.extend(prepare_source_batch_items(source, choice.translate_items))
    plan = plan_source_batches(items, max_batch_items=3)
    chosen = []
    for prefix in SAMPLE_BATCH_PREFIXES:
        matches = [b for b in plan.batches if b.batch_id.startswith(prefix)]
        if len(matches) != 1:
            raise ValueError(f"Candidate plan changed before live pilot: {prefix}")
        chosen.append(matches[0])
    if len({b.source_job_id for b in chosen}) != 3:
        raise ValueError("Variety pilot requires three exposed source jobs")
    return chosen


def freeze() -> dict:
    if SCOPE.exists() or RESULT.exists():
        raise ValueError("The budget pilot scope/result is already sealed")
    batches = chosen_batches()
    source_review = read(REVIEW)
    if (
        source_review.get("source_review_type")
        != "assistant_exposed_original_before_new_translation"
        or source_review.get("unseen_claim") is not False
        or source_review.get("model_outputs_seen_during_review") is not False
    ):
        raise ValueError("Only a pre-model original-only exposed review may freeze this pilot")
    expected = [
        (b.batch_id, x.source_anchor_id, x.source_span_sha256) for b in batches for x in b.items
    ]
    observed = [
        (x["batch_id"], x["source_anchor_id"], x["source_span_sha256"])
        for x in source_review["reviewed_source_items"]
    ]
    if expected != observed:
        raise ValueError("Source-only review must match every exact chosen source anchor")
    frozen = {
        "contract": "jobhunter-p16-b5-exposed-physical-budget-variety-pilot-v1",
        "date_utc": datetime.now(UTC).isoformat(),
        "source_cohort": "previously_exposed_regression_not_unseen",
        "source_first_review_sha256": sha(REVIEW),
        "original_snapshot_sha256": sha(BASE / "B5_8_SOURCE_SNAPSHOT.sqlite3"),
        "previous_exposed_batch_preflight_sha256": sha(
            BASE / "B5_TRANSLATION_BATCH_PREFLIGHT.json"
        ),
        "B2v2_source_sha256": sha(ROOT / "src/jobhunter/source_item_candidate_b2_v2.py"),
        "batch_planner_source_sha256": sha(
            ROOT / "src/jobhunter/source_bound_translation_batch_b5.py"
        ),
        "budget_guard_source_sha256": sha(
            ROOT / "src/jobhunter/source_bound_translation_budget_b5.py"
        ),
        "pilot_script_sha256": sha(Path(__file__)),
        "production_database_sha256": sha(ROOT / "data/jobhunter.sqlite3"),
        "public_corpus_sha256": sha(ROOT / "corpus/manifest.json"),
        "physical_attempt_guard_contract": B5_PHYSICAL_BUDGET_CONTRACT,
        "max_physical_http_attempts": MAX_ATTEMPTS,
        "max_wall_seconds": WALL_SECONDS,
        "max_retries_per_logical_invocation": 1,
        "max_selected_logical_batches": len(batches),
        "selected_original_source_items": len(expected),
        "model": MODEL,
        "endpoint": ENDPOINT,
        "batch_identity": [
            {
                "batch_id": b.batch_id,
                "source_job_id": b.source_job_id,
                "source_anchor_ids": [x.source_anchor_id for x in b.items],
                "source_span_sha256s": [x.source_span_sha256 for x in b.items],
                "category": b.items[0].category,
                "strength": b.items[0].strength,
            }
            for b in batches
        ],
        "B5_80_paired_analysis_call_budget_is_separate": True,
        "accepted_employer_facts": 0,
        "unseen_B5_evaluation": False,
        "B6_promotion": False,
    }
    write_once(SCOPE, frozen)
    return frozen


def verify_scope() -> tuple[dict, list]:
    scope = read(SCOPE)
    pairs = (
        (REVIEW, "source_first_review_sha256"),
        (BASE / "B5_8_SOURCE_SNAPSHOT.sqlite3", "original_snapshot_sha256"),
        (BASE / "B5_TRANSLATION_BATCH_PREFLIGHT.json", "previous_exposed_batch_preflight_sha256"),
        (ROOT / "src/jobhunter/source_item_candidate_b2_v2.py", "B2v2_source_sha256"),
        (
            ROOT / "src/jobhunter/source_bound_translation_batch_b5.py",
            "batch_planner_source_sha256",
        ),
        (
            ROOT / "src/jobhunter/source_bound_translation_budget_b5.py",
            "budget_guard_source_sha256",
        ),
        (Path(__file__), "pilot_script_sha256"),
        (ROOT / "data/jobhunter.sqlite3", "production_database_sha256"),
        (ROOT / "corpus/manifest.json", "public_corpus_sha256"),
    )
    if any(sha(path) != scope[key] for path, key in pairs):
        raise ValueError("Frozen source/model code identity or production state drifted")
    batches = chosen_batches()
    if [(b.batch_id, [x.source_anchor_id for x in b.items]) for b in batches] != [
        (x["batch_id"], x["source_anchor_ids"]) for x in scope["batch_identity"]
    ]:
        raise ValueError("Frozen selected source batches changed")
    if (
        scope["model"] != MODEL
        or scope["endpoint"] != ENDPOINT
        or scope["max_physical_http_attempts"] != MAX_ATTEMPTS
        or scope["max_wall_seconds"] != WALL_SECONDS
        or scope["max_selected_logical_batches"] != len(batches)
    ):
        raise ValueError("Frozen model transport or budget policy changed")
    return scope, batches


def execute() -> dict:
    if RESULT.exists():
        raise ValueError("Cannot rerun a completed pilot")
    scope, batches = verify_scope()
    capture = CapturingHTTPTransport()
    guard = B5PhysicalBudgetTransport(
        budget=B5PhysicalBudget(MAX_ATTEMPTS, WALL_SECONDS),
        inner=capture,
    )
    provider = BoundedBatchLMStudioProvider(
        base_url=ENDPOINT,
        configured_model=MODEL,
        max_retries=1,
        timeout_seconds=15,
        max_tokens=4096,
        transport=guard,
    )
    responses = []
    started = time.monotonic()
    try:
        with guard:
            for batch in batches:
                if guard.attempted_http_dispatches >= MAX_ATTEMPTS or guard.wall_deadline_hit:
                    responses.append(
                        {
                            "batch_id": batch.batch_id,
                            "state": "not_attempted_budget_exhausted",
                            "source_anchor_ids": [x.source_anchor_id for x in batch.items],
                        }
                    )
                    continue
                try:
                    result = evaluate_batched_translation(batch, provider)
                    responses.append(
                        {"batch_id": batch.batch_id, "state": "attempted", "result": result}
                    )
                except B5WallBudgetExceeded:
                    responses.append(
                        {
                            "batch_id": batch.batch_id,
                            "state": "interrupted_wall_budget",
                            "source_anchor_ids": [x.source_anchor_id for x in batch.items],
                        }
                    )
                    break
    finally:
        # The original provider's short-lived clients do not own the capture transport.
        capture.close_inner()
    raw_events = []
    for number, event in enumerate(capture.events, start=1):
        folder = PILOT / "raw" / f"attempt-{number:02d}"
        if folder.exists():
            raise ValueError("Raw evidence directory already exists")
        folder.mkdir(parents=True, mode=0o700)
        request_path = folder / "request.json"
        request_path.write_bytes(event.request_body)
        request_path.chmod(0o600)
        response_path = None
        if event.response_body is not None:
            response_path = folder / "response.json"
            response_path.write_bytes(event.response_body)
            response_path.chmod(0o600)
        raw_events.append(
            {
                "ordinal": number,
                "method": event.method,
                "url_path": event.url_path,
                "status_code": event.response_status,
                "error_type": event.error_type,
                "elapsed_seconds": round(event.elapsed_seconds, 3),
                "request_sha256": sha(request_path),
                "response_sha256": sha(response_path) if response_path else None,
                "private_request_path": str(request_path.relative_to(PILOT)),
                "private_response_path": str(response_path.relative_to(PILOT))
                if response_path
                else None,
            }
        )
    record = {
        "contract": scope["contract"],
        "source_cohort": scope["source_cohort"],
        "scope_sha256": sha(SCOPE),
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "model": MODEL,
        "attempt_budget": guard.safe_summary(),
        "actual_captured_HTTP_requests": len(raw_events),
        "http_events": raw_events,
        "responses": responses,
        "run_elapsed_seconds": round(time.monotonic() - started, 3),
        "per_item_linguistic_quality": "not_yet_reviewed",
        "new_unseen_B5": False,
        "accepted_employer_facts": 0,
        "production_database_unchanged": sha(ROOT / "data/jobhunter.sqlite3")
        == scope["production_database_sha256"],
        "public_corpus_unchanged": sha(ROOT / "corpus/manifest.json")
        == scope["public_corpus_sha256"],
    }
    write_once(RESULT, record)
    if (
        record["actual_captured_HTTP_requests"] > MAX_ATTEMPTS
        or guard.attempted_http_dispatches > MAX_ATTEMPTS
        or not record["production_database_unchanged"]
        or not record["public_corpus_unchanged"]
    ):
        raise ValueError("Live B5 pilot guardrail failed: check frozen private result")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--freeze", action="store_true")
    modes.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result = freeze() if args.freeze else execute()
    if args.freeze:
        print(
            json.dumps(
                {
                    "state": "FROZEN_BEFORE_LOCAL_INFERENCE",
                    "batches": result["max_selected_logical_batches"],
                    "original_items": result["selected_original_source_items"],
                    "max_http_attempts": result["max_physical_http_attempts"],
                    "max_wall_seconds": result["max_wall_seconds"],
                    "unseen_claim": False,
                }
            )
        )
    else:
        print(
            json.dumps(
                {
                    "state": "EXECUTED_EXPOSED_BUDGETED_PILOT",
                    "physical_attempts": result["attempt_budget"]["attempted_http_dispatches"],
                    "captured_http_requests": result["actual_captured_HTTP_requests"],
                    "logical_batches": len(result["responses"]),
                    "wall_deadline_hit": result["attempt_budget"]["wall_deadline_hit"],
                    "production_database_unchanged": result["production_database_unchanged"],
                    "unseen_claim": False,
                }
            )
        )


if __name__ == "__main__":
    main()
