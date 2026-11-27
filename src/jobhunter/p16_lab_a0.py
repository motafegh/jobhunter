"""A0 offline adapter: original V30 service, private state and exact frozen L0 input.

This is a research adapter, not a production route or live experiment runner.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_failure_diagnostics import AnalysisFailureDiagnosticStore
from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
from jobhunter.analysis_store import AnalysisStore
from jobhunter.p16_lab import OfflineRun, checked_path, digest, file_digest, load_requirements
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

PRIVATE_SOURCES = (
    "data/local-acceptance/p16-evolution-e1-2026-11-24/PRIVATE_E2_3_SOURCE_SELECTION.json"
)


class FreshAnalysisStore(AnalysisStore):
    """Use incumbent persistence; explicitly disallow historical analysis cache reuse.

    After the one new write, only its exact artifact may satisfy the service readback.
    """

    def __init__(self, database: Path):
        super().__init__(database)
        self.written_id: int | None = None
        self.cache_bypasses = 0

    def find_artifact(self, **kwargs):
        if self.written_id is None:
            self.cache_bypasses += 1
            return None
        artifact = self.artifact_by_id(self.written_id)
        if (
            artifact is None
            or artifact.semantic_review_status != "pending"
            or not kwargs.get("require_translation_dependency")
            or any(
                getattr(artifact, key) != kwargs[key]
                for key in (
                    "job_detail_version_id",
                    "translation_artifact_id",
                    "model",
                    "prompt_version",
                    "schema_version",
                )
            )
        ):
            raise ValueError("fresh artifact readback mismatch")
        return artifact

    def record_artifact(self, **kwargs):
        if self.written_id is not None or kwargs.get("semantic_review_status") != "pending":
            raise ValueError("invalid research artifact write")
        self.written_id = super().record_artifact(**kwargs)
        return self.written_id


class FrozenProjection:
    """Read only the exact frozen, associated English projection; no translation provider."""

    def __init__(self, store: TranslationStore, expected: dict):
        self.store, self.expected = store, expected

    def current_artifact(self, source_job_id):
        a = self.store.artifact_by_id(self.expected["translation_id"])
        s = self.store.latest_source_version(source_job_id)
        if (
            a is None
            or s is None
            or a.source_job_id != source_job_id
            or a.job_detail_version_id != s.job_detail_version_id
            or s.job_detail_version_id != self.expected["source_version"]
            or a.source_semantic_sha256 != s.semantic_sha256
            or s.semantic_sha256 != self.expected["source_semantic_sha256"]
            or a.translation_sha256 != self.expected["translation_sha256"]
            or a.provider_model != self.expected["translation_model"]
            or a.translation_schema_version != "english-projection-v2"
            or a.target_language != "en"
        ):
            raise ValueError("frozen projection association mismatch")
        return a


def prepare_retained_d1(run: OfflineRun):
    """Fixed first A0 cell, using pinned source and retained original completion bytes."""
    freeze, _ = load_requirements(run.root)
    selection = checked_path(run.root, PRIVATE_SOURCES)
    if file_digest(selection) != freeze["private_source_manifest_sha256"]:
        raise ValueError("source selection digest mismatch")
    rows = json.loads(selection.read_bytes())["sources"]
    selected = [s for s in rows if s["source_group"] == "nov23" and s["source_version"] == 1]
    if len(selected) != 1 or selected[0]["case"] != "tdIF":
        raise ValueError("unexpected retained D1 identity")
    expected = selected[0]
    frozen = run.clone_snapshot("nov23")
    database = checked_path(run.path, "working.sqlite3")
    with frozen.open("rb") as src, database.open("xb") as dst:
        shutil.copyfileobj(src, dst)
    if file_digest(database) != run.snapshot_hashes["nov23"]:
        raise ValueError("working copy digest mismatch")
    with closing(sqlite3.connect(frozen.as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        records = db.execute(
            """SELECT d.completion_text FROM job_analysis_failure_diagnostics d
               JOIN job_analysis_attempts a ON a.id=d.attempt_id
               WHERE a.job_detail_version_id=? AND a.model=?
                 AND a.prompt_version='job-analysis-english-v30' AND a.outcome='failed'
               ORDER BY d.id""",
            (expected["source_version"], run.models["M0"]),
        ).fetchall()
    replies = [row[0] for row in records]
    if len(replies) != 2 or not all(
        isinstance(r, str) and isinstance(json.loads(r), dict) for r in replies
    ):
        raise ValueError("unexpected retained response inventory")
    store = TranslationStore(database)
    a = store.artifact_by_id(expected["translation_id"])
    if a is None or a.source_job_id != expected["case"]:
        raise ValueError("retained translation missing")
    source = store.latest_source_version(a.source_job_id)
    if (
        source is None
        or digest(source.fields["description"].encode()) != expected["original_description_sha256"]
    ):
        raise ValueError("source description mismatch")
    projection = FrozenProjection(store, expected)
    projection.current_artifact(a.source_job_id)
    run.event(
        "a0_input_bound",
        case="D1",
        source_version=expected["source_version"],
        translation_id=expected["translation_id"],
        source_semantic_sha256=expected["source_semantic_sha256"],
        translation_sha256=expected["translation_sha256"],
        completion_sha256=[digest(r.encode()) for r in replies],
        offline_replay=True,
    )
    return database, a.source_job_id, projection, replies


def prepare_synthetic(run: OfflineRun):
    """A separate synthetic positive persistence test, never a frozen D1 result."""
    database = checked_path(run.path, "working.sqlite3")
    source_store = JobHunterStore(database)
    source_store.initialize()
    now = datetime.now(UTC)
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="lab-synthetic",
            company_slug="synthetic",
            canonical_url="https://example.invalid/job/lab-synthetic",
            observed_text="Synthetic role",
        ),
        observed_at=now,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://example.invalid/job/lab-synthetic",
        final_url="https://example.invalid/job/lab-synthetic",
        status_code=200,
        content_sha256="synthetic-content",
        semantic_sha256="synthetic-semantic",
        evidence_path=Path("synthetic.html"),
        metadata_path=Path("synthetic.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={"title": "Synthetic role", "language": "en", "parser_version": "jobinja-detail-v2"},
    )
    t = TranslationService(store=TranslationStore(database), provider=None)
    a = t.translate_job("lab-synthetic")
    # Prove an incumbent-compatible historical record exists yet cannot be reused.
    old_id = AnalysisStore(database).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=a.artifact_id,
        model=run.models["M0"],
        prompt_version="job-analysis-english-v28",
        schema_version="job-analysis-v5",
        analysis={"requirements": [], "responsibilities": []},
        request_body={"synthetic": True},
        raw_response={"synthetic": True},
        created_at=now,
        semantic_review_status="accepted",
    )
    run.event("synthetic_history_created", artifact_id=old_id)
    return database, "lab-synthetic", t, []


def analyze_fresh(run: OfflineRun, database: Path, source_job_id: str, projection, provider):
    if database != checked_path(run.path, "working.sqlite3"):
        raise ValueError("unapproved research database")
    store = FreshAnalysisStore(database)
    service = JobAnalysisServiceV30(
        source_store=TranslationStore(database),
        translation_service=projection,
        analysis_store=store,
        diagnostic_store=AnalysisFailureDiagnosticStore(database),
        provider=provider,
        model=run.models["M0"],
        max_tokens=8192,
    )
    result = service.analyze_english_job(source_job_id)
    if (
        result.outcome != "completed"
        or result.artifact_id != store.written_id
        or result.semantic_review_status != "pending"
        or store.cache_bypasses != 1
    ):
        run.stop("a0_not_fresh_pending")
    return result
