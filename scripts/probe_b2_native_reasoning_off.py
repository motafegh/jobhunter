"""Versioned B2 original-source trial using LM Studio's native reasoning-off API.

Keeps the v1 seven-array prompt and the same four frozen exposed job versions.
Changes only transport, explicit reasoning control and output token budget.
Private raw responses stay in ignored local data. No production persistence.

From repo root:
python scripts/probe_b2_native_reasoning_off.py \
  --database path/to/frozen-B0.sqlite3 \
  --out data/local-acceptance/p16-stage-b2-2026-11-16/native-reasoning-off-v2
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

from probe_b2_local_semantics import JOBS, MODEL, PROMPT, _json_array_counts, _sha

from jobhunter.translation_store import TranslationStore

CONTRACT = "jobhunter-b2-original-context-native-reasoning-off-v2"
BASE = "http://127.0.0.1:18080"
MAX_OUTPUT_TOKENS = 1400
TIMEOUT_SECONDS = 40
EXPECTED_B0_SHA256 = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"


def _post(client: urllib.request.OpenerDirector, body: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        BASE + "/api/v1/chat",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with client.open(request, timeout=TIMEOUT_SECONDS) as response:
        result: dict[str, Any] = json.load(response)
    return result


def _answer_parts(result: dict[str, Any]) -> tuple[str, int]:
    output = result.get("output")
    if not isinstance(output, list):
        return "", 0
    messages = [
        x.get("content") for x in output if isinstance(x, dict) and x.get("type") == "message"
    ]
    return "\n".join(x for x in messages if isinstance(x, str)), len(messages)


def _request_for_job(*, prompt: str, description: str) -> dict[str, Any]:
    """Fixed reasoning-off, no-stored-chat request; no per-job prompt changes."""
    return {
        "model": MODEL,
        "system_prompt": prompt,
        "input": description,
        "temperature": 0,
        "reasoning": "off",
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "stream": False,
        "store": False,
    }


def run_trial(
    database: Path, out: Path, *, prompt: str = PROMPT, contract: str = CONTRACT
) -> dict[str, Any]:
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter repository root")
    if not out.resolve().is_relative_to(root / "data/local-acceptance"):
        raise ValueError("Private output must be inside ignored local data")
    if out.exists():
        raise FileExistsError("Trial evidence must not overwrite an existing run")
    if not database.is_file():
        raise FileNotFoundError("Frozen source database unavailable")
    db_sha256 = hashlib.sha256(database.read_bytes()).hexdigest()
    if db_sha256 != EXPECTED_B0_SHA256:
        raise ValueError("B0 database differs from frozen evaluation version")
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with client.open(BASE + "/api/v1/models", timeout=5) as response:
        models = json.load(response).get("models", [])
    selected = [m for m in models if m.get("key") == MODEL]
    if len(selected) != 1:
        raise ValueError("Requested local Gemma model not available")
    m = selected[0]
    reasoning = m.get("capabilities", {}).get("reasoning", {})
    if "off" not in reasoning.get("allowed_options", []):
        raise ValueError("Model does not explicitly support reasoning-off")
    if not m.get("loaded_instances"):
        raise ValueError("Model is not loaded; load/validate separately before trial")

    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-native-") as tmp:
        target = Path(tmp) / "copied.sqlite3"
        uri = database.resolve().as_uri() + "?mode=ro"
        with (
            sqlite3.connect(uri, uri=True) as readonly,
            sqlite3.connect(target) as copied,
        ):
            readonly.backup(copied)
            if copied.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Frozen diagnostic copy failed SQLite integrity")
            if copied.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Frozen diagnostic copy failed foreign keys")
        store = TranslationStore(target)
        frozen = []
        for jid in JOBS:
            source = store.latest_source_version(jid)
            if source is None or not isinstance(source.fields.get("description"), str):
                raise ValueError(f"Original employer description missing: {jid}")
            frozen.append((jid, source))

    out.mkdir(parents=True)
    record: dict[str, Any] = {
        "contract": contract,
        "authority": "research_only_no_downstream_reuse",
        "model": MODEL,
        "transport": "LM Studio local native /api/v1/chat",
        "reasoning": "off",
        "model_declared_reasoning": reasoning,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "temperature": 0,
        "system_prompt": prompt,
        "prompt_sha256": _sha(prompt),
        "source_database_sha256": db_sha256,
        "cases": {},
        "stopped_early": False,
    }
    for jid, source in frozen:
        body = _request_for_job(prompt=prompt, description=source.fields["description"])
        start = time.perf_counter()
        case: dict[str, Any] = {
            "source_job_id": jid,
            "source_semantic_sha256": source.semantic_sha256,
            "source_description_sha256": _sha(source.fields["description"]),
            "request_sha256": _sha(json.dumps(body, sort_keys=True, ensure_ascii=False)),
        }
        try:
            result = _post(client, body)
            elapsed = round(time.perf_counter() - start, 3)
            answer, message_count = _answer_parts(result)
            case.update(
                {
                    "outcome": "response",
                    "elapsed_seconds": elapsed,
                    "message_count": message_count,
                    "content": answer,
                    "content_sha256": _sha(answer),
                    "stats": result.get("stats"),
                    "structure": _json_array_counts(answer),
                    "raw_response": result,
                }
            )
        except (TimeoutError, OSError, ValueError, urllib.error.HTTPError) as err:
            case.update(
                {
                    "outcome": "failed",
                    "elapsed_seconds": round(time.perf_counter() - start, 3),
                    "error_type": type(err).__name__,
                    "error_message": str(err)[:200],
                }
            )
            record["stopped_early"] = True
        record["cases"][jid] = case
        (out / "PRIVATE_NATIVE_TRIAL.json").write_text(
            json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )
        print(
            jid,
            case["outcome"],
            case["elapsed_seconds"],
            "visible_chars",
            len(case.get("content", "")),
            "valid_json",
            case.get("structure", {}).get("is_json", False),
            flush=True,
        )
        if record["stopped_early"]:
            break

    public = {
        "contract": contract,
        "prompt_sha256": record["prompt_sha256"],
        "model": MODEL,
        "reasoning": "off",
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "database_sha256": db_sha256,
        "total_planned": len(JOBS),
        "attempted": len(record["cases"]),
        "stopped_early": record["stopped_early"],
        "production_writes": 0,
        "accepted_semantic_claims": 0,
        "candidate_only": True,
        "cases": {
            job: {
                k: v
                for k, v in case.items()
                if k
                in (
                    "outcome",
                    "elapsed_seconds",
                    "content_sha256",
                    "structure",
                    "error_type",
                    "source_semantic_sha256",
                    "message_count",
                    "stats",
                )
            }
            for job, case in record["cases"].items()
        },
    }
    (out / "SAFE_NATIVE_TRIAL_SUMMARY.json").write_text(
        json.dumps(public, sort_keys=True, indent=2) + "\n"
    )
    return public


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run_trial(args.database, args.out)
    print("B2_NATIVE_TRIAL_COMPLETED", result["attempted"], "of", result["total_planned"])


if __name__ == "__main__":
    main()
