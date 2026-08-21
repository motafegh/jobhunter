"""Export deterministic, repository-safe job intelligence snapshots for review."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_ANALYSIS_SCHEMA_VERSION,
    ORIGINAL_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import (
    CapabilityIntelligenceArtifact,
    CapabilityIntelligenceStore,
)
from jobhunter.config import ConfigLoadError, Settings
from jobhunter.role_blueprint_service import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
)
from jobhunter.role_blueprint_store import RoleBlueprintArtifact, RoleBlueprintStore
from jobhunter.translation_store import TranslationArtifact, TranslationStore

SNAPSHOT_SCHEMA_VERSION = "job-review-snapshot-v1"
_DEFAULT_OUTPUT_DIR = Path("review-snapshots/jobs")
_SAFE_JOB_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class ReviewSnapshotError(ValueError):
    """Raised when a current review snapshot cannot be produced safely."""


def _source_record(database_path: Path, source_job_id: str) -> dict[str, Any]:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT p.source_job_id, p.canonical_url, p.title_observed,
                   p.first_seen_at, p.last_seen_at, p.lifecycle_state,
                   v.id AS job_detail_version_id, v.fetched_at, v.final_url,
                   v.status_code, v.content_sha256, v.semantic_sha256,
                   v.evidence_path, v.parser_version, v.parse_status, v.fields_json
            FROM job_postings AS p
            JOIN job_detail_versions AS v ON v.job_posting_id = p.id
            WHERE p.source = 'jobinja' AND p.source_job_id = ?
              AND v.parse_status = 'parsed'
              AND v.id = (
                  SELECT MAX(v2.id)
                  FROM job_detail_versions AS v2
                  WHERE v2.job_posting_id = p.id AND v2.parse_status = 'parsed'
              )
            LIMIT 1
            """,
            (source_job_id,),
        ).fetchone()
    if row is None:
        raise ReviewSnapshotError(
            f"No current parsed Jobinja source record exists for {source_job_id!r}"
        )
    return {
        "source_job_id": str(row["source_job_id"]),
        "job_detail_version_id": int(row["job_detail_version_id"]),
        "canonical_url": str(row["canonical_url"]),
        "title_observed": row["title_observed"],
        "first_seen_at": str(row["first_seen_at"]),
        "last_seen_at": str(row["last_seen_at"]),
        "lifecycle_state": str(row["lifecycle_state"]),
        "fetched_at": str(row["fetched_at"]),
        "final_url": str(row["final_url"]),
        "status_code": int(row["status_code"]),
        "content_sha256": str(row["content_sha256"]),
        "semantic_sha256": str(row["semantic_sha256"] or ""),
        "evidence_path": str(row["evidence_path"]),
        "parser_version": str(row["parser_version"]),
        "parse_status": str(row["parse_status"]),
        "fields": json.loads(str(row["fields_json"])),
    }


def _translation_payload(artifact: TranslationArtifact | None) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "model": artifact.provider_model,
        "provider": artifact.provider_name,
        "schema_version": artifact.translation_schema_version,
        "source_semantic_sha256": artifact.source_semantic_sha256,
        "source_language": artifact.source_language,
        "target_language": artifact.target_language,
        "translation_sha256": artifact.translation_sha256,
        "translated_segment_count": artifact.translated_segment_count,
        "native_segment_count": artifact.native_segment_count,
        "segment_provenance": artifact.segment_provenance,
        "created_at": artifact.created_at,
        "fields": artifact.fields,
    }


def _analysis_payload(artifact: AnalysisArtifact | None) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "translation_artifact_id": artifact.translation_artifact_id,
        "model": artifact.model,
        "prompt_version": artifact.prompt_version,
        "schema_version": artifact.schema_version,
        "created_at": artifact.created_at,
        "semantic_review_status": artifact.semantic_review_status,
        "semantic_reviewed_at": artifact.semantic_reviewed_at,
        "semantic_review_note": artifact.semantic_review_note,
        "analysis": artifact.analysis,
    }


def _capability_payload(
    artifact: CapabilityIntelligenceArtifact | None,
) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "translation_artifact_id": artifact.translation_artifact_id,
        "analysis_artifact_id": artifact.analysis_artifact_id,
        "model": artifact.model,
        "prompt_version": artifact.prompt_version,
        "schema_version": artifact.schema_version,
        "created_at": artifact.created_at,
        "intelligence": artifact.intelligence,
    }


def _blueprint_payload(artifact: RoleBlueprintArtifact | None) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "translation_artifact_id": artifact.translation_artifact_id,
        "analysis_artifact_id": artifact.analysis_artifact_id,
        "capability_artifact_id": artifact.capability_artifact_id,
        "model": artifact.model,
        "prompt_version": artifact.prompt_version,
        "schema_version": artifact.schema_version,
        "created_at": artifact.created_at,
        "blueprint": artifact.blueprint,
    }


