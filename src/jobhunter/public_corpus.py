"""Version-controlled public corpus projection for durable JobHunter job data.

The local SQLite database remains the runtime authority. This module projects only
public/job-domain state into deterministic UTF-8 JSON suitable for Git review and
remote reuse. Raw model protocol, request bodies, secrets, logs, and machine-local
paths are deliberately excluded.
"""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
from jobhunter.storage import JobHunterStore
from jobhunter.translation_store import TranslationArtifact, TranslationStore

PUBLIC_CORPUS_SCHEMA_VERSION = "jobhunter-public-corpus-v1"
DEFAULT_PUBLIC_CORPUS_DIR = Path("corpus")
_SAFE_JOB_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class PublicCorpusError(ValueError):
    """Raised when the public corpus cannot be exported or verified safely."""


@dataclass(frozen=True, slots=True)
class PublicCorpusExportSummary:
    jobs: int
    sources: int
    english_projections: int
    english_analyses: int
    original_analyses: int
    capabilities: int
    output_dir: Path


@dataclass(frozen=True, slots=True)
class PublicCorpusVerification:
    ok: bool
    jobs: int
    errors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _CorpusJob:
    source_job_id: str
    source_payload: dict[str, Any]
    english_projection: dict[str, Any] | None
    english_analysis: dict[str, Any] | None
    original_analysis: dict[str, Any] | None
    capability: dict[str, Any] | None
    manifest_entry: dict[str, Any]


def _json_text(payload: object) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(_json_text(payload), encoding="utf-8")
    temporary.replace(path)


def _write_optional(path: Path, payload: dict[str, Any] | None) -> None:
    if payload is None:
        path.unlink(missing_ok=True)
        return
    _atomic_write_json(path, payload)


