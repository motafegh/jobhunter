"""One bounded B2 local LM Studio trial of model-produced original item references.

The legacy seven-array v3 output has no citations. This version asks a model
for compact English claims and numbered exact-original item references. The
references are *advisory suggestions*, not Persian semantic entailment or
accepted employer facts. No production/canonical persistence is modified.

From the repo root, after confirming LM Studio has the exact model loaded:
python scripts/probe_b2_model_source_refs.py --database PRIVATE_B0_DB --out PRIVATE_NEW_DIR

All raw original text, model requests/responses and item maps remain ignored.
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
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from probe_b2_local_semantics import JOBS, MODEL
from probe_b2_native_reasoning_off import BASE, _answer_parts
from reconcile_b2_native_trials import _parse_model_json

from jobhunter.source_claim_reconciliation_b2 import AdvisoryClaim, reconcile_advisory_claims
from jobhunter.source_item_candidate_b2 import (
    B2SourceCandidate,
    interpret_original_source_candidate,
    verify_b2_candidate,
)
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

CONTRACT = "jobhunter-b2-native-source-references-v1"
DB_SHA256 = "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
FIELD_ORDER = (
    "duties",
    "requirements",
    "preferences",
    "alternatives",
    "arrangements",
    "uncertainties",
    "work_implied_capabilities",
)
PROMPT = (
    "Interpret the original Persian job advertisement below. Each numbered [N] is "
    "one original employer-source item; the headings are also original context. "
    "Return ONLY a JSON object with seven arrays: duties, requirements, preferences, "
    "alternatives, arrangements, uncertainties, work_implied_capabilities. Each array "
    'entry is {"t":"short English statement","s":[N]} citing the original item number(s); '
    "use s:[] when no exact original item supports an interpretation. "
    "Distinguish assigned tasks, applicant qualifications and preferences from work "
    "arrangements. Do not turn an ability into an assigned task or a work-implied "
    "capability into mandatory past employment. Preserve explicit required/preferred "
    "wording and meaningful OR choices; leave unclear employer strength uncertain. "
    "Keep useful work-implied capabilities separately when supported by duties. "
    "Keep output concise and source-grounded; do not invent employer facts."
)
MAX_OUTPUT_TOKENS = 2700
TIMEOUT_SECONDS = 55
MAX_CALLS = len(JOBS)


def sha(blob: str | bytes) -> str:
    return hashlib.sha256(blob.encode("utf-8") if isinstance(blob, str) else blob).hexdigest()


def make_numbered_input(
    source: TranslationSourceVersion, candidate: B2SourceCandidate
) -> tuple[str, dict[int, str]]:
    """Retain exact original items, their order and original section headings."""
    verify_b2_candidate(candidate, source)
    rows = []
    id_to_anchor = {}
    prior_heading: str | None = None
    for number, item in enumerate(candidate.items):
        if item.heading != prior_heading and item.heading:
            rows.append(f"HEADING: {item.heading}")
        rows.append(f"[{number}] {item.anchor.exact_text}")
        id_to_anchor[number] = item.anchor.anchor_id
        prior_heading = item.heading
    return "\n".join(rows), id_to_anchor


def normalize_model_output(
    answer: str, valid_ids: dict[int, str]
) -> tuple[tuple[AdvisoryClaim, ...], dict[str, Any]]:
    """No semantic validation. Invalid invented IDs are rejected, not coerced."""
    parsed = _parse_model_json(answer)
    if set(parsed) != set(FIELD_ORDER):
        raise ValueError("Unexpected model output categories")
    claims = []
    invalid_refs = []
    for field in FIELD_ORDER:
        for index, row in enumerate(parsed[field]):
            if not isinstance(row, dict) or set(row) != {"t", "s"}:
                raise ValueError("Model claim is not a t/s object")
            statement, ids = row["t"], row["s"]
            if not isinstance(statement, str) or not statement.strip() or not isinstance(ids, list):
                raise ValueError("Invalid model claim text or reference container")
            if any(isinstance(n, bool) or not isinstance(n, int) for n in ids):
                raise ValueError("Source IDs must be integer indices")
            if len(set(ids)) != len(ids):
                raise ValueError("Repeated source item references")
            wrong = [n for n in ids if n not in valid_ids]
            if wrong:
                invalid_refs.append({"field": field, "index": index, "invalid_ids": wrong})
            # An invalid citation cannot be silently replaced by a plausible
            # source, nor mixed with otherwise valid citations in a promoted claim.
            refs = () if wrong else tuple(valid_ids[n] for n in ids)
            claims.append(
                AdvisoryClaim(
                    field=field,
                    index=index,
                    text=statement,
                    source_anchor_ids=refs,
                    link_provenance="model_suggested" if refs else "none",
                )
            )
    return tuple(claims), {
        "invalid_reference_claims": invalid_refs,
        "field_counts": {f: len(parsed[f]) for f in FIELD_ORDER},
    }


def request_body(numbered_original: str) -> dict[str, Any]:
    return {
        "model": MODEL,
        "system_prompt": PROMPT,
        "input": numbered_original,
        "temperature": 0,
        "reasoning": "off",
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "stream": False,
        "store": False,
    }


def run(database: Path, out: Path) -> dict[str, Any]:
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Run from JobHunter repository root")
    if not out.resolve().is_relative_to(root / "data/local-acceptance") or out.exists():
        raise ValueError("New private output must remain in ignored data/local-acceptance")
    if not database.is_file() or sha(database.read_bytes()) != DB_SHA256:
        raise ValueError("Frozen B0 database is missing or has changed")

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(BASE + "/api/v1/models", timeout=5) as response:
        models = json.load(response).get("models", [])
    matching = [m for m in models if m.get("key") == MODEL]
    if len(matching) != 1 or not matching[0].get("loaded_instances"):
        raise ValueError("Exact local Gemma model must already be loaded")
    if "off" not in matching[0].get("capabilities", {}).get("reasoning", {}).get(
        "allowed_options", []
    ):
        raise ValueError("Model does not support reasoning off")

    with tempfile.TemporaryDirectory(prefix="jobhunter-b2-refs-") as temp:
        copied_path = Path(temp) / "copy.sqlite3"
        with (
            sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as original,
            sqlite3.connect(copied_path) as copy,
        ):
            original.backup(copy)
            if copy.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Frozen SQLite copy integrity failure")
            if copy.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Frozen SQLite copy foreign-key failure")
        store = TranslationStore(copied_path)
        source_items = []
        for job in JOBS:
            source = store.latest_source_version(job)
            if source is None:
                raise ValueError(f"Missing frozen source for {job}")
            candidate = interpret_original_source_candidate(source)
            numbered, source_map = make_numbered_input(source, candidate)
            source_items.append((job, source, candidate, numbered, source_map))

    out.mkdir(parents=True)
    record: dict[str, Any] = {
        "contract": CONTRACT,
        "authority": "research_only_no_downstream_reuse",
        "source_database_sha256": DB_SHA256,
        "model": MODEL,
        "prompt_sha256": sha(PROMPT),
        "system_prompt": PROMPT,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "reasoning": "off",
        "model_declared_reasoning": matching[0]["capabilities"]["reasoning"],
        "cases": {},
        "stopped_early": False,
        "source_exposure": "four_existing_development_cases_no_holdout",
        "accepted_employer_facts": 0,
    }
    for job, source, candidate, numbered, source_map in source_items:
        body = request_body(numbered)
        start = time.perf_counter()
        case: dict[str, Any] = {
            "source_job_id": job,
            "source_semantic_sha256": source.semantic_sha256,
            "original_description_sha256": sha(source.fields["description"]),
            "numbered_input": numbered,
            "input_sha256": sha(numbered),
            "source_items": [
                {
                    "number": index,
                    "anchor_id": source_map[index],
                    "original_text": item.anchor.exact_text,
                }
                for index, item in enumerate(candidate.items)
            ],
            "request_sha256": sha(json.dumps(body, sort_keys=True, ensure_ascii=False)),
        }
        try:
            request = urllib.request.Request(
                BASE + "/api/v1/chat",
                data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
                result = json.load(response)
            answer, message_count = _answer_parts(result)
            case.update(
                {
                    "outcome": "response",
                    "elapsed_seconds": round(time.perf_counter() - start, 3),
                    "content": answer,
                    "content_sha256": sha(answer),
                    "message_count": message_count,
                    "raw_response": result,
                    "stats": result.get("stats"),
                }
            )
            try:
                claims, diagnostics = normalize_model_output(answer, source_map)
                reconciled = reconcile_advisory_claims(source, candidate, claims)
                counts = Counter(row.grounding_state for row in reconciled.claims)
                flags = Counter(
                    flag for row in reconciled.claims for flag in row.diagnostic_signals
                )
                case.update(
                    {
                        "structured": True,
                        "parsed_claims": [asdict(c) for c in claims],
                        "reconciled_claims": [asdict(c) for c in reconciled.claims],
                        "model_claim_count": len(claims),
                        "link_counts": dict(counts),
                        "diagnostic_signal_counts": dict(flags),
                        "invalid_ref_claims": diagnostics["invalid_reference_claims"],
                        "field_counts": diagnostics["field_counts"],
                    }
                )
            except ValueError as exc:
                case["structured"] = False
                case["parse_error"] = str(exc)[:200]
        except (OSError, ValueError, TimeoutError, urllib.error.HTTPError) as exc:
            case.update(
                {
                    "outcome": "failed",
                    "elapsed_seconds": round(time.perf_counter() - start, 3),
                    "error": type(exc).__name__,
                    "error_message": str(exc)[:200],
                }
            )
            record["stopped_early"] = True
        record["cases"][job] = case
        (out / "PRIVATE_SOURCE_REFERENCED_TRIAL.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        print(
            job,
            case["outcome"],
            case["elapsed_seconds"],
            "structured",
            case.get("structured"),
            "claims",
            case.get("model_claim_count", 0),
            "linked",
            case.get("link_counts", {}).get("linked_semantics_unreviewed", 0)
            + case.get("link_counts", {}).get("source_candidate_disagreement", 0),
            flush=True,
        )
        if record["stopped_early"]:
            break

    if sha(database.read_bytes()) != DB_SHA256:
        raise ValueError("Frozen SQLite input changed")
    public = {
        "contract": CONTRACT,
        "authority": "candidate_only_no_downstream_reuse",
        "source_database_sha256": DB_SHA256,
        "model": MODEL,
        "prompt_sha256": sha(PROMPT),
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "source_exposure": "four_existing_development_cases_no_holdout",
        "case_count": len(record["cases"]),
        "stopped_early": record["stopped_early"],
        "b2_semantic_gate": "OPEN_NO_PROMOTION",
        "accepted_employer_facts": 0,
        "cases": {
            job: {
                k: value
                for k, value in case.items()
                if k
                in {
                    "outcome",
                    "elapsed_seconds",
                    "structured",
                    "model_claim_count",
                    "link_counts",
                    "diagnostic_signal_counts",
                    "field_counts",
                    "source_semantic_sha256",
                    "content_sha256",
                    "parse_error",
                    "invalid_ref_claims",
                }
            }
            for job, case in record["cases"].items()
        },
    }
    public["private_trial_sha256"] = sha(
        (out / "PRIVATE_SOURCE_REFERENCED_TRIAL.json").read_bytes()
    )
    (out / "SAFE_SOURCE_REFERENCED_METRICS.json").write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n"
    )
    return public


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--database", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    result = run(args.database, args.out)
    print(
        json.dumps(
            {
                "case_count": result["case_count"],
                "stopped_early": result["stopped_early"],
                "b2_semantic_gate": result["b2_semantic_gate"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
