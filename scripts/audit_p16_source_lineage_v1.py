"""Bounded original-language source lineage audit; no production database writes.

Example:
  python scripts/audit_p16_source_lineage_v1.py \
    --database data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 \
    --jobs tNhZ tMps tMqd tNDx tMjm \
    --report docs/working-memory/2026-11-13_p16_source_lineage/COHORT_AUDIT.json \
    --private data/local-acceptance/p16-source-lineage-2026-11-13/PRIVATE_REVIEW.json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.source_lineage_v1 import (
    CONTRACT_VERSION,
    align_legacy_english_field,
    original_source_spine,
)
from jobhunter.source_obligation_audit_v1 import source_skill_obligation_warnings
from jobhunter.translation_store import TranslationStore


def _unique_job_ids(values: list[str]) -> tuple[str, ...]:
    ids = tuple(dict.fromkeys(x.strip() for x in values if x.strip()))
    if not 1 <= len(ids) <= 20:
        raise ValueError("One to twenty exact source job IDs are required")
    if any(not x.isascii() or not x.isalnum() for x in ids):
        raise ValueError("Source job IDs must contain ASCII letters and digits only")
    return ids


def audit_on_snapshot(
    database: Path,
    jobs: tuple[str, ...],
) -> tuple[dict, dict]:
    if not database.exists() or not database.is_file():
        raise FileNotFoundError("Selected source database is not a regular file")
    if not jobs or len(jobs) > 20 or len(jobs) != len(set(jobs)):
        raise ValueError("Provide one to twenty distinct selected job IDs")
    with tempfile.TemporaryDirectory(prefix="jobhunter-p16-lineage-v1-") as temp:
        snapshot = Path(temp) / "source-copy.sqlite3"
        source_uri = f"{database.resolve().as_uri()}?mode=ro"
        with (
            sqlite3.connect(source_uri, uri=True) as original,
            sqlite3.connect(snapshot) as local,
        ):
            original.backup(local)
            assert local.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            assert not local.execute("PRAGMA foreign_key_check").fetchall()
        store = TranslationStore(snapshot)
        cases = []
        private_cases = []
        for job_id in jobs:
            source = store.latest_source_version(job_id)
            translation = store.latest_artifact(job_id)
            if source is None or translation is None:
                cases.append({
                    "job_id": job_id,
                    "status": "missing_current_source_or_translation",
                    "source_available": source is not None,
                    "translation_available": translation is not None,
                })
                continue
            spine = original_source_spine(source)
            links = align_legacy_english_field(spine, source, translation)
            warnings = source_skill_obligation_warnings(spine, source)
            classes = Counter(x.kind for x in spine.spans)
            obligations = Counter(x.obligation for x in spine.spans)
            alignment = Counter(x.alignment for x in links)
            cases.append({
                "job_id": job_id,
                "status": "inspected_not_semantically_approved",
                "source_detail_version_id": source.job_detail_version_id,
                "source_semantic_sha256": source.semantic_sha256,
                "source_language": source.source_language,
                "description_field_sha256": spine.field_text_sha256,
                "translation_artifact_id": translation.id,
                "translation_schema_version": translation.translation_schema_version,
                "translation_sha256": translation.translation_sha256,
                "spans": len(spine.spans),
                "span_kind_counts": dict(sorted(classes.items())),
                "span_obligation_counts": dict(sorted(obligations.items())),
                "alignment_counts": dict(sorted(alignment.items())),
                "structured_tag_preference_warnings": len(warnings),
                "nonpromotable": True,
                "source_exact_utf8_offsets_checked": True,
                "source_span_ids": [s.span_id for s in spine.spans],
                "warning_span_ids": [warning.source_span_id for warning in warnings],
            })
            private_cases.append({
                "job_id": job_id,
                "source_semantic_sha256": source.semantic_sha256,
                "translation_sha256": translation.translation_sha256,
                "original_description": source.fields["description"],
                "legacy_english_description": translation.fields["description"],
                "spans": [{
                    "span_id": span.span_id,
                    "start": span.start,
                    "end": span.end,
                    "start_utf8": span.start_utf8,
                    "end_utf8": span.end_utf8,
                    "text": span.exact_text,
                    "kind": span.kind,
                    "obligation": span.obligation,
                    "authority_basis": span.authority_basis,
                    "heading_text": span.heading_text,
                } for span in spine.spans],
                "review_warnings": [{
                    "code": warning.code,
                    "structured_skill": warning.structured_skill,
                    "source_span_id": warning.source_span_id,
                } for warning in warnings],
            })
    summary = {
        "contract": "p16-source-lineage-audit-v1",
        "source_lineage_contract": CONTRACT_VERSION,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "jobs_requested": len(jobs),
        "jobs_inspected": sum(x["status"] == "inspected_not_semantically_approved" for x in cases),
        "candidate_generated": 0,
        "semantic_reviewed_or_promoted": 0,
        "current_english_p16_changed": False,
        "original_analysis_p16_changed": False,
        "source_db_changed": False,
        "whole_field_v2_provenance_cannot_prove_item_alignment": True,
        "source_snapshot_integrity": "ok",
        "source_snapshot_foreign_keys": "ok",
        "privacy": "public_counts_hashes_only",
        "cases": cases,
    }
    private = {
        "contract": "p16-original-source-lineage-private-review-v1",
        "privacy": "local_only_never_commit",
        "cases": private_cases,
    }
    return summary, private


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--jobs", nargs="+", required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    args = parser.parse_args()
    jobs = _unique_job_ids(args.jobs)
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file() or not (
        root / "src/jobhunter/source_lineage_v1.py"
    ).is_file():
        raise RuntimeError("Run the source lineage audit from the repository root")
    private = args.private.resolve()
    expected = root / "data/local-acceptance"
    if not private.is_relative_to(expected):
        raise ValueError("Private review must remain inside ignored data/local-acceptance")
    report = args.report.resolve()
    if not report.is_relative_to(root / "docs/working-memory"):
        raise ValueError("Public report must remain inside docs/working-memory")
    if report == private or args.database.resolve() in {report, private}:
        raise ValueError("Input and output paths must be distinct")
    if report.exists() or private.exists():
        raise FileExistsError("Outputs already exist; never overwrite audit evidence")
    summary, details = audit_on_snapshot(args.database, jobs)
    report.parent.mkdir(parents=True, exist_ok=True)
    private.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(summary, ensure_ascii=False, indent=2,
                                 sort_keys=True) + "\n", encoding="utf-8")
    private.write_text(json.dumps(details, ensure_ascii=False, indent=2,
                                  sort_keys=True) + "\n", encoding="utf-8")
    print("source_lineage_contract:", summary["source_lineage_contract"])
    print("jobs_inspected:", summary["jobs_inspected"])
    print("public_report:", report.relative_to(root))
    print("private_review:", private.relative_to(root))
    print("semantic_promotion:", summary["semantic_reviewed_or_promoted"])


if __name__ == "__main__":
    main()