def _connect(database_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def _source_rows(database_path: Path) -> tuple[sqlite3.Row, ...]:
    JobHunterStore(database_path).initialize()
    with _connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT
                p.id AS job_posting_id,
                p.source_job_id,
                p.company_slug,
                p.canonical_url,
                p.title_observed,
                p.first_seen_at,
                p.last_seen_at,
                p.lifecycle_state,
                v.id AS job_detail_version_id,
                v.fetched_at,
                v.requested_url,
                v.final_url,
                v.status_code,
                v.content_sha256,
                v.semantic_sha256,
                v.parser_version,
                v.parse_status,
                v.fields_json
            FROM job_postings AS p
            LEFT JOIN job_detail_versions AS v
              ON v.id = (
                  SELECT MAX(v2.id)
                  FROM job_detail_versions AS v2
                  WHERE v2.job_posting_id = p.id
              )
            WHERE p.source = 'jobinja'
            ORDER BY p.source_job_id ASC
            """
        ).fetchall()
    return tuple(rows)


def _translation_payload(artifact: TranslationArtifact | None) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "schema_version": PUBLIC_CORPUS_SCHEMA_VERSION,
        "stage": "english_projection",
        "source_job_id": artifact.source_job_id,
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "source_semantic_sha256": artifact.source_semantic_sha256,
        "source_language": artifact.source_language,
        "target_language": artifact.target_language,
        "provider": artifact.provider_name,
        "model": artifact.provider_model,
        "translation_schema_version": artifact.translation_schema_version,
        "translation_sha256": artifact.translation_sha256,
        "translated_segment_count": artifact.translated_segment_count,
        "native_segment_count": artifact.native_segment_count,
        "segment_provenance": artifact.segment_provenance,
        "created_at": artifact.created_at,
        "fields": artifact.fields,
        "english_document": artifact.english_document,
    }


def _analysis_payload(
    artifact: AnalysisArtifact | None,
    *,
    stage: str,
) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "schema_version": PUBLIC_CORPUS_SCHEMA_VERSION,
        "stage": stage,
        "source_job_id": artifact.source_job_id,
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "translation_artifact_id": artifact.translation_artifact_id,
        "model": artifact.model,
        "prompt_version": artifact.prompt_version,
        "analysis_schema_version": artifact.schema_version,
        "created_at": artifact.created_at,
        "semantic_review_status": artifact.semantic_review_status,
        "analysis": artifact.analysis,
    }


def _capability_payload(
    artifact: CapabilityIntelligenceArtifact | None,
) -> dict[str, Any] | None:
    if artifact is None:
        return None
    return {
        "schema_version": PUBLIC_CORPUS_SCHEMA_VERSION,
        "stage": "capability",
        "source_job_id": artifact.source_job_id,
        "artifact_id": artifact.id,
        "job_detail_version_id": artifact.job_detail_version_id,
        "translation_artifact_id": artifact.translation_artifact_id,
        "analysis_artifact_id": artifact.analysis_artifact_id,
        "model": artifact.model,
        "prompt_version": artifact.prompt_version,
        "capability_schema_version": artifact.schema_version,
        "created_at": artifact.created_at,
        "intelligence": artifact.intelligence,
    }


def _build_source_payload(row: sqlite3.Row) -> tuple[dict[str, Any], str]:
    detail_id = row["job_detail_version_id"]
    fields: dict[str, Any] = {}
    if detail_id is not None:
        fields = json.loads(str(row["fields_json"]))
    language = str(fields.get("language") or "unknown")
    detail = None
    if detail_id is not None:
        detail = {
            "job_detail_version_id": int(detail_id),
            "fetched_at": str(row["fetched_at"]),
            "requested_url": str(row["requested_url"]),
            "final_url": str(row["final_url"]),
            "status_code": int(row["status_code"]),
            "content_sha256": str(row["content_sha256"]),
            "semantic_sha256": str(row["semantic_sha256"] or ""),
            "parser_version": str(row["parser_version"]),
            "parse_status": str(row["parse_status"]),
            "fields": fields,
        }
    return (
        {
            "schema_version": PUBLIC_CORPUS_SCHEMA_VERSION,
            "stage": "source",
            "source": "jobinja",
            "source_job_id": str(row["source_job_id"]),
            "company_slug": str(row["company_slug"]),
            "canonical_url": str(row["canonical_url"]),
            "title_observed": row["title_observed"],
            "first_seen_at": str(row["first_seen_at"]),
            "last_seen_at": str(row["last_seen_at"]),
            "lifecycle_state": str(row["lifecycle_state"]),
            "language": language,
            "current_detail": detail,
        },
        language,
    )


def _build_jobs(
    database_path: Path,
    *,
    analysis_model: str | None,
    capability_model: str | None,
) -> tuple[_CorpusJob, ...]:
    if not database_path.exists():
        raise PublicCorpusError(f"JobHunter database does not exist: {database_path}")

    translation_store = TranslationStore(database_path)
    analysis_store = AnalysisStore(database_path)
    capability_store = CapabilityIntelligenceStore(database_path)
    capability_store.initialize()

    jobs: list[_CorpusJob] = []
    for row in _source_rows(database_path):
        source_job_id = str(row["source_job_id"])
        if not _SAFE_JOB_ID_RE.fullmatch(source_job_id):
            raise PublicCorpusError(
                f"source_job_id contains unsupported path characters: {source_job_id!r}"
            )

        source_payload, language = _build_source_payload(row)
        translation = translation_store.latest_artifact(source_job_id, target_language="en")
        english_analysis = analysis_store.latest_current(
            source_job_id,
            model=analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            accepted_only=True,
        )
        original_analysis = analysis_store.latest_current(
            source_job_id,
            model=analysis_model,
            prompt_version=ORIGINAL_PROMPT_VERSION,
            schema_version=ORIGINAL_ANALYSIS_SCHEMA_VERSION,
        )
        capability = capability_store.latest_current(
            source_job_id,
            model=capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if (
            capability is not None
            and (
                english_analysis is None
                or capability.analysis_artifact_id != english_analysis.id
                or capability.translation_artifact_id
                != english_analysis.translation_artifact_id
            )
        ):
            capability = None

        translation_payload = _translation_payload(translation)
        english_analysis_payload = _analysis_payload(
            english_analysis,
            stage="p16_english",
        )
        original_analysis_payload = _analysis_payload(
            original_analysis,
            stage="p16_original",
        )
        capability_payload = _capability_payload(capability)

        detail = source_payload["current_detail"]
        jobs.append(
            _CorpusJob(
                source_job_id=source_job_id,
                source_payload=source_payload,
                english_projection=translation_payload,
                english_analysis=english_analysis_payload,
                original_analysis=original_analysis_payload,
                capability=capability_payload,
                manifest_entry={
                    "source_job_id": source_job_id,
                    "title": (
                        detail["fields"].get("title")
                        if isinstance(detail, dict)
                        else row["title_observed"]
                    ),
                    "company_slug": str(row["company_slug"]),
                    "canonical_url": str(row["canonical_url"]),
                    "lifecycle_state": str(row["lifecycle_state"]),
                    "language": language,
                    "job_detail_version_id": (
                        int(row["job_detail_version_id"])
                        if row["job_detail_version_id"] is not None
                        else None
                    ),
                    "parse_status": (
                        str(row["parse_status"])
                        if row["parse_status"] is not None
                        else None
                    ),
                    "semantic_sha256": (
                        str(row["semantic_sha256"])
                        if row["semantic_sha256"] is not None
                        else None
                    ),
                    "stages": {
                        "source": True,
                        "english_projection": translation_payload is not None,
                        "p16_english": english_analysis_payload is not None,
                        "p16_original": original_analysis_payload is not None,
                        "capability": capability_payload is not None,
                    },
                    "artifact_ids": {
                        "english_projection": translation.id if translation else None,
                        "p16_english": english_analysis.id if english_analysis else None,
                        "p16_original": original_analysis.id if original_analysis else None,
                        "capability": capability.id if capability else None,
                    },
                },
            )
        )
    return tuple(jobs)


def _manifest(jobs: tuple[_CorpusJob, ...]) -> dict[str, Any]:
    return {
        "schema_version": PUBLIC_CORPUS_SCHEMA_VERSION,
        "contracts": {
            "p16_english": {
                "prompt_version": ENGLISH_PROMPT_VERSION,
                "schema_version": ENGLISH_ANALYSIS_SCHEMA_VERSION,
            },
            "p16_original": {
                "prompt_version": ORIGINAL_PROMPT_VERSION,
                "schema_version": ORIGINAL_ANALYSIS_SCHEMA_VERSION,
            },
            "capability": {
                "prompt_version": CAPABILITY_PROMPT_VERSION,
                "schema_version": CAPABILITY_SCHEMA_VERSION,
            },
        },
        "counts": {
            "jobs": len(jobs),
            "sources": len(jobs),
            "english_projections": sum(job.english_projection is not None for job in jobs),
            "p16_english": sum(job.english_analysis is not None for job in jobs),
            "p16_original": sum(job.original_analysis is not None for job in jobs),
            "capabilities": sum(job.capability is not None for job in jobs),
        },
        "jobs": [job.manifest_entry for job in jobs],
    }


def _write_job(output_dir: Path, job: _CorpusJob) -> None:
    job_dir = output_dir / "jobs" / job.source_job_id
    _atomic_write_json(job_dir / "source.json", job.source_payload)
    _write_optional(job_dir / "english-projection.json", job.english_projection)
    _write_optional(job_dir / "p16-english.json", job.english_analysis)
    _write_optional(job_dir / "p16-original.json", job.original_analysis)
    _write_optional(job_dir / "capability.json", job.capability)


def export_public_corpus(
    database_path: Path,
    *,
    output_dir: Path = DEFAULT_PUBLIC_CORPUS_DIR,
    analysis_model: str | None = None,
    capability_model: str | None = None,
    prune: bool = True,
) -> PublicCorpusExportSummary:
    """Export the complete current public job corpus from durable SQLite state."""

    jobs = _build_jobs(
        database_path,
        analysis_model=analysis_model,
        capability_model=capability_model,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    jobs_dir = output_dir / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)

    for job in jobs:
        _write_job(output_dir, job)

    if prune:
        known = {job.source_job_id for job in jobs}
        for child in jobs_dir.iterdir():
            if child.is_dir() and child.name not in known:
                shutil.rmtree(child)

    _atomic_write_json(output_dir / "manifest.json", _manifest(jobs))
    return PublicCorpusExportSummary(
        jobs=len(jobs),
        sources=len(jobs),
        english_projections=sum(job.english_projection is not None for job in jobs),
        english_analyses=sum(job.english_analysis is not None for job in jobs),
        original_analyses=sum(job.original_analysis is not None for job in jobs),
        capabilities=sum(job.capability is not None for job in jobs),
        output_dir=output_dir,
    )


def export_public_job(
    database_path: Path,
    source_job_id: str,
    *,
    output_dir: Path = DEFAULT_PUBLIC_CORPUS_DIR,
    analysis_model: str | None = None,
    capability_model: str | None = None,
) -> None:
    """Refresh one job projection and the complete manifest after a durable operation."""

    jobs = _build_jobs(
        database_path,
        analysis_model=analysis_model,
        capability_model=capability_model,
    )
    selected = next((job for job in jobs if job.source_job_id == source_job_id), None)
    if selected is None:
        raise PublicCorpusError(f"Unknown Jobinja job ID: {source_job_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_job(output_dir, selected)
    _atomic_write_json(output_dir / "manifest.json", _manifest(jobs))


def verify_public_corpus(
    database_path: Path,
    *,
    output_dir: Path = DEFAULT_PUBLIC_CORPUS_DIR,
    analysis_model: str | None = None,
    capability_model: str | None = None,
) -> PublicCorpusVerification:
    """Verify that repository JSON exactly matches current durable public state."""

    jobs = _build_jobs(
        database_path,
        analysis_model=analysis_model,
        capability_model=capability_model,
    )
    errors: list[str] = []

    expected_manifest = _manifest(jobs)
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append("manifest.json is missing")
    else:
        try:
            actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"manifest.json is unreadable: {exc}")
        else:
            if actual_manifest != expected_manifest:
                errors.append("manifest.json does not match current SQLite state")

    expected_names = {job.source_job_id for job in jobs}
    jobs_dir = output_dir / "jobs"
    actual_names = (
        {item.name for item in jobs_dir.iterdir() if item.is_dir()}
        if jobs_dir.exists()
        else set()
    )
    for stale in sorted(actual_names - expected_names):
        errors.append(f"stale corpus job directory: {stale}")

    for job in jobs:
        job_dir = jobs_dir / job.source_job_id
        expected_files: dict[str, dict[str, Any] | None] = {
            "source.json": job.source_payload,
            "english-projection.json": job.english_projection,
            "p16-english.json": job.english_analysis,
            "p16-original.json": job.original_analysis,
            "capability.json": job.capability,
        }
        for filename, expected in expected_files.items():
            path = job_dir / filename
            if expected is None:
                if path.exists():
                    errors.append(f"{job.source_job_id}/{filename} is stale")
                continue
            if not path.exists():
                errors.append(f"{job.source_job_id}/{filename} is missing")
                continue
            try:
                actual = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{job.source_job_id}/{filename} is unreadable: {exc}")
                continue
            if actual != expected:
                errors.append(f"{job.source_job_id}/{filename} differs from SQLite state")

    return PublicCorpusVerification(
        ok=not errors,
        jobs=len(jobs),
        errors=tuple(errors),
    )
