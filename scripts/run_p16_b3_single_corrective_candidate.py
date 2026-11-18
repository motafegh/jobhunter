#!/usr/bin/env python3
"""Run the single evidence-justified B3 corrective candidate (request 64/64)."""

from __future__ import annotations

import hashlib
import json
import os
import signal
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

from jobhunter.config import Settings
from jobhunter.source_bound_translation_b3 import CapturingHTTPTransport, sha256_bytes
from jobhunter.translation.projection import contains_persian

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/local-acceptance/p16-stage-b3-2026-11-18/primary-v1"
JOB = "tMjm"
ANCHOR = "beeca48335d4bd92df06c563ff3593278b8c72c2960583169a7a6d0ec2be8062"
ITEM_ID = "s_beeca48335d4bd92df06c563ff3593278b8c72c2"
NOTE = (
    "This source segment is a list of personal traits. In this context, the Persian "
    "compound وظیفه‌شناس means conscientious or dutiful, and مسئولیت‌پذیر means "
    "responsible. Translate the complete list naturally and preserve every trait. "
    "Do not render either compound literally as a noun such as 'duty identifier' "
    "or 'responsibility acceptance'."
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def main() -> None:
    corrective_path = OUT / "B3_CORRECTIVE_CANDIDATE.json"
    if corrective_path.exists():
        raise SystemExit("A B3 corrective candidate already exists; refusing a second correction.")

    manifest = json.loads((OUT / "run_manifest.json").read_text(encoding="utf-8"))
    private = json.loads((OUT / "PRIVATE_B3_CANDIDATES.json").read_text(encoding="utf-8"))
    primary = next(
        row
        for row in private["items"]
        if row["source_job_id"] == JOB and row["source_anchor_id"] == ANCHOR
    )
    if primary["state"] != "source_bound_translation_candidate":
        raise ValueError("Expected primary source-bound candidate is missing")
    if "duty identifier" not in primary["target_text"].casefold():
        raise ValueError("Primary translation no longer matches the diagnosed material error")

    checkpoint_path = OUT / "checkpoint.jsonl"
    checkpoint = [
        json.loads(line)
        for line in checkpoint_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    primary_started = sum(row.get("event") == "request_started" for row in checkpoint)
    primary_terminal = sum(
        row.get("event") in {"request_completed", "request_failed", "request_interrupted_unknown"}
        for row in checkpoint
    )
    if primary_started != 63 or primary_terminal != 63:
        raise ValueError("Corrective request requires all 63 primary requests to be terminal")
    if primary_started + 1 > manifest["limits"]["max_source_bound_requests"]:
        raise ValueError("Corrective request would exceed the frozen 64-request ceiling")

    event = primary["raw_http_events"][-1]
    original_request = json.loads((OUT / event["raw_request_file"]).read_text(encoding="utf-8"))
    messages = original_request["messages"]
    user_payload = json.loads(messages[1]["content"])
    source_text = user_payload["items"][0]["text"]
    if sha256_bytes(source_text.encode("utf-8")) != primary["source_span_sha256"]:
        raise ValueError("Primary request source text hash does not match the frozen anchor")
    user_payload["correction_note"] = NOTE
    request_body = {
        **original_request,
        "messages": [
            messages[0],
            {
                "role": "user",
                "content": json.dumps(user_payload, ensure_ascii=False, separators=(",", ":")),
            },
        ],
    }

    settings = Settings.load("config/local.toml")
    if settings.effective_translation_lm_studio_model() != "gemma-4-e2b-it":
        raise ValueError("Corrective model differs from frozen B3 provider")
    capture = CapturingHTTPTransport()
    headers = (
        {"Authorization": f"Bearer {settings.lm_studio_api_token}"}
        if settings.lm_studio_api_token
        else {}
    )
    start = time.monotonic()
    try:
        with httpx.Client(
            base_url=settings.lm_studio_base_url,
            headers=headers,
            timeout=900.0,
            trust_env=False,
            transport=capture,
        ) as client:
            models = client.get("models")
            models.raise_for_status()
            ids = {row.get("id") for row in models.json().get("data", []) if isinstance(row, dict)}
            if "gemma-4-e2b-it" not in ids:
                raise ValueError("Corrective model is not available on local LM Studio")
            preflight_events = capture.events[:]
            request_start = len(capture.events)
            append_jsonl(
                checkpoint_path,
                {
                    "event": "corrective_request_started",
                    "timestamp": utc_now(),
                    "request_ordinal": 64,
                    "source_job_id": JOB,
                    "source_item_id": ITEM_ID,
                    "source_anchor_id": ANCHOR,
                    "source_span_sha256": primary["source_span_sha256"],
                    "reason": "material_personal_trait_mistranslation",
                    "corrective_candidate_ordinal": 1,
                },
            )

            previous = signal.getsignal(signal.SIGALRM)

            def alarm(_signum: int, _frame: object) -> None:
                raise TimeoutError("Corrective request exceeded 900-second wall ceiling")

            signal.signal(signal.SIGALRM, alarm)
            signal.setitimer(signal.ITIMER_REAL, 900)
            try:
                response = client.post("chat/completions", json=request_body)
                response.raise_for_status()
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, previous)
            elapsed = time.monotonic() - start
            payload = response.json()
            message = json.loads(payload["choices"][0]["message"]["content"])
            translations = message["translations"]
            if len(translations) != 1 or translations[0]["id"] != user_payload["items"][0]["id"]:
                raise ValueError("Corrective response ID/cardinality mismatch")
            target = translations[0]["translation"].strip()
            if not target or contains_persian(target):
                raise ValueError("Corrective output is empty or still contains Persian")
            request_events = capture.events[request_start:]
            raw_dir = OUT / "raw/corrective" / JOB / ANCHOR
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_records = []
            for index, http_event in enumerate(request_events, 1):
                request_path = raw_dir / f"http-{index:02d}.request.json"
                response_path = raw_dir / f"http-{index:02d}.response.json"
                request_path.write_bytes(http_event.request_body)
                if http_event.response_body is not None:
                    response_path.write_bytes(http_event.response_body)
                raw_records.append(
                    {
                        "method": http_event.method,
                        "url_path": http_event.url_path,
                        "request_body_sha256": sha256_bytes(http_event.request_body),
                        "response_status": http_event.response_status,
                        "response_body_sha256": (
                            sha256_bytes(http_event.response_body)
                            if http_event.response_body is not None
                            else None
                        ),
                        "elapsed_seconds": round(http_event.elapsed_seconds, 4),
                        "raw_request_file": str(request_path.relative_to(OUT)),
                        "raw_response_file": str(response_path.relative_to(OUT)),
                    }
                )
            usage = payload.get("usage", {})
            candidate = {
                "contract": "jobhunter-p16-b3-corrective-candidate-v1",
                "candidate_kind": "single_corrective_translation_candidate",
                "source_job_id": JOB,
                "source_item_id": ITEM_ID,
                "source_anchor_id": ANCHOR,
                "source_span_sha256": primary["source_span_sha256"],
                "source_char_start": primary["source_char_start"],
                "source_char_end": primary["source_char_end"],
                "primary_target_text": primary["target_text"],
                "primary_target_sha256": primary["target_sha256"],
                "correction_reason": (
                    "Primary translation rendered وظیفه‌شناس as 'duty identifier' and "
                    "مسئولیت‌پذیر as 'responsibility acceptance'."
                ),
                "correction_note": NOTE,
                "corrective_prompt_sha256": sha256_bytes(
                    request_body["messages"][1]["content"].encode("utf-8")
                ),
                "system_prompt_sha256": manifest["provider"]["system_prompt_sha256"],
                "provider_name": "lm-studio-translation-v2",
                "provider_model": "gemma-4-e2b-it",
                "response_model": payload.get("model"),
                "temperature": request_body["temperature"],
                "seed": request_body["seed"],
                "state": "source_bound_translation_corrective_candidate",
                "target_language": "en",
                "target_text": target,
                "target_sha256": sha256_bytes(target.encode("utf-8")),
                "target_char_start": 0,
                "target_char_end": len(target),
                "meaning_review": "pending_separate_review",
                "request_count": 1,
                "http_completion_attempt_count": len(request_events),
                "elapsed_seconds": round(elapsed, 4),
                "usage": usage,
                "finish_reason": payload["choices"][0].get("finish_reason"),
                "request_body_sha256": sha256_bytes(request_events[-1].request_body),
                "response_body_sha256": sha256_bytes(request_events[-1].response_body),
                "raw_http_events": raw_records,
                "preflight_model_ids": sorted(ids),
                "preflight_http_request_count": len(preflight_events),
            }
            write_json(corrective_path, candidate)
            append_jsonl(
                checkpoint_path,
                {
                    "event": "corrective_request_completed",
                    "timestamp": utc_now(),
                    "request_ordinal": 64,
                    "source_job_id": JOB,
                    "source_item_id": ITEM_ID,
                    "source_anchor_id": ANCHOR,
                    "source_span_sha256": primary["source_span_sha256"],
                    "corrective_target_sha256": candidate["target_sha256"],
                    "http_completion_attempt_count": candidate["http_completion_attempt_count"],
                    "elapsed_seconds": candidate["elapsed_seconds"],
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                },
            )
            print(
                json.dumps(
                    {
                        "status": "corrective_candidate_created",
                        "source_item_id": ITEM_ID,
                        "corrective_target_sha256": candidate["target_sha256"],
                        "corrective_target_characters": len(target),
                        "finish_reason": candidate["finish_reason"],
                        "elapsed_seconds": candidate["elapsed_seconds"],
                        "usage": usage,
                        "raw_http_events": len(raw_records),
                    },
                    sort_keys=True,
                )
            )
    finally:
        capture.close_inner()


if __name__ == "__main__":
    main()
