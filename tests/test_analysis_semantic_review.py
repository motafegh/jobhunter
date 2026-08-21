from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.analysis_store import (
    SEMANTIC_REVIEW_ACCEPTED,
    SEMANTIC_REVIEW_PENDING,
    AnalysisStore,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def _seed_dependencies(database_path: Path) -> tuple[int, int]:
    now = datetime(2026, 8, 21, tzinfo=UTC)
    source = JobHunterStore(database_path)
    source.initialize()
    posting = source.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="review1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/review1/example",
            observed_text="Python Developer",
        ),
        observed_at=now,
    )
    detail = source.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/acme/jobs/review1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/review1/example",
        status_code=200,
        content_sha256="raw-review1",
        semantic_sha256="semantic-review1",
        evidence_path=Path("review1.html"),
        metadata_path=Path("review1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Python Developer",
            "description": "Mastery of Python is required.",
            "skills": ["Python"],
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job("review1")
    return detail.version_id, translation.artifact_id


def _record_pending(database_path: Path, detail_id: int, translation_id: int) -> int:
    return AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        analysis={"requirements": [{"concept": "Python"}]},
        request_body={"local": "request"},
        raw_response={"local": "response"},
        created_at=datetime(2026, 8, 21, 1, tzinfo=UTC),
        semantic_review_status=SEMANTIC_REVIEW_PENDING,
    )


def test_pending_analysis_is_hidden_until_explicit_acceptance(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    detail_id, translation_id = _seed_dependencies(database_path)
    artifact_id = _record_pending(database_path, detail_id, translation_id)
    store = AnalysisStore(database_path)

    assert store.latest_current("review1").semantic_review_status == SEMANTIC_REVIEW_PENDING
    assert store.latest_current("review1", accepted_only=True) is None
    assert store.list_current(accepted_only=True) == ()

    result = store.review_current(
        "review1",
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        disposition="accepted",
        reviewed_at=datetime(2026, 8, 21, 2, tzinfo=UTC),
        note="Complete source and depth review passed",
    )

    accepted = store.latest_current("review1", accepted_only=True)
    assert result.artifact_id == artifact_id
    assert accepted is not None
    assert accepted.semantic_review_status == SEMANTIC_REVIEW_ACCEPTED
    assert accepted.semantic_review_note == "Complete source and depth review passed"


def test_rejection_archives_candidate_and_allows_clean_rebuild(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    detail_id, translation_id = _seed_dependencies(database_path)
    artifact_id = _record_pending(database_path, detail_id, translation_id)
    store = AnalysisStore(database_path)
    store.record_attempt(
        job_detail_version_id=detail_id,
        attempted_at=datetime(2026, 8, 21, 1, tzinfo=UTC),
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        outcome="completed",
        artifact_id=artifact_id,
    )

    result = store.review_current(
        "review1",
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        disposition="rejected",
        reviewed_at=datetime(2026, 8, 21, 2, tzinfo=UTC),
        note="Depth was spread across unrelated technologies",
    )

    assert result.disposition == "rejected"
    assert store.latest_current("review1") is None
    with sqlite3.connect(database_path) as connection:
        archived = connection.execute(
            "SELECT original_artifact_id, rejection_note "
            "FROM job_analysis_rejected_artifacts"
        ).fetchone()
        attempt_artifact_id = connection.execute(
            "SELECT artifact_id FROM job_analysis_attempts"
        ).fetchone()[0]
    assert archived == (artifact_id, "Depth was spread across unrelated technologies")
    assert attempt_artifact_id is None
    assert _record_pending(database_path, detail_id, translation_id) > artifact_id


def test_rejection_is_blocked_after_capability_consumes_analysis(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    detail_id, translation_id = _seed_dependencies(database_path)
    artifact_id = _record_pending(database_path, detail_id, translation_id)
    CapabilityIntelligenceStore(database_path).record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=artifact_id,
        model="capability-model",
        prompt_version="job-capability-intelligence-v9",
        schema_version="job-capability-intelligence-v5",
        intelligence={},
        request_body={},
        raw_response={},
        created_at=datetime(2026, 8, 21, 2, tzinfo=UTC),
    )

    with pytest.raises(ValueError, match="durable Capability downstream"):
        AnalysisStore(database_path).review_current(
            "review1",
            model="analysis-model",
            prompt_version="job-analysis-english-v20",
            schema_version="job-analysis-v5",
            disposition="rejected",
            reviewed_at=datetime(2026, 8, 21, 3, tzinfo=UTC),
            note="Attempted review reversal after downstream use",
        )
