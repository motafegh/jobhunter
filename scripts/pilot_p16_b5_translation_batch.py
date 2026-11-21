#!/usr/bin/env python3
"""Frozen local-only B5 batching pilot on EXPOSED original-source items.

--freeze records a two-preferred-item source batch before any model request.
--execute compares one batch with two individual v2 translations, all local.
Raw original quotes, requests, responses and output remain ignored/private.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import signal
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

from jobhunter.source_bound_translation_b3 import (
    CapturingHTTPTransport,
    build_translation_review_flags,
    select_b3_items,
)
from jobhunter.source_bound_translation_batch_b5 import (
    BoundedBatchLMStudioProvider,
    evaluate_batched_translation,
    plan_source_batches,
    prepare_source_batch_items,
)
from jobhunter.source_item_candidate_b2_v2 import interpret_original_source_candidate_v2
from jobhunter.translation.lm_studio import LMStudioTranslationProvider
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
B5 = ROOT / "data/local-acceptance/p16-stage-b5-2026-11-21/acquisition-v1"
OUT = B5 / "batch-pilot-v1"
SCOPE = OUT / "FROZEN_SCOPE.json"
RESULT = OUT / "PRIVATE_RESULT.json"
MODEL = "gemma-4-e2b-it"
URL = "http://127.0.0.1:18080/v1"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_once(path: Path, data: dict) -> None:
    if path.exists():
        raise ValueError("Pilot evidence is immutable: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    path.chmod(0o600)


def chosen_batch():
    selection = json.loads((B5 / "B5_SELECTION_FROZEN.json").read_text())
    store = TranslationStore(B5 / "B5_8_SOURCE_SNAPSHOT.sqlite3")
    all_items = []
    for entry in selection["selected_primary"]:
        s = store.latest_source_version(entry["source_job_id"])
        c = interpret_original_source_candidate_v2(s)
        b3 = select_b3_items(s.source_job_id, c.items)
        all_items.extend(prepare_source_batch_items(s, b3.translate_items))
    plan = plan_source_batches(all_items, max_batch_items=3)
    return min(
        (
            x
            for x in plan.batches
            if len(x.items) == 2
            and x.items[0].category == "candidate_qualification"
            and x.items[0].strength == "preferred"
        ),
        key=lambda x: (x.total_source_characters, x.batch_id),
    )


def freeze_scope() -> dict:
    if OUT.exists():
        raise ValueError("Pilot scope already frozen")
    batch = chosen_batch()
    plan = json.loads((B5 / "B5_TRANSLATION_BATCH_PREFLIGHT.json").read_text())
    assert batch.batch_id in {x["batch_id"] for x in plan["selected_batch_sources"]}
    frozen = {
        "contract": "p16-b5-exposed-local-translation-batch-pilot-v1",
        "date_utc": datetime.now(UTC).isoformat(),
        "source_cohort": "previously_exposed_eight_development_jobs",
        "source_first_modality": "two_preferred_qualification_candidates",
        "source_review_prior_to_model": True,
        "batch_id": batch.batch_id,
        "source_job_id": batch.source_job_id,
        "source_anchors": [x.source_anchor_id for x in batch.items],
        "source_hashes": [x.source_span_sha256 for x in batch.items],
        "model": MODEL,
        "endpoint": URL,
        "planned_invocations": 3,
        "max_physical_http_completion_attempts": 4,
        "max_per_invocation_seconds": 120,
        "preflight_sha256": sha(B5 / "B5_TRANSLATION_BATCH_PREFLIGHT.json"),
        "batch_code_sha256": sha(ROOT / "src/jobhunter/source_bound_translation_batch_b5.py"),
        "original_snapshot_sha256": sha(B5 / "B5_8_SOURCE_SNAPSHOT.sqlite3"),
        "production_db_sha256": sha(ROOT / "data/jobhunter.sqlite3"),
        "corpus_sha256": sha(ROOT / "corpus/manifest.json"),
        "acceptance_authority": "none",
    }
    write_once(SCOPE, frozen)
    return frozen


def execute() -> dict:
    if RESULT.exists():
        raise ValueError("Pilot has already been executed")
    frozen = json.loads(SCOPE.read_text())
    batch = chosen_batch()
    if (
        frozen["batch_id"] != batch.batch_id
        or frozen["source_anchors"] != [x.source_anchor_id for x in batch.items]
        or frozen["source_hashes"] != [x.source_span_sha256 for x in batch.items]
        or frozen["preflight_sha256"] != sha(B5 / "B5_TRANSLATION_BATCH_PREFLIGHT.json")
        or frozen["batch_code_sha256"]
        != sha(ROOT / "src/jobhunter/source_bound_translation_batch_b5.py")
        or frozen["original_snapshot_sha256"] != sha(B5 / "B5_8_SOURCE_SNAPSHOT.sqlite3")
        or frozen["production_db_sha256"] != sha(ROOT / "data/jobhunter.sqlite3")
        or frozen["corpus_sha256"] != sha(ROOT / "corpus/manifest.json")
    ):
        raise ValueError("Original pilot sources, scope or production identity changed")
    with httpx.Client(timeout=5, trust_env=False) as client:
        response = client.get(URL + "/models")
        response.raise_for_status()
        if MODEL not in {x["id"] for x in response.json()["data"]}:
            raise ValueError("Frozen Gemma model not listed by local LM Studio")
    transport = CapturingHTTPTransport()
    providers = [
        BoundedBatchLMStudioProvider(
            base_url=URL, configured_model=MODEL, transport=transport, max_retries=0
        ),
        LMStudioTranslationProvider(
            base_url=URL, configured_model=MODEL, transport=transport, max_retries=0
        ),
    ]
    outputs = []
    raw_events = []
    started = time.monotonic()

    def timeout_handler(_signum, _frame):
        raise TimeoutError("B5 single local inference invocation exceeded 120s")

    previous = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, timeout_handler)
    try:
        for index, name in enumerate(("batch", "single_0", "single_1")):
            if sum(e.url_path.endswith("/chat/completions") for e in transport.events) >= 4:
                outputs.append(
                    {
                        "stage": name,
                        "state": "unresolved",
                        "failure": "http_attempt_budget_exhausted",
                    }
                )
                break
            begin = len(transport.events)
            try:
                signal.alarm(120)
                if name == "batch":
                    out = evaluate_batched_translation(batch, providers[0])
                else:
                    item = batch.items[index - 1]
                    response = providers[1].translate_texts(
                        (item.exact_source_text,),
                        source_language="fa",
                        target_language="en",
                    )
                    target = response.texts[0]
                    out = {
                        "source_anchor_id": item.source_anchor_id,
                        "source_span_sha256": item.source_span_sha256,
                        "target_text": target,
                        "target_sha256": hashlib.sha256(target.encode()).hexdigest(),
                        "review_flags": list(
                            build_translation_review_flags(item.exact_source_text, target)
                        ),
                        "meaning_review": "unreviewed",
                    }
                outputs.append({"stage": name, "state": "returned", "result": out})
            except Exception as e:
                outputs.append(
                    {"stage": name, "state": "unresolved", "failure_type": type(e).__name__}
                )
            finally:
                signal.alarm(0)
            for n, event in enumerate(transport.events[begin:], start=1):
                folder = OUT / "raw" / f"{name}-{n:02d}"
                folder.mkdir(parents=True, mode=0o700, exist_ok=False)
                req = folder / "request.json"
                req.write_bytes(event.request_body)
                req.chmod(0o600)
                reply = None
                if event.response_body is not None:
                    reply = folder / "response.json"
                    reply.write_bytes(event.response_body)
                    reply.chmod(0o600)
                raw_events.append(
                    {
                        "stage": name,
                        "path": event.url_path,
                        "status": event.response_status,
                        "error_type": event.error_type,
                        "request_sha256": sha(req),
                        "response_sha256": sha(reply) if reply else None,
                        "private_request_path": str(req.relative_to(OUT)),
                        "private_response_path": str(reply.relative_to(OUT)) if reply else None,
                        "elapsed_seconds": round(event.elapsed_seconds, 3),
                    }
                )
            print(
                "EXPOSED local pilot",
                name,
                "POSTs",
                sum(e.url_path.endswith("/chat/completions") for e in transport.events),
                flush=True,
            )
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
        transport.close_inner()
    actual_calls = sum(e["path"].endswith("/chat/completions") for e in raw_events)
    result = {
        "contract": frozen["contract"],
        "frozen_scope_sha256": sha(SCOPE),
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        "logical_invocations": len(outputs),
        "physical_http_completion_attempts": actual_calls,
        "http_records": raw_events,
        "source_bound_candidate_outputs": outputs,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "no_unseen_B5_claim": True,
        "semantic_review_status": "not_yet_independently_reviewed",
        "accepted_employer_facts": 0,
        "production_database_unchanged": frozen["production_db_sha256"]
        == sha(ROOT / "data/jobhunter.sqlite3"),
    }
    write_once(RESULT, result)
    if actual_calls > frozen["max_physical_http_completion_attempts"]:
        raise ValueError("Pilot exceeded predeclared physical call ceiling")
    if not result["production_database_unchanged"]:
        raise ValueError("Production DB changed during exposed pilot")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--freeze", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = p.parse_args()
    out = freeze_scope() if args.freeze else execute()
    print(
        json.dumps(
            {
                key: out[key]
                for key in (
                    ("batch_id", "planned_invocations")
                    if args.freeze
                    else (
                        "logical_invocations",
                        "physical_http_completion_attempts",
                        "elapsed_seconds",
                        "production_database_unchanged",
                    )
                )
            },
            sort_keys=True,
        )
    )
