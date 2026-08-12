#!/usr/bin/env python3
"""Export a normal review snapshot with the isolated English P1.6 v11 candidate selected."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION
from jobhunter.analysis_service_v11 import ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.review_snapshot import (
    _analysis_payload,
    _translation_payload,
    build_review_snapshot,
)
from jobhunter.translation_store import TranslationStore


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export one repository-reviewable snapshot using English P1.6 v11 candidate."
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("review-snapshots/jobs"),
    )
    args = parser.parse_args()

    settings = Settings.load(args.config)
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise SystemExit("No configured analysis model")

    snapshot = build_review_snapshot(
        settings.database_path,
        args.job_id,
        analysis_model=model,
        capability_model=settings.effective_capability_lm_studio_model(),
        blueprint_model=settings.effective_blueprint_lm_studio_model(),
    )
    analysis_store = AnalysisStore(settings.database_path)
    candidate = analysis_store.latest_current(
        args.job_id,
        model=model,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
    )
    if candidate is None:
        raise SystemExit(
            f"No current {ENGLISH_PROMPT_VERSION} / {ANALYSIS_SCHEMA_VERSION} artifact for "
            f"{args.job_id!r}; run scripts/run_p16_v11_candidate.py first"
        )

    translation = None
    if candidate.translation_artifact_id is not None:
        translation = TranslationStore(settings.database_path).artifact_by_id(
            candidate.translation_artifact_id
        )
    if translation is None:
        raise SystemExit("P1.6 v11 candidate has no resolvable English projection dependency")

    snapshot["english_analysis"] = _analysis_payload(candidate)
    snapshot["english_projection"] = _translation_payload(translation)
    snapshot["capability_intelligence"] = None
    snapshot["role_capability_blueprint"] = None
    status = dict(snapshot.get("status") or {})
    status.update(
        {
            "english_projection_present": True,
            "english_analysis_present": True,
            "translation_matches_english_analysis": True,
            "capability_intelligence_present": False,
            "capability_is_current_chain": False,
            "role_capability_blueprint_present": False,
            "blueprint_is_current_chain": False,
        }
    )
    snapshot["status"] = status

    args.output_dir.mkdir(parents=True, exist_ok=True)
    destination = args.output_dir / f"{args.job_id}.json"
    destination.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(destination.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
