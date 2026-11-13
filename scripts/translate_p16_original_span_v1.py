"""Translate one exact original source span with local LM Studio only.

This is an isolated candidate and does not write to JobHunter's production
source, translation, P1.6 or Market persistence.

Example (LM Studio must already be running):
  timeout 180 python scripts/translate_p16_original_span_v1.py \
    --database data/local-acceptance/current-real-ads-2026-11-12/data/current-cohort.sqlite3 \
    --job tNDx --span d6b09e236c88e964dc5c886608e54c5f \
    --model gemma-4-e4b-it-ud --base-url http://127.0.0.1:18080/v1 \
    --out data/local-acceptance/p16-source-lineage-2026-11-13/PRIVATE_TRANSLATION_EDR.json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from jobhunter.source_bound_translation_v1 import (
    check_candidate_source_identity,
    translate_selected_spans,
)
from jobhunter.source_lineage_v1 import original_source_spine
from jobhunter.translation.lm_studio import LMStudioTranslationProvider
from jobhunter.translation_store import TranslationStore


def local_lm_studio_url(url: str) -> str:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path.rstrip("/") != "/v1"
    ):
        raise ValueError("LM Studio endpoint must be local loopback HTTP with path /v1")
    if parsed.port is None:
        raise ValueError("LM Studio loopback port must be explicit")
    return url


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--span", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if not (root / "AGENTS.md").is_file() or not (
        root / "src/jobhunter/source_bound_translation_v1.py"
    ).is_file():
        raise RuntimeError("Run from JobHunter repository root")
    output = args.out.resolve()
    if not output.is_relative_to(root / "data/local-acceptance"):
        raise ValueError("Translated source text must remain in ignored local acceptance data")
    if output.exists() or args.database.resolve() == output:
        raise FileExistsError("Translation output already exists or conflicts with input")
    if not args.job.isascii() or not args.job.isalnum():
        raise ValueError("Invalid exact source job ID")
    if len(args.span) != 32 or any(c not in "0123456789abcdef" for c in args.span):
        raise ValueError("Invalid exact source span identity")
    if not args.database.exists() or not args.database.is_file():
        raise FileNotFoundError("Selected source database not found")
    url = local_lm_studio_url(args.base_url)
    with tempfile.TemporaryDirectory(prefix="jobhunter-sourcebound-v1-") as directory:
        snap = Path(directory) / "source.sqlite3"
        with (
            sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True) as source_db,
            sqlite3.connect(snap) as target_db,
        ):
            source_db.backup(target_db)
            if target_db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Source snapshot integrity failed")
            if target_db.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Source snapshot foreign keys failed")
        store = TranslationStore(snap)
        source = store.latest_source_version(args.job)
        if source is None:
            raise ValueError("No current parsed source version for selected job")
        spine = original_source_spine(source)
        if args.span not in {span.span_id for span in spine.spans}:
            raise ValueError("Requested span is not part of current source version")
        translator = LMStudioTranslationProvider(
            base_url=url,
            configured_model=args.model,
            timeout_seconds=20,
            max_retries=0,
        )
        candidates = translate_selected_spans(
            spine,
            provider=translator,
            selected_span_ids=(args.span,),
            max_segments=1,
        )
        check_candidate_source_identity(spine, candidates)
        chosen = next(span for span in spine.spans if span.span_id == args.span)
        private = {
            "contract": "p16-sourcebound-local-evaluation-record-v1",
            "created_at_utc": datetime.now(UTC).isoformat(),
            "privacy": "local_only_never_commit",
            "source_semantic_sha256": source.semantic_sha256,
            "source_detail_version_id": source.job_detail_version_id,
            "source_field_sha256": spine.field_text_sha256,
            "original_span_id": chosen.span_id,
            "original_exact_text": chosen.exact_text,
            "original_obligation_candidate": chosen.obligation,
            "original_basis": chosen.authority_basis,
            "translation_candidate": asdict(candidates[0]),
            "semantic_review_state": "unreviewed",
            "promotion": False,
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(private, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        print("saved_local_private_translation:", output.relative_to(root))
        print("source_bound:", True)
        print("translation_candidate_state:", candidates[0].status)
        print("review_flag_count:", len(candidates[0].review_flags))
        print("promoted:", False)


if __name__ == "__main__":
    main()
