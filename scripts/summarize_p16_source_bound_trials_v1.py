"""Verify local source-bound translation candidates and export only safe hashes/counts.

Run from the repo root. No source, English prose or raw inference output is
published. Reuses a read-only SQLite backup; never mutates current P1.6.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import tempfile
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.source_bound_translation_v1 import (
    BoundTranslationCandidate,
    check_candidate_source_identity,
)
from jobhunter.source_lineage_v1 import original_source_spine
from jobhunter.translation_store import TranslationStore


def _parse_status(content: str) -> dict[str, str]:
    result = {}
    for line in content.splitlines():
        if not line.strip():
            continue
        if "=" not in line:
            raise ValueError("Malformed candidate status line")
        key, value = line.split("=", 1)
        if key in result:
            raise ValueError("Duplicate candidate status key")
        result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--private-dir", required=True, type=Path)
    parser.add_argument("--jobs", required=True, nargs="+")
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file():
        raise RuntimeError("Run from JobHunter repository root")
    private_dir = args.private_dir.resolve()
    out = args.report.resolve()
    if not private_dir.is_relative_to(root / "data/local-acceptance"):
        raise ValueError("Private review must stay under ignored local acceptance")
    if not out.is_relative_to(root / "docs/working-memory"):
        raise ValueError("Public report must stay under docs/working-memory")
    if out.exists() or not 1 <= len(args.jobs) <= 20:
        raise ValueError("Output already exists or job selection is unbounded")
    if len(set(args.jobs)) != len(args.jobs):
        raise ValueError("Duplicate job IDs are not allowed")
    with tempfile.TemporaryDirectory(prefix="jobhunter-bound-report-v1-") as directory:
        snap = Path(directory) / "snapshot.sqlite3"
        with (
            sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True) as src,
            sqlite3.connect(snap) as dest,
        ):
            src.backup(dest)
            if dest.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Source snapshot integrity failed")
            if dest.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Source snapshot foreign keys failed")
        store = TranslationStore(snap)
        results = []
        for job in args.jobs:
            if not job.isascii() or not job.isalnum():
                raise ValueError("Invalid source job ID")
            status_path = private_dir / f"TRANSLATION_{job}.status"
            private_path = private_dir / f"PRIVATE_TRANSLATION_{job}.json"
            log_path = private_dir / f"TRANSLATION_{job}.log"
            status = _parse_status(status_path.read_text())
            private = json.loads(private_path.read_text())
            source = store.latest_source_version(job)
            if source is None:
                raise ValueError("Candidate source no longer exists at current version")
            spine = original_source_spine(source)
            fields_by_name = {field.name for field in fields(BoundTranslationCandidate)}
            payload = private["translation_candidate"]
            candidate = BoundTranslationCandidate(**{
                key: payload[key] for key in fields_by_name
            })
            check_candidate_source_identity(spine, (candidate,))
            span = next(x for x in spine.spans if x.span_id == candidate.original_span_id)
            if (
                private["original_exact_text"] != span.exact_text
                or private["source_semantic_sha256"] != source.semantic_sha256
                or private["original_span_id"] != span.span_id
                or private["semantic_review_state"] != "unreviewed"
                or private["promotion"] is not False
                or status.get("source_job_id") != job
                or status.get("span_id") != span.span_id
                or status.get("model") != candidate.provider_model
                or status.get("exit_code") != "0"
            ):
                raise ValueError("Local source-bound trial provenance mismatch")
            results.append({
                "job_id": job,
                "source_detail_version_id": source.job_detail_version_id,
                "source_semantic_sha256": source.semantic_sha256,
                "source_field_sha256": spine.field_text_sha256,
                "original_span_id": span.span_id,
                "original_span_sha256": span.text_sha256,
                "original_kind": span.kind,
                "original_obligation": span.obligation,
                "translation_status": candidate.status,
                "translation_provider": candidate.provider_name,
                "model": candidate.provider_model,
                "translation_sha256": candidate.translated_sha256,
                "review_flag_count": len(candidate.review_flags),
                "elapsed_seconds": int(status["elapsed_seconds"]),
                "raw_trial_log_sha256": hashlib.sha256(log_path.read_bytes()).hexdigest(),
                "private_record_sha256": hashlib.sha256(private_path.read_bytes()).hexdigest(),
                "candidate_semantic_review_state": "unreviewed",
                "promoted": False,
            })
    summary = {
        "contract": "p16-sourcebound-translation-trial-v1",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "case_count": len(results),
        "source_bound_completed": len(results),
        "semantically_accepted": 0,
        "current_translation_modified": False,
        "current_english_p16_modified": False,
        "private_text_exported": False,
        "results": results,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, sort_keys=True, indent=2,
                              ensure_ascii=False) + "\n", encoding="utf-8")
    print("verified_private_trials:", len(results))
    print("public_report:", out.relative_to(root))
    print("accepted_or_promoted:", summary["semantically_accepted"])


if __name__ == "__main__":
    main()
