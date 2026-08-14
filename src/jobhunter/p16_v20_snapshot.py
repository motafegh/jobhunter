"""Review-snapshot helper for isolated P1.6 v20 candidate."""
from __future__ import annotations

import json
from pathlib import Path

from jobhunter.analysis_service_v20 import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.review_snapshot import _analysis_payload, _translation_payload, build_review_snapshot
from jobhunter.translation_store import TranslationStore


def export_candidate_snapshot(settings: Settings, job_id: str, output_dir: Path) -> Path:
    model = settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No configured analysis model")
    snapshot = build_review_snapshot(
        settings.database_path,
        job_id,
        analysis_model=model,
        capability_model=settings.effective_capability_lm_studio_model(),
        blueprint_model=settings.effective_blueprint_lm_studio_model(),
    )
    candidate = AnalysisStore(settings.database_path).latest_current(
        job_id,
        model=model,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
    )
    if candidate is None:
        raise ValueError(f"No current {ENGLISH_PROMPT_VERSION} candidate for {job_id!r}")
    translation = None
    if candidate.translation_artifact_id is not None:
        translation = TranslationStore(settings.database_path).artifact_by_id(
            candidate.translation_artifact_id
        )
    if translation is None:
        raise ValueError("P1.6 v20 candidate has no resolvable English projection dependency")
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
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{job_id}.json"
    destination.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination
