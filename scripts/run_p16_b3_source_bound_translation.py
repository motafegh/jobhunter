#!/usr/bin/env python3
"""Run the private, candidate-only P1.6 B3 source-bound translation experiment."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import runpy
import signal
import sqlite3
import tempfile
import time
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

from jobhunter.config import Settings
from jobhunter.source_bound_translation_b3 import (
    B3_CONTRACT_VERSION,
    B3_SELECTION_VERSION,
    CapturingHTTPTransport,
    build_translation_review_flags,
    make_b1_source_bound_alignment,
    make_b1_unresolved_alignment,
    make_native_identity_record,
    nested_leaf_parent_relations,
    select_b3_items,
    sha256_bytes,
    sha256_text,
)
from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import (
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation.lm_studio import _SYSTEM_PROMPT, LMStudioTranslationProvider
from jobhunter.translation.projection import contains_persian
from jobhunter.translation_store import TranslationStore

ROOT = Path(__file__).resolve().parents[1]
COHORT = ("tNhZ", "tMps", "tNDx", "tMjm")
B0_SHA256 = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
B2_CANDIDATE_SHA256 = "2b3618dbd9d68b939a974bb81b0ce2200bcdc8ee4d9dc1a805cb73102c450f31"
B2_METRICS_SHA256 = "11031e6b4c2c6b53db165c4730479153cf006b7f67c6ee4e7045f137cff79847"
B2_SCORECARD = ROOT / "docs/working-memory/2026-11-17_p16_b2/SAFE_B2_CANDIDATE_MILESTONE.json"
DEFAULT_DB = (
    ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
)
DEFAULT_B2 = ROOT / "data/local-acceptance/p16-stage-b2-2026-11-17/b2-candidate-acceptance-v5"
DEFAULT_OUT = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"
MAX_REQUESTS = 64
REQUEST_WALL_SECONDS = 900
RUN_WALL_SECONDS = 10_800
RESPONSE_SCHEMA_NAME = "jobhunter_translation_batch_v2"


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def json_sha(value: Any) -> str:
    return sha256_bytes(json_bytes(value))


def file_sha(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"JSONL record {number} is not an object")
            rows.append(value)
    return rows


def private_output_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    private_root = (ROOT / "data/local-acceptance").resolve()
    if not resolved.is_relative_to(private_root):
        raise ValueError("B3 output must stay under ignored data/local-acceptance/")
    return resolved


def copy_frozen_database(source: Path, destination: Path) -> None:
    uri = "file:" + str(source.resolve()) + "?mode=ro"
    with sqlite3.connect(uri, uri=True) as src, sqlite3.connect(destination) as dst:
        src.backup(dst)
        if dst.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Frozen B0 SQLite integrity check failed")
        if dst.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Frozen B0 SQLite foreign-key check failed")


def b1_helpers() -> tuple[Any, Any]:
    diagnostic = runpy.run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))
    validator = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))
    return diagnostic["b1_design_from_b2"], validator["validate_bundle"]


def build_contexts(
    database: Path, b2_dir: Path
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    candidate_path = b2_dir / "PRIVATE_B2_CANDIDATES.json"
    if file_sha(database) != B0_SHA256 or file_sha(candidate_path) != B2_CANDIDATE_SHA256:
        raise ValueError("Frozen B0/B2 source fingerprints changed")
    scorecard = json.loads(B2_SCORECARD.read_text(encoding="utf-8"))
    if scorecard["safe_diagnostic_metrics_sha256"] != B2_METRICS_SHA256:
        raise ValueError("B2 safe scorecard fingerprint changed")
    reconcile = runpy.run_path(str(ROOT / "scripts/reconcile_b2_candidate_milestone.py"))[
        "reconcile"
    ]
    if reconcile(database, b2_dir) != scorecard:
        raise ValueError("B2 private candidate output no longer reproduces its safe scorecard")

    b1_design, validate = b1_helpers()
    private = json.loads(candidate_path.read_text(encoding="utf-8"))
    contexts = {}
    with tempfile.TemporaryDirectory(prefix="jobhunter-b3-source-") as temporary:
        copied = Path(temporary) / "frozen.sqlite3"
        copy_frozen_database(database, copied)
        store = TranslationStore(copied)
        for job_id in COHORT:
            source = store.latest_source_version(job_id)
            if source is None:
                raise ValueError(f"Frozen source version missing for {job_id}")
            candidate = interpret_original_source_candidate(source)
            verify_b2_candidate(candidate, source)
            if (
                json.loads(json.dumps(dataclasses.asdict(candidate)))
                != private[job_id]["original_candidate"]
            ):
                raise ValueError(f"Reconstructed B2 candidate differs for {job_id}")
            draft = b1_design(candidate, source)
            validate(draft, source=source)
            item_ids = {
                item["source_ref"]["anchor_id"]: item["item_id"]
                for item in draft["items"]
                if item["source_ref"]["kind"] == "original_description_span"
            }
            selection = select_b3_items(job_id, candidate.items)
            logic = build_candidate_eligibility_logic(source, candidate)
            leaves = [leaf.anchor for graph in logic.graphs for leaf in graph.leaves]
            nested = nested_leaf_parent_relations(
                candidate_items=selection.translate_items,
                nested_leaf_anchors=leaves,
            )
            nested = [
                {
                    **relation,
                    "leaf_item_id": item_ids[relation["leaf_anchor_id"]],
                    "parent_item_id": item_ids[relation["parent_anchor_id"]],
                }
                for relation in nested
            ]
            contexts[job_id] = {
                "source": source,
                "candidate": candidate,
                "draft": draft,
                "item_ids": item_ids,
                "selection": selection,
                "nested": nested,
            }
    return scorecard, contexts


def build_manifest(
    database: Path,
    b2_dir: Path,
    settings: Settings,
    scorecard: dict[str, Any],
    contexts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    model = settings.effective_translation_lm_studio_model()
    endpoint = urlparse(settings.lm_studio_base_url)
    if settings.translation_provider != "lm-studio" or settings.translation_target_language != "en":
        raise ValueError("B3 requires the configured local LM Studio provider and English target")
    if model != "gemma-4-e2b-it" or endpoint.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("B3 provider/model must remain the predeclared local Gemma 4 E2B")

    selected, native, excluded, nested = [], [], [], []
    per_job, lengths = {}, []
    counts = {
        "source_item_count": 0,
        "translation_request_count": 0,
        "native_identity_count": 0,
        "context_excluded_count": 0,
        "generic_application_excluded_count": 0,
        "nested_eligibility_leaf_count": 0,
    }
    for job_id in COHORT:
        context = contexts[job_id]
        source, selection = context["source"], context["selection"]
        counts["source_item_count"] += len(context["candidate"].items)
        counts["translation_request_count"] += len(selection.translate_items)
        counts["native_identity_count"] += len(selection.native_identity_items)
        counts["context_excluded_count"] += sum(
            r == "context_only" for _, r in selection.excluded_items
        )
        counts["generic_application_excluded_count"] += sum(
            r == "generic_application_instruction" for _, r in selection.excluded_items
        )
        counts["nested_eligibility_leaf_count"] += len(context["nested"])
        job_lengths = []

        for item in selection.translate_items:
            anchor = item.anchor
            length = len(anchor.exact_text)
            lengths.append(length)
            job_lengths.append(length)
            selected.append(
                {
                    "source_job_id": job_id,
                    "source_item_id": context["item_ids"][anchor.anchor_id],
                    "source_anchor_id": anchor.anchor_id,
                    "source_semantic_sha256": source.semantic_sha256,
                    "source_field_sha256": anchor.field_sha256,
                    "source_span_sha256": anchor.text_sha256,
                    "source_char_start": anchor.char_start,
                    "source_char_end": anchor.char_end,
                    "source_char_count": length,
                    "source_category_candidate": item.category,
                    "source_strength_candidate": item.employer_strength,
                    "source_qualifier_candidate": item.qualifier,
                    "source_heading_context_sha256": sha256_text(item.heading)
                    if item.heading
                    else None,
                    "heading_context_in_prompt": False,
                    "input_kind": "exact_source_item_text_only",
                }
            )
        for item in selection.native_identity_items:
            anchor = item.anchor
            native.append(
                {
                    "source_job_id": job_id,
                    "source_item_id": context["item_ids"][anchor.anchor_id],
                    "source_anchor_id": anchor.anchor_id,
                    "source_span_sha256": anchor.text_sha256,
                    "source_char_start": anchor.char_start,
                    "source_char_end": anchor.char_end,
                    "input_kind": "native_english_exact_source_item",
                }
            )
        for item, reason in selection.excluded_items:
            anchor = item.anchor
            excluded.append(
                {
                    "source_job_id": job_id,
                    "source_item_id": context["item_ids"][anchor.anchor_id],
                    "source_anchor_id": anchor.anchor_id,
                    "source_span_sha256": anchor.text_sha256,
                    "reason": reason,
                }
            )
        nested.extend({"source_job_id": job_id, **relation} for relation in context["nested"])
        per_job[job_id] = {
            "source_item_count": len(context["candidate"].items),
            "translation_request_count": len(selection.translate_items),
            "native_identity_count": len(selection.native_identity_items),
            "excluded_count": len(selection.excluded_items),
            "nested_eligibility_leaf_count": len(context["nested"]),
            "max_source_item_characters": max(job_lengths, default=0),
        }

    expected = {
        "source_item_count": 78,
        "translation_request_count": 63,
        "native_identity_count": 1,
        "context_excluded_count": 12,
        "generic_application_excluded_count": 2,
        "nested_eligibility_leaf_count": 12,
    }
    if counts != expected or not lengths:
        raise ValueError(f"B3 frozen selection changed: {counts!r}")
    if max(lengths) > settings.translation_lm_studio_character_target:
        raise ValueError("A selected source item exceeds the configured character target")
    if counts["translation_request_count"] + counts["native_identity_count"] > 64:
        raise ValueError("B3 exceeds the frozen 64-item request ceiling")

    provider = {
        "name": "lm-studio-translation-v2",
        "base_url": settings.lm_studio_base_url,
        "model": model,
        "source_language": "fa",
        "target_language": "en",
        "timeout_seconds": settings.translation_timeout_seconds,
        "max_retries": settings.translation_max_retries,
        "max_tokens": settings.translation_lm_studio_max_tokens,
        "request_character_target": settings.translation_lm_studio_character_target,
        "api_token_configured": bool(settings.lm_studio_api_token),
        "system_prompt_sha256": sha256_text(_SYSTEM_PROMPT),
    }
    core = {
        "contract": B3_CONTRACT_VERSION,
        "selection_contract": B3_SELECTION_VERSION,
        "source_database_sha256": file_sha(database),
        "b2_private_candidate_sha256": file_sha(b2_dir / "PRIVATE_B2_CANDIDATES.json"),
        "b2_safe_scorecard_sha256": file_sha(B2_SCORECARD),
        "b2_code_fingerprints": {
            key: value
            for key, value in scorecard.items()
            if key.endswith("_code_sha256") or key == "schema_sha256"
        },
        "b3_code_fingerprints": {
            "runner_sha256": file_sha(ROOT / "scripts/run_p16_b3_source_bound_translation.py"),
            "support_module_sha256": file_sha(
                ROOT / "src/jobhunter/source_bound_translation_b3.py"
            ),
            "b1_schema_sha256": file_sha(
                ROOT / "docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json"
            ),
        },
        "provider": provider,
        "limits": {
            "max_source_bound_requests": MAX_REQUESTS,
            "request_wall_seconds": REQUEST_WALL_SECONDS,
            "run_wall_seconds": RUN_WALL_SECONDS,
            "corrective_candidate_count": 0,
            "heading_context_sent_to_model": False,
        },
        "counts": counts,
        "source_character_stats": {
            "minimum": min(lengths),
            "maximum": max(lengths),
            "mean": round(sum(lengths) / len(lengths), 2),
        },
        "per_job": per_job,
        "selected_items": selected,
        "native_identity_items": native,
        "excluded_items": excluded,
        "nested_leaf_relations": nested,
    }
    return {**core, "created_at": utc_now(), "plan_sha256": json_sha(core)}


def persist_events(
    output_dir: Path,
    folder: Path,
    events: list[Any],
) -> list[dict[str, Any]]:
    records = []
    for index, event in enumerate(events, 1):
        stem = f"http-{index:02d}"
        request_path = output_dir / folder / f"{stem}.request.json"
        request_path.parent.mkdir(parents=True, exist_ok=True)
        request_path.write_bytes(event.request_body)
        response_path = None
        if event.response_body is not None:
            response_path = request_path.with_name(f"{stem}.response.json")
            response_path.write_bytes(event.response_body)
        payload = None
        if event.response_body:
            with suppress(json.JSONDecodeError, UnicodeDecodeError):
                payload = json.loads(event.response_body)
        usage = payload.get("usage") if isinstance(payload, dict) else None
        finish = None
        response_model = payload.get("model") if isinstance(payload, dict) else None
        if isinstance(payload, dict):
            with suppress(KeyError, IndexError, TypeError):
                finish = payload["choices"][0].get("finish_reason")
        records.append(
            {
                "ordinal": index,
                "method": event.method,
                "url_path": event.url_path,
                "request_body_sha256": sha256_bytes(event.request_body),
                "response_status": event.response_status,
                "response_body_sha256": sha256_bytes(event.response_body)
                if event.response_body is not None
                else None,
                "error_type": event.error_type,
                "elapsed_seconds": round(event.elapsed_seconds, 4),
                "response_model": response_model,
                "finish_reason": finish,
                "usage": usage,
                "raw_request_file": str(request_path.relative_to(output_dir)),
                "raw_response_file": str(response_path.relative_to(output_dir))
                if response_path
                else None,
            }
        )
    return records


def request_with_deadline(call: Any) -> Any:
    previous = signal.getsignal(signal.SIGALRM)

    def timeout_handler(_signum: int, _frame: Any) -> None:
        raise TimeoutError("B3 per-item request wall ceiling reached")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, REQUEST_WALL_SECONDS)
    try:
        return call()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def failure_code(exc: Exception) -> str:
    message = str(exc).casefold()
    if isinstance(exc, TimeoutError):
        return "request_wall_timeout"
    if isinstance(exc, httpx.ConnectError) or "could not reach lm studio" in message:
        return "provider_unavailable"
    if "lm studio returned http" in message:
        return "provider_http_error"
    if any(word in message for word in ("json", "structured", "translation id")):
        return "invalid_structured_response"
    return "translation_error"


def response_schema_sha(event: Any) -> str | None:
    try:
        request = json.loads(event.request_body)
        schema = request["response_format"]["json_schema"]["schema"]
    except (KeyError, TypeError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    return json_sha(schema)


def checkpoint_state(events: list[dict[str, Any]]) -> dict[str, str]:
    state = {}
    for event in events:
        item_id = event.get("source_item_id")
        if not isinstance(item_id, str):
            continue
        if event.get("event") == "request_started":
            state[item_id] = "started"
        elif event.get("event") in {
            "request_completed",
            "request_failed",
            "request_interrupted_unknown",
        }:
            state[item_id] = str(event["event"])
    return state


def load_candidates(path: Path) -> dict[str, dict[str, Any]]:
    result = {}
    for record in read_jsonl(path):
        anchor_id = record.get("source_anchor_id")
        if not isinstance(anchor_id, str) or anchor_id in result:
            raise ValueError("B3 candidate JSONL has a missing or duplicate source anchor")
        result[anchor_id] = record
    return result


def candidate_base(job_id: str, source: Any, item: Any, item_id: str) -> dict[str, Any]:
    anchor = item.anchor
    return {
        "contract_version": B3_CONTRACT_VERSION,
        "source_job_id": job_id,
        "source_item_id": item_id,
        "source_anchor_id": anchor.anchor_id,
        "source_semantic_sha256": source.semantic_sha256,
        "source_field_sha256": anchor.field_sha256,
        "source_span_sha256": anchor.text_sha256,
        "source_char_start": anchor.char_start,
        "source_char_end": anchor.char_end,
        "source_category_candidate": item.category,
        "source_strength_candidate": item.employer_strength,
        "source_qualifier_candidate": item.qualifier,
        "source_heading_context": item.heading,
        "source_heading_context_sha256": sha256_text(item.heading) if item.heading else None,
        "heading_context_in_prompt": False,
        "input_kind": "exact_source_item_text_only",
        "target_language": "en",
        "meaning_review": "unreviewed",
    }


def verify_local_model(
    settings: Settings,
    expected_model: str,
    capture: CapturingHTTPTransport,
    output_dir: Path,
) -> list[dict[str, Any]]:
    headers = (
        {"Authorization": f"Bearer {settings.lm_studio_api_token}"}
        if settings.lm_studio_api_token
        else {}
    )
    start = len(capture.events)
    try:
        with httpx.Client(
            base_url=settings.lm_studio_base_url,
            headers=headers,
            timeout=10.0,
            trust_env=False,
            transport=capture,
        ) as client:
            response = client.get("models")
            response.raise_for_status()
            model_ids = {
                row.get("id") for row in response.json().get("data", []) if isinstance(row, dict)
            }
        if expected_model not in model_ids:
            raise ValueError("Predeclared B3 model is not available from local LM Studio")
    finally:
        records = persist_events(output_dir, Path("raw/preflight"), capture.events[start:])
        write_json(output_dir / "RAW_PREFLIGHT_INDEX.json", records)
    return records


def run_requests(
    *,
    output_dir: Path,
    contexts: dict[str, dict[str, Any]],
    provider: LMStudioTranslationProvider,
    capture: CapturingHTTPTransport,
    candidates: dict[str, dict[str, Any]],
    checkpoint_path: Path,
    candidate_path: Path,
    manifest: dict[str, Any],
) -> str:
    checkpoint = read_jsonl(checkpoint_path)
    states = checkpoint_state(checkpoint)
    started_count = sum(event.get("event") == "request_started" for event in checkpoint)
    run_started = time.monotonic()
    prompt_version = (
        "lm-studio-translation-v2-system-sha256:" + manifest["provider"]["system_prompt_sha256"]
    )
    stop_reason = None

    for job_id in COHORT:
        context = contexts[job_id]
        source = context["source"]
        for item in context["selection"].translate_items:
            anchor = item.anchor
            anchor_id = anchor.anchor_id
            item_id = context["item_ids"][anchor_id]
            state = states.get(item_id)

            if state in {"request_completed", "request_failed", "request_interrupted_unknown"}:
                if anchor_id not in candidates:
                    raise ValueError("Terminal B3 checkpoint has no candidate record")
                continue
            if state == "started" and anchor_id in candidates:
                record = candidates[anchor_id]
                terminal = (
                    "request_completed"
                    if record.get("state") == "source_bound_translation_candidate"
                    else "request_failed"
                )
                append_jsonl(
                    checkpoint_path,
                    {
                        "event": terminal,
                        "timestamp": utc_now(),
                        "source_job_id": job_id,
                        "source_item_id": item_id,
                        "source_anchor_id": anchor_id,
                        "source_span_sha256": anchor.text_sha256,
                        "target_sha256": record.get("target_sha256"),
                        "recovered_from_candidate_record": True,
                    },
                )
                states[item_id] = terminal
                continue
            if state == "started":
                record = candidate_base(job_id, source, item, item_id)
                record.update(
                    {
                        "state": "unresolved",
                        "target_text": None,
                        "target_sha256": None,
                        "target_char_start": None,
                        "target_char_end": None,
                        "provider_name": provider.name,
                        "provider_model": provider.model,
                        "prompt_version": prompt_version,
                        "model_request_count": 1,
                        "http_completion_attempt_count": 0,
                        "failure_code": "interrupted_unknown",
                        "review_flags": [],
                        "raw_http_events": [],
                    }
                )
                append_jsonl(candidate_path, record)
                candidates[anchor_id] = record
                append_jsonl(
                    checkpoint_path,
                    {
                        "event": "request_interrupted_unknown",
                        "timestamp": utc_now(),
                        "source_job_id": job_id,
                        "source_item_id": item_id,
                        "source_anchor_id": anchor_id,
                        "source_span_sha256": anchor.text_sha256,
                        "failure_code": "interrupted_unknown",
                    },
                )
                states[item_id] = "request_interrupted_unknown"
                continue

            if started_count >= MAX_REQUESTS:
                stop_reason = "source_bound_request_ceiling_reached"
                break
            if time.monotonic() - run_started >= RUN_WALL_SECONDS:
                stop_reason = "run_wall_ceiling_reached"
                break

            started_count += 1
            append_jsonl(
                checkpoint_path,
                {
                    "event": "request_started",
                    "timestamp": utc_now(),
                    "request_ordinal": started_count,
                    "source_job_id": job_id,
                    "source_item_id": item_id,
                    "source_anchor_id": anchor_id,
                    "source_semantic_sha256": source.semantic_sha256,
                    "source_span_sha256": anchor.text_sha256,
                    "provider_name": provider.name,
                    "provider_model": provider.model,
                    "prompt_version": prompt_version,
                    "request_wall_seconds": REQUEST_WALL_SECONDS,
                },
            )
            states[item_id] = "started"
            event_start = len(capture.events)
            item_started = time.monotonic()
            source_text = anchor.exact_text
            try:
                result = request_with_deadline(
                    lambda text=source_text: provider.translate_texts(
                        (text,), source_language="fa", target_language="en"
                    )
                )
                if len(result.texts) != 1:
                    raise ValueError("Translation provider returned wrong batch cardinality")
                target_text = result.texts[0].strip()
                events = capture.events[event_start:]
                http_events = persist_events(output_dir, Path("raw") / job_id / anchor_id, events)
                completion = [
                    event for event in events if event.url_path.endswith("/chat/completions")
                ]
                response_records = [
                    event
                    for event in http_events
                    if event["url_path"].endswith("/chat/completions")
                ]
                usage_rows = [
                    event["usage"]
                    for event in response_records
                    if isinstance(event.get("usage"), dict)
                ]
                english = bool(target_text) and not contains_persian(target_text)
                record = candidate_base(job_id, source, item, item_id)
                record.update(
                    {
                        "state": "source_bound_translation_candidate" if english else "unresolved",
                        "target_text": target_text or None,
                        "target_sha256": sha256_text(target_text) if target_text else None,
                        "target_char_start": 0 if target_text else None,
                        "target_char_end": len(target_text) if target_text else None,
                        "provider_name": provider.name,
                        "provider_model": provider.model,
                        "response_model": next(
                            (
                                event.get("response_model")
                                for event in reversed(response_records)
                                if event.get("response_model")
                            ),
                            None,
                        ),
                        "prompt_version": prompt_version,
                        "response_schema_name": RESPONSE_SCHEMA_NAME,
                        "response_schema_sha256": next(
                            (
                                response_schema_sha(event)
                                for event in reversed(events)
                                if event.url_path.endswith("/chat/completions")
                            ),
                            None,
                        ),
                        "request_body_sha256": next(
                            (event["request_body_sha256"] for event in reversed(response_records)),
                            None,
                        ),
                        "response_body_sha256": next(
                            (event["response_body_sha256"] for event in reversed(response_records)),
                            None,
                        ),
                        "raw_http_events": http_events,
                        "model_request_count": 1,
                        "http_completion_attempt_count": len(completion),
                        "transport_retry_count": sum(
                            (event.response_status is not None and event.response_status >= 500)
                            or event.error_type is not None
                            for event in completion
                        ),
                        "truncation_recovery_count": sum(
                            event.get("finish_reason") == "length" for event in response_records
                        ),
                        "elapsed_seconds": round(time.monotonic() - item_started, 4),
                        "usage": {
                            "prompt_tokens": sum(
                                row["prompt_tokens"]
                                for row in usage_rows
                                if isinstance(row.get("prompt_tokens"), int)
                            )
                            or None,
                            "completion_tokens": sum(
                                row["completion_tokens"]
                                for row in usage_rows
                                if isinstance(row.get("completion_tokens"), int)
                            )
                            or None,
                        },
                        "meaning_review": "unreviewed",
                        "review_flags": build_translation_review_flags(source_text, target_text)
                        if target_text
                        else [],
                        "failure_code": None if english else "persian_script_remains",
                    }
                )
                append_jsonl(candidate_path, record)
                candidates[anchor_id] = record
                terminal = "request_completed" if english else "request_failed"
                append_jsonl(
                    checkpoint_path,
                    {
                        "event": terminal,
                        "timestamp": utc_now(),
                        "source_job_id": job_id,
                        "source_item_id": item_id,
                        "source_anchor_id": anchor_id,
                        "source_span_sha256": anchor.text_sha256,
                        "target_sha256": record["target_sha256"],
                        "failure_code": record["failure_code"],
                        "elapsed_seconds": record["elapsed_seconds"],
                        "http_completion_attempt_count": record["http_completion_attempt_count"],
                        "transport_retry_count": record["transport_retry_count"],
                        "truncation_recovery_count": record["truncation_recovery_count"],
                        "http_events": http_events,
                    },
                )
                states[item_id] = terminal
                print(
                    f"B3 {started_count}/63 {job_id} {anchor_id[:12]} "
                    f"{record['state']} flags={len(record['review_flags'])}"
                )
            except Exception as exc:
                events = capture.events[event_start:]
                http_events = persist_events(output_dir, Path("raw") / job_id / anchor_id, events)
                completion = [
                    event for event in events if event.url_path.endswith("/chat/completions")
                ]
                code = failure_code(exc)
                record = candidate_base(job_id, source, item, item_id)
                record.update(
                    {
                        "state": "unresolved",
                        "target_text": None,
                        "target_sha256": None,
                        "target_char_start": None,
                        "target_char_end": None,
                        "provider_name": provider.name,
                        "provider_model": provider.model,
                        "prompt_version": prompt_version,
                        "model_request_count": 1,
                        "http_completion_attempt_count": len(completion),
                        "transport_retry_count": sum(
                            (event.response_status is not None and event.response_status >= 500)
                            or event.error_type is not None
                            for event in completion
                        ),
                        "elapsed_seconds": round(time.monotonic() - item_started, 4),
                        "failure_code": code,
                        "meaning_review": "unreviewed",
                        "review_flags": [],
                        "raw_http_events": http_events,
                    }
                )
                append_jsonl(candidate_path, record)
                candidates[anchor_id] = record
                append_jsonl(
                    checkpoint_path,
                    {
                        "event": "request_failed",
                        "timestamp": utc_now(),
                        "source_job_id": job_id,
                        "source_item_id": item_id,
                        "source_anchor_id": anchor_id,
                        "source_span_sha256": anchor.text_sha256,
                        "failure_code": code,
                        "elapsed_seconds": record["elapsed_seconds"],
                        "http_completion_attempt_count": record["http_completion_attempt_count"],
                        "transport_retry_count": record["transport_retry_count"],
                        "http_events": http_events,
                    },
                )
                states[item_id] = "request_failed"
                print(f"B3 {started_count}/63 {job_id} {anchor_id[:12]} FAILED {code}")
                if code in {"provider_unavailable", "provider_http_error", "request_wall_timeout"}:
                    stop_reason = code
                    break
        if stop_reason:
            break
    return stop_reason or "all_selected_items_processed"


def build_b1_drafts(
    contexts: dict[str, dict[str, Any]],
    candidates: dict[str, dict[str, Any]],
    validate: Any,
) -> dict[str, dict[str, Any]]:
    result = {}
    for job_id in COHORT:
        context = contexts[job_id]
        draft = json.loads(json.dumps(context["draft"]))
        alignments = []
        items = list(context["selection"].translate_items) + list(
            context["selection"].native_identity_items
        )
        for item in items:
            anchor_id = item.anchor.anchor_id
            record = candidates.get(anchor_id)
            item_id = context["item_ids"][anchor_id]
            if record and record.get("state") == "source_bound_translation_candidate":
                alignments.append(
                    make_b1_source_bound_alignment(
                        source_item_id=item_id,
                        target_text=record["target_text"],
                        provider_name=record["provider_name"],
                        provider_model=record["provider_model"],
                        prompt_version=record["prompt_version"],
                    )
                )
            else:
                alignments.append(make_b1_unresolved_alignment(item_id))
        alignments.extend(
            make_b1_unresolved_alignment(item["leaf_item_id"]) for item in context["nested"]
        )
        draft["alignments"] = alignments
        validate(draft, source=context["source"])
        result[job_id] = draft
    return result


def safe_metrics(
    output: Path,
    manifest: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    b1_drafts: dict[str, dict[str, Any]],
    checkpoint: list[dict[str, Any]],
    preflight: list[dict[str, Any]],
    status: str,
) -> dict[str, Any]:
    rows = list(candidates.values())
    translated = [row for row in rows if row.get("state") == "source_bound_translation_candidate"]
    native = [row for row in rows if row.get("state") == "native_identity"]
    unresolved = [row for row in rows if row.get("state") == "unresolved"]
    terminal = [
        event
        for event in checkpoint
        if event.get("event")
        in {"request_completed", "request_failed", "request_interrupted_unknown"}
    ]
    completion_attempts = sum(
        int(event.get("http_completion_attempt_count", 0)) for event in terminal
    )
    retries = sum(int(event.get("transport_retry_count", 0)) for event in terminal)
    truncations = sum(int(event.get("truncation_recovery_count", 0)) for event in terminal)
    prompt_tokens = [
        row["usage"]["prompt_tokens"]
        for row in rows
        if isinstance(row.get("usage"), dict) and isinstance(row["usage"].get("prompt_tokens"), int)
    ]
    completion_tokens = [
        row["usage"]["completion_tokens"]
        for row in rows
        if isinstance(row.get("usage"), dict)
        and isinstance(row["usage"].get("completion_tokens"), int)
    ]
    per_job = {}
    for job_id in COHORT:
        job_rows = [row for row in rows if row["source_job_id"] == job_id]
        per_job[job_id] = {
            "candidate_records": len(job_rows),
            "translated_candidates": sum(
                row.get("state") == "source_bound_translation_candidate" for row in job_rows
            ),
            "native_identity": sum(row.get("state") == "native_identity" for row in job_rows),
            "unresolved": sum(row.get("state") == "unresolved" for row in job_rows),
        }
    return {
        "contract": "jobhunter-p16-b3-safe-metrics-v1",
        "run_status": status,
        "candidate_authority": "candidate_only_no_downstream_reuse",
        "meaning_review_state": "unreviewed_except_separately_recorded_diagnostic_reviews",
        "source_database_sha256": manifest["source_database_sha256"],
        "b2_private_candidate_sha256": manifest["b2_private_candidate_sha256"],
        "run_manifest_sha256": file_sha(output / "run_manifest.json"),
        "private_candidate_output_sha256": file_sha(output / "PRIVATE_B3_CANDIDATES.json"),
        "b1_compatible_drafts_sha256": file_sha(output / "B1_COMPATIBLE_DRAFTS.json"),
        "checkpoint_sha256": file_sha(output / "checkpoint.jsonl"),
        "raw_capture_index_sha256": file_sha(output / "RAW_CAPTURE_INDEX.json"),
        "provider": manifest["provider"],
        "limits": manifest["limits"],
        "aggregate": {
            **manifest["counts"],
            "candidate_record_count": len(rows),
            "translated_candidate_count": len(translated),
            "native_identity_count": len(native),
            "unresolved_count": len(unresolved),
            "logical_source_bound_requests_started": sum(
                event.get("event") == "request_started" for event in checkpoint
            ),
            "logical_source_bound_requests_terminal": len(terminal),
            "http_completion_attempt_count": completion_attempts,
            "transport_retry_count": retries,
            "truncation_recovery_count": truncations,
            "preflight_http_request_count": len(preflight),
            "prompt_tokens": sum(prompt_tokens) if prompt_tokens else None,
            "completion_tokens": sum(completion_tokens) if completion_tokens else None,
            "corrective_candidate_count": 0,
        },
        "per_job": per_job,
        "b1_bundle_validation": {job_id: "PASS" for job_id in b1_drafts},
        "privacy": {
            "raw_source_and_model_request_response_retained_only_under_"
            "ignored_local_acceptance": True,
            "safe_metrics_contains_raw_source_or_translation_text": False,
            "authorization_headers_persisted": False,
            "production_database_written": False,
            "accepted_facts_promoted": 0,
            "public_route_changed": False,
        },
        "limitations": [
            "Four source ads are exposed development cases, not a holdout.",
            "Exact source anchors prove provenance, not semantic translation correctness.",
            "Candidate translations remain unreviewed unless separately reviewed.",
            "Native identity is in the B3 sidecar; no B1 v2-native artifact is fabricated.",
            "Twelve nested eligibility leaves have no separate target subspan offsets.",
            "No B3 candidate gains accepted-fact or downstream authority.",
        ],
    }


def run(args: argparse.Namespace) -> int:
    database = Path(args.database).resolve()
    b2_dir = Path(args.private_b2_dir).resolve()
    output = private_output_path(Path(args.out_dir))
    if args.plan_only and args.resume:
        raise ValueError("--plan-only and --resume cannot be combined")
    if not database.is_file() or not (b2_dir / "PRIVATE_B2_CANDIDATES.json").is_file():
        raise ValueError("Frozen B0/B2 input is missing")

    database_before = file_sha(database)
    b2_before = file_sha(b2_dir / "PRIVATE_B2_CANDIDATES.json")
    settings = Settings.load(args.config)
    scorecard, contexts = build_contexts(database, b2_dir)
    manifest = build_manifest(database, b2_dir, settings, scorecard, contexts)
    manifest_path = output / "run_manifest.json"

    if output.exists():
        if not args.resume or not manifest_path.is_file():
            raise ValueError("B3 output exists; use --resume with its original manifest")
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing.get("plan_sha256") != manifest["plan_sha256"]:
            raise ValueError("B3 resume rejected: source, selection or provider plan changed")
    else:
        output.mkdir(parents=True)
        (output / "raw").mkdir()
        (output / "checkpoint.jsonl").write_text("", encoding="utf-8")
        (output / "candidates.jsonl").write_text("", encoding="utf-8")
        write_json(manifest_path, manifest)

    if args.plan_only:
        _, validate = b1_helpers()
        plan_drafts = build_b1_drafts(contexts, {}, validate)
        write_json(
            output / "SAFE_B3_METRICS.json",
            {
                "contract": "jobhunter-p16-b3-safe-metrics-v1",
                "run_status": "planned_no_model_requests",
                "source_database_sha256": manifest["source_database_sha256"],
                "b2_private_candidate_sha256": manifest["b2_private_candidate_sha256"],
                "run_manifest_sha256": file_sha(manifest_path),
                "provider": manifest["provider"],
                "limits": manifest["limits"],
                "aggregate": manifest["counts"],
                "source_character_stats": manifest["source_character_stats"],
                "per_job": manifest["per_job"],
                "b1_bundle_validation": {job_id: "PASS" for job_id in plan_drafts},
                "privacy": {
                    "raw_source_or_model_text_written": False,
                    "production_database_written": False,
                    "accepted_facts_promoted": 0,
                    "public_route_changed": False,
                },
            },
        )
        print(
            json.dumps(
                {
                    "run_status": "planned_no_model_requests",
                    "counts": manifest["counts"],
                    "source_character_stats": manifest["source_character_stats"],
                }
            )
        )
        return 0

    checkpoint_path = output / "checkpoint.jsonl"
    candidate_path = output / "candidates.jsonl"
    checkpoint = read_jsonl(checkpoint_path)
    candidates = load_candidates(candidate_path)
    for job_id in COHORT:
        context = contexts[job_id]
        for item in context["selection"].native_identity_items:
            anchor_id = item.anchor.anchor_id
            if anchor_id not in candidates:
                record = make_native_identity_record(
                    source_job_id=job_id,
                    source_item_id=context["item_ids"][anchor_id],
                    item=item,
                )
                append_jsonl(candidate_path, record)
                candidates[anchor_id] = record
                append_jsonl(
                    checkpoint_path,
                    {
                        "event": "native_identity_recorded",
                        "timestamp": utc_now(),
                        "source_job_id": job_id,
                        "source_item_id": record["source_item_id"],
                        "source_anchor_id": anchor_id,
                        "source_span_sha256": item.anchor.text_sha256,
                        "target_sha256": record["target_sha256"],
                        "model_request_count": 0,
                    },
                )

    capture = CapturingHTTPTransport()
    preflight_records = []
    status = "partial"
    try:
        preflight_records = verify_local_model(
            settings,
            manifest["provider"]["model"],
            capture,
            output,
        )
        provider = LMStudioTranslationProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=settings.effective_translation_lm_studio_model(),
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.translation_timeout_seconds,
            max_retries=settings.translation_max_retries,
            max_tokens=settings.translation_lm_studio_max_tokens,
            request_character_target=settings.translation_lm_studio_character_target,
            transport=capture,
        )
        if provider.model != manifest["provider"]["model"]:
            raise ValueError("Configured provider model differs from frozen B3 plan")
        stop_reason = run_requests(
            output_dir=output,
            contexts=contexts,
            provider=provider,
            capture=capture,
            candidates=candidates,
            checkpoint_path=checkpoint_path,
            candidate_path=candidate_path,
            manifest=manifest,
        )
        checkpoint = read_jsonl(checkpoint_path)
        candidates = load_candidates(candidate_path)
        terminal = sum(
            event.get("event")
            in {"request_completed", "request_failed", "request_interrupted_unknown"}
            for event in checkpoint
        )
        unresolved = sum(record.get("state") == "unresolved" for record in candidates.values())
        status = (
            "completed"
            if terminal == 63 and unresolved == 0
            else "completed_with_unresolved_items"
            if terminal == 63
            else "partial"
        )
        if stop_reason not in {"all_selected_items_processed", None} and terminal < 63:
            status = "partial"
    except Exception as exc:
        index = output / "RAW_PREFLIGHT_INDEX.json"
        if not preflight_records and index.is_file():
            preflight_records = json.loads(index.read_text(encoding="utf-8"))
        status = "preflight_failed" if not preflight_records else "partial_runner_error"
        write_json(
            output / "RUN_FAILURE.json",
            {
                "failure_type": type(exc).__name__,
                "failure_code": failure_code(exc),
                "timestamp": utc_now(),
            },
        )
        print(f"B3 stopped: {type(exc).__name__} ({failure_code(exc)})")
    finally:
        capture.close_inner()

    checkpoint = read_jsonl(checkpoint_path)
    candidates = load_candidates(candidate_path)
    _, validate = b1_helpers()
    b1_drafts = build_b1_drafts(contexts, candidates, validate)

    private_output = {
        "contract": B3_CONTRACT_VERSION,
        "authority": "candidate_only_no_downstream_reuse",
        "run_plan_sha256": manifest["plan_sha256"],
        "source_database_sha256": manifest["source_database_sha256"],
        "b2_private_candidate_sha256": manifest["b2_private_candidate_sha256"],
        "provider": manifest["provider"],
        "items": list(candidates.values()),
        "nested_leaf_relations": manifest["nested_leaf_relations"],
        "excluded_items": manifest["excluded_items"],
        "semantic_review_authority": "unreviewed_unless_separate_diagnostic_event",
    }
    write_json(output / "PRIVATE_B3_CANDIDATES.json", private_output)
    write_json(output / "B1_COMPATIBLE_DRAFTS.json", b1_drafts)
    raw_index = {
        "contract": "jobhunter-p16-b3-private-raw-capture-index-v1",
        "authorization_headers_persisted": False,
        "preflight_events": preflight_records,
        "request_events": [event for item in checkpoint for event in item.get("http_events", [])],
    }
    write_json(output / "RAW_CAPTURE_INDEX.json", raw_index)
    metrics = safe_metrics(
        output, manifest, candidates, b1_drafts, checkpoint, preflight_records, status
    )
    write_json(output / "SAFE_B3_METRICS.json", metrics)

    if file_sha(database) != database_before or database_before != B0_SHA256:
        raise ValueError("Frozen B0 source database changed during B3")
    if file_sha(b2_dir / "PRIVATE_B2_CANDIDATES.json") != b2_before:
        raise ValueError("Private B2 candidate input changed during B3")

    print(
        json.dumps(
            {
                "run_status": status,
                "aggregate": metrics["aggregate"],
                "per_job": metrics["per_job"],
                "safe_metrics_sha256": file_sha(output / "SAFE_B3_METRICS.json"),
            },
            sort_keys=True,
        )
    )
    return 0 if status in {"completed", "completed_with_unresolved_items"} else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/local.toml")
    parser.add_argument("--database", default=str(DEFAULT_DB))
    parser.add_argument("--private-b2-dir", default=str(DEFAULT_B2))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