def build_review_snapshot(
    database_path: Path,
    source_job_id: str,
    *,
    analysis_model: str | None = None,
    capability_model: str | None = None,
    blueprint_model: str | None = None,
) -> dict[str, Any]:
    """Build the configured current chain without raw model protocol or private local state."""

    source_job_id = source_job_id.strip()
    if not _SAFE_JOB_ID_RE.fullmatch(source_job_id):
        raise ReviewSnapshotError("source_job_id contains unsupported path characters")
    if not database_path.exists():
        raise ReviewSnapshotError(f"JobHunter database does not exist: {database_path}")

    source = _source_record(database_path, source_job_id)
    translation_store = TranslationStore(database_path)
    analysis_store = AnalysisStore(database_path)
    capability_store = CapabilityIntelligenceStore(database_path)
    blueprint_store = RoleBlueprintStore(database_path)

    english_analysis = analysis_store.latest_current(
        source_job_id,
        model=analysis_model,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
    )
    original_analysis = analysis_store.latest_current(
        source_job_id,
        model=analysis_model,
        prompt_version=ORIGINAL_PROMPT_VERSION,
        schema_version=ORIGINAL_ANALYSIS_SCHEMA_VERSION,
    )

    translation = None
    if english_analysis is not None and english_analysis.translation_artifact_id is not None:
        translation = translation_store.artifact_by_id(english_analysis.translation_artifact_id)
    if translation is None:
        translation = translation_store.latest_artifact(source_job_id, target_language="en")

    capability = capability_store.latest_current(
        source_job_id,
        model=capability_model,
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )
    blueprint = blueprint_store.latest_current(
        source_job_id,
        model=blueprint_model,
        prompt_version=BLUEPRINT_PROMPT_VERSION,
        schema_version=BLUEPRINT_SCHEMA_VERSION,
    )

    translation_matches_analysis = bool(
        translation is not None
        and english_analysis is not None
        and english_analysis.translation_artifact_id == translation.id
    )
    capability_is_current_chain = bool(
        capability is not None
        and english_analysis is not None
        and capability.analysis_artifact_id == english_analysis.id
        and capability.translation_artifact_id == english_analysis.translation_artifact_id
    )
    blueprint_is_current_chain = bool(
        blueprint is not None
        and capability is not None
        and capability_is_current_chain
        and blueprint.capability_artifact_id == capability.id
        and blueprint.analysis_artifact_id == capability.analysis_artifact_id
        and blueprint.translation_artifact_id == capability.translation_artifact_id
    )

    return {
        "snapshot_schema_version": SNAPSHOT_SCHEMA_VERSION,
        "source_job_id": source_job_id,
        "configured_models": {
            "analysis": analysis_model,
            "capability": capability_model,
            "blueprint": blueprint_model,
        },
        "status": {
            "english_projection_present": translation is not None,
            "english_analysis_present": english_analysis is not None,
            "english_analysis_semantic_review": (
                english_analysis.semantic_review_status
                if english_analysis is not None
                else None
            ),
            "original_analysis_present": original_analysis is not None,
            "capability_intelligence_present": capability is not None,
            "role_capability_blueprint_present": blueprint is not None,
            "translation_matches_english_analysis": translation_matches_analysis,
            "capability_is_current_chain": capability_is_current_chain,
            "blueprint_is_current_chain": blueprint_is_current_chain,
        },
        "source": source,
        "english_projection": _translation_payload(translation),
        "english_analysis": _analysis_payload(english_analysis),
        "original_analysis": _analysis_payload(original_analysis),
        "capability_intelligence": _capability_payload(
            capability if capability_is_current_chain else None
        ),
        "role_capability_blueprint": _blueprint_payload(
            blueprint if blueprint_is_current_chain else None
        ),
    }


def write_review_snapshot(
    database_path: Path,
    source_job_id: str,
    *,
    output_dir: Path = _DEFAULT_OUTPUT_DIR,
    analysis_model: str | None = None,
    capability_model: str | None = None,
    blueprint_model: str | None = None,
) -> Path:
    """Write one stable UTF-8 JSON file suitable for Git diff/review."""

    snapshot = build_review_snapshot(
        database_path,
        source_job_id,
        analysis_model=analysis_model,
        capability_model=capability_model,
        blueprint_model=blueprint_model,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{source_job_id}.json"
    destination.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter-review-snapshot",
        description=(
            "Export one current JobHunter job/intelligence chain as repository-reviewable JSON."
        ),
    )
    parser.add_argument("job_id", help="Stable Jobinja job ID, for example tG9K")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=_DEFAULT_OUTPUT_DIR)
    return parser


def main(argv: list[str] | None = None) -> int:
    parsed = _parser().parse_args(argv)
    try:
        settings = Settings.load(parsed.config)
        destination = write_review_snapshot(
            settings.database_path,
            parsed.job_id,
            output_dir=parsed.output_dir,
            analysis_model=settings.effective_analysis_lm_studio_model(),
            capability_model=settings.effective_capability_lm_studio_model(),
            blueprint_model=settings.effective_blueprint_lm_studio_model(),
        )
    except (ConfigLoadError, ValidationError, ReviewSnapshotError, OSError) as exc:
        print(f"Review snapshot failed: {exc}", file=sys.stderr)
        return 1
    print(destination.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
