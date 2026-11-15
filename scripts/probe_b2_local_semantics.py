"""Bounded original-context B2 local-LLM probe; exposed cases only.

Run from repo root with an already-running LM Studio server:
  python scripts/probe_b2_local_semantics.py --database data/local-acceptance/\
p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3 \
--out data/local-acceptance/p16-stage-b2-2026-11-15/local-semantic-probe

Uses NO proxy and sends only to the fixed loopback endpoint. No cloud fallback,
prompt retry, per-job tweaks, artifact promotion or public raw outputs.
Four frozen, previously exposed descriptions are read from a private DB copy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from jobhunter.translation_store import TranslationStore

PROBE_CONTRACT = "jobhunter-b2-minimal-original-context-probe-v1"
MODEL = "gemma-4-e4b-it-ud"
ENDPOINT = "http://127.0.0.1:18080"
JOBS = ("tNhZ", "tMps", "tNDx", "tMjm")
MAX_TOKENS = 760
TIMEOUT_SECONDS = 95
PROMPT = (
    "Analyze the whole original Persian job ad. Return one compact JSON object in "
    "English with arrays named duties, requirements, preferences, alternatives, "
    "arrangements, uncertainties, and work_implied_capabilities. Distinguish "
    "what the employer explicitly requires from relevant ability implied by "
    "assigned work. Do not invent experience requirements or named technologies. "
    "Preserve OR alternatives; leave unclear obligations uncertain."
)


def _sha(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def _json_array_counts(content: str) -> dict[str, Any]:
    candidate = content.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1])
    try:
        parsed = json.loads(candidate)
    except (ValueError, TypeError):
        return {"is_json": False, "valid_top_level": False, "field_lengths": {}}
    keys = (
        "duties",
        "requirements",
        "preferences",
        "alternatives",
        "arrangements",
        "uncertainties",
        "work_implied_capabilities",
    )
    return {
        "is_json": True,
        "valid_top_level": isinstance(parsed, dict),
        "field_lengths": {
            key: len(parsed[key])
            for key in keys
            if isinstance(parsed, dict) and isinstance(parsed.get(key), list)
        },
        "missing_fields": [
            key for key in keys if not isinstance(parsed, dict) or key not in parsed
        ],
    }


def _client() -> urllib.request.OpenerDirector:
    # Remote WSL may configure an HTTP proxy that intercepts localhost.
    # Disable it for the loopback-only LM Studio session.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _post(opener: urllib.request.OpenerDirector, body: dict) -> dict:
    request = urllib.request.Request(
        ENDPOINT + "/v1/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    allowed = root / "data/local-acceptance"
    if not (root / "AGENTS.md").exists():
        raise ValueError("Run from JobHunter repository root")
    if not args.out.resolve().is_relative_to(allowed) or args.out.exists():
        raise ValueError("Private output must be new and inside ignored local data")
    if not args.database.is_file():
        raise ValueError("Explicit frozen input database missing")
    opener = _client()
    with opener.open(ENDPOINT + "/v1/models", timeout=4) as resp:
        available = {m["id"] for m in json.load(resp)["data"]}
    if MODEL not in available:
        raise ValueError("Required local model not exposed by LM Studio")
    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-model-") as temp:
        temp_path = Path(temp) / "snapshot.sqlite3"
        uri = "file:" + str(args.database.resolve()) + "?mode=ro"
        with sqlite3.connect(uri, uri=True) as read, sqlite3.connect(temp_path) as write:
            read.backup(write)
            if write.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Frozen original source database integrity failed")
            if write.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Frozen original source database foreign keys failed")
        store = TranslationStore(temp_path)
        frozen = []
        for job in JOBS:
            src = store.latest_source_version(job)
            if src is None or not isinstance(src.fields.get("description"), str):
                raise ValueError(f"Missing original employer source for {job}")
            frozen.append((job, src))
    args.out.mkdir(parents=True)
    run = {
        "contract": PROBE_CONTRACT,
        "state": "candidate_only_no_downstream_reuse",
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "max_tokens": MAX_TOKENS,
        "timeout_seconds_per_case": TIMEOUT_SECONDS,
        "system_prompt": PROMPT,
        "prompt_sha256": _sha(PROMPT),
        "database_sha256": _sha(args.database.read_bytes()),
        "cases": {},
    }
    # One fixed prompt/configuration; no response-conditioned retry or changes.
    for job, src in frozen:
        msg = {
            "model": MODEL,
            "temperature": 0,
            "max_tokens": MAX_TOKENS,
            "stream": False,
            "messages": [
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": src.fields["description"]},
            ],
        }
        start = time.perf_counter()
        record: dict[str, Any] = {
            "source_semantic_sha256": src.semantic_sha256,
            "source_version_id": src.job_detail_version_id,
            "source_description_sha256": _sha(src.fields["description"]),
            "request_sha256": _sha(json.dumps(msg, sort_keys=True, ensure_ascii=False)),
        }
        try:
            response = _post(opener, msg)
            elapsed = round(time.perf_counter() - start, 2)
            choices = response.get("choices") or []
            choice = choices[0] if choices else {}
            content = choice.get("message", {}).get("content") or ""
            record.update(
                {
                    "outcome": "response",
                    "elapsed_seconds": elapsed,
                    "returned_model": response.get("model"),
                    "finish_reason": choice.get("finish_reason"),
                    "raw_content": content,
                    "raw_content_sha256": _sha(content),
                    "response_usage": response.get("usage"),
                    "structure": _json_array_counts(content),
                }
            )
        except (TimeoutError, OSError, ValueError, urllib.error.HTTPError) as err:
            record.update(
                {
                    "outcome": "failed",
                    "elapsed_seconds": round(time.perf_counter() - start, 2),
                    "error_type": type(err).__name__,
                    "error_message": str(err)[:250],
                }
            )
        run["cases"][job] = record
        (args.out / "PRIVATE_MODEL_TRIAL.json").write_text(
            json.dumps(run, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        print(
            job,
            record["outcome"],
            f"{record['elapsed_seconds']:.1f}s",
            record.get("finish_reason") or record.get("error_type"),
            flush=True,
        )
        # Preserve a failed-attempt record and stop; repeated identical slow
        # calls cannot establish a meaningful performance comparison.
        if record["outcome"] != "response":
            break
    report = {
        "contract": PROBE_CONTRACT,
        "model": MODEL,
        "model_result_not_independent_semantic_review": True,
        "prompt_sha256": run["prompt_sha256"],
        "source_database_sha256": run["database_sha256"],
        "source_jobs": JOBS,
        "model_calls_attempted": len(run["cases"]),
        "planned_job_count": len(JOBS),
        "batch_incomplete_after_failure": len(run["cases"]) != len(JOBS),
        "production_writes": 0,
        "candidate_only": True,
        "cases": {
            j: {
                k: v
                for k, v in rec.items()
                if k
                in (
                    "source_semantic_sha256",
                    "outcome",
                    "elapsed_seconds",
                    "finish_reason",
                    "raw_content_sha256",
                    "structure",
                    "error_type",
                )
            }
            for j, rec in run["cases"].items()
        },
    }
    (args.out / "SAFE_MODEL_PROBE_SUMMARY.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print("MODEL_PROBE_FINISHED", len(run["cases"]), flush=True)


if __name__ == "__main__":
    main()
