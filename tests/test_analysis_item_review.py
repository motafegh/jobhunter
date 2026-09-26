"""Item review never replaces original claims or bypasses artifact acceptance."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.analysis_item_review import AnalysisItemReviewStore
from jobhunter.analysis_store import AnalysisStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def _candidate(tmp_path: Path) -> tuple[Path, int, int]:
    database = tmp_path / "jobhunter.sqlite3"
    now = datetime(2026, 9, 24, tzinfo=UTC)
    source = JobHunterStore(database)
    source.initialize()
    posting = source.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="review-b", company_slug="example",
            canonical_url="https://jobinja.ir/companies/example/jobs/review-b/example",
            observed_text="Python Developer",
        ),
        observed_at=now,
    )
    detail = source.record_job_detail(
        job_posting_id=posting.job_posting_id, fetched_at=now,
        requested_url="https://jobinja.ir/companies/example/jobs/review-b/example",
        final_url="https://jobinja.ir/companies/example/jobs/review-b/example",
        status_code=200, content_sha256="content-review-b",
        semantic_sha256="semantic-review-b", evidence_path=Path("review-b.html"),
        metadata_path=Path("review-b.json"), parser_version="jobinja-detail-v2",
        parse_status="parsed", fields={
            "title": "Python Developer",
            "description": "Mastery of Python is required. Agent demo is a plus.",
            "skills": ["Python"], "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    translation = TranslationService(store=TranslationStore(database), provider=None)
    result = translation.translate_job("review-b")
    analysis_id = AnalysisStore(database).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=result.artifact_id, model="model",
        prompt_version="job-analysis-english-v23", schema_version="job-analysis-v5",
        analysis={
            "role_purpose": [], "responsibilities": [],
            "requirements": [{
                "concept": "Python", "evidence": "Mastery of Python is required.",
                "requirement_type": "required", "concept_type": "skill",
                "confidence": "high", "depth_signal": "Mastery",
            }],
        },
        request_body={"placeholder": True}, raw_response={"placeholder": True},
        created_at=now, semantic_review_status="pending",
    )
    return database, analysis_id, result.artifact_id


def _accept(database: Path, projection_id: int) -> None:
    AnalysisStore(database).review_current(
        "review-b", model="model", prompt_version="job-analysis-english-v23",
        schema_version="job-analysis-v5", translation_artifact_id=projection_id,
        require_translation_dependency=True, disposition="accepted",
        reviewed_at=datetime(2026, 9, 24, tzinfo=UTC),
        note="Source evidence reviewed and complete",
    )


def test_started_review_blocks_existing_artifact_acceptance(tmp_path):
    database, artifact_id, projection_id = _candidate(tmp_path)
    review = AnalysisItemReviewStore(database)
    review.begin(artifact_id)
    with pytest.raises(sqlite3.IntegrityError, match="Finish item review"):
        _accept(database, projection_id)
    assert AnalysisStore(database).artifact_by_id(artifact_id).semantic_review_status == "pending"
    with pytest.raises(ValueError, match="Every original claim"):
        review.complete(artifact_id, note="All claims were checked")
    review.review_item(
        artifact_id, kind="requirements", index=0, finding="supported",
        note="Python requirement is exact source evidence",
    )
    review.complete(artifact_id, note="All original claims and source coverage checked")
    assert review.is_complete(artifact_id)
    _accept(database, projection_id)
    assert AnalysisStore(database).artifact_by_id(artifact_id).semantic_review_status == "accepted"
    with pytest.raises(ValueError, match="pending"):
        review.review_item(
            artifact_id, kind="requirements", index=0, finding="unsupported",
            note="Later unauthorized review change",
        )


def test_material_issue_and_source_gap_reopen_and_block_acceptance(tmp_path):
    database, artifact_id, projection_id = _candidate(tmp_path)
    review = AnalysisItemReviewStore(database)
    review.review_item(
        artifact_id, kind="requirements", index=0, finding="needs_clarification",
        note="The claim might borrow another depth marker",
        proposed_text="Source-supported narrower claim",
    )
    with pytest.raises(ValueError, match="Material"):
        review.complete(artifact_id, note="Incomplete review with unresolved meaning")
    with pytest.raises(sqlite3.IntegrityError, match="Finish item review"):
        _accept(database, projection_id)
    review.review_item(
        artifact_id, kind="requirements", index=0, finding="supported",
        note="The original Python source is exact after manual recheck",
    )
    review.complete(artifact_id, note="Original claim checked against exact evidence")
    review.review_gap(
        artifact_id, source_excerpt="Agent demo is a plus.",
        finding="gap_open", note="Preferred demonstration is missing from extraction",
        proposed_text="Preferred agent demonstration project",
    )
    assert not review.is_complete(artifact_id)
    with pytest.raises(ValueError, match="Material"):
        review.complete(artifact_id, note="Still missing source coverage")
    with pytest.raises(ValueError, match="exact current English"):
        review.review_gap(
            artifact_id, source_excerpt="Invented evidence not in the source",
            finding="gap_open", note="An invented demonstration requirement",
        )
    review.review_gap(
        artifact_id, source_excerpt="Agent demo is a plus.",
        finding="gap_dismissed", note="Gap flagged in error after source recheck",
    )
    review.complete(artifact_id, note="All remaining source coverage reviewed")
    _accept(database, projection_id)
    artifact = AnalysisStore(database).artifact_by_id(artifact_id)
    assert artifact.analysis["requirements"][0]["concept"] == "Python"
    assert len(review.events(artifact_id)) == 4
    assert review.events(artifact_id)[0].proposed_text == "Source-supported narrower claim"


def test_rejected_candidate_keeps_review_history_and_legacy_gate(tmp_path):
    database, artifact_id, projection_id = _candidate(tmp_path)
    review = AnalysisItemReviewStore(database)
    review.review_item(
        artifact_id, kind="requirements", index=0, finding="unsupported",
        note="Employer source evidence does not establish this claim",
    )
    AnalysisStore(database).review_current(
        "review-b", model="model", prompt_version="job-analysis-english-v23",
        schema_version="job-analysis-v5", translation_artifact_id=projection_id,
        require_translation_dependency=True, disposition="rejected",
        reviewed_at=datetime(2026, 9, 24, tzinfo=UTC),
        note="Material semantic error remains unresolved",
    )
    assert AnalysisStore(database).artifact_by_id(artifact_id) is None
    assert len(review.events(artifact_id)) == 1
    with sqlite3.connect(database) as connection:
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_old_pending_candidate_without_review_session_keeps_existing_behavior(tmp_path):
    database, artifact_id, projection_id = _candidate(tmp_path)
    AnalysisItemReviewStore(database).initialize()
    _accept(database, projection_id)
    assert AnalysisStore(database).artifact_by_id(artifact_id).semantic_review_status == "accepted"
