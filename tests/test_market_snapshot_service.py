import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.market_affected_work import MarketAffectedWorkPlanner
from jobhunter.market_membership_models import MARKET_MEMBERSHIP_CONTRACT_VERSION
from jobhunter.market_models import MarketDefinitionSpec
from jobhunter.market_snapshot_service import MarketSnapshotError, MarketSnapshotService
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 17, 12, tzinfo=UTC)
_MODEL = "analysis-model"


class Harness:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.now = _NOW
        self.source = JobHunterStore(database_path)
        self.source.initialize()
        self.market = MarketStore(database_path)
        self.translations = TranslationStore(database_path)
        self.analyses = AnalysisStore(database_path)
        self.translation_service = TranslationService(
            store=self.translations,
            provider=None,
            clock=lambda: self.now,
        )
        target = self.market.create_target(
            slug="applied-ai",
            name="Applied AI / ML Engineering",
            description=None,
            created_at=self.now,
        )
        self.definition = self.market.create_definition_version(
            target.id,
            spec=MarketDefinitionSpec(
                membership_intent=(
                    "Applied AI / ML engineering; backend infrastructure is adjacent."
                ),
                search_catalog_version="fixture-v1",
                search_profiles=("ai-focused",),
            ),
            created_at=self.now,
        )

    def seed_source(self, job_id: str, *, version: int = 1) -> tuple[int, int]:
        posting = self.source.upsert_job(
            job=DiscoveredJobLink(
                source_job_id=job_id,
                company_slug="fixture",
                canonical_url=f"https://jobinja.ir/companies/fixture/jobs/{job_id}/role",
                observed_text="Applied AI Engineer",
            ),
            observed_at=self.now,
        )
        detail = self.source.record_job_detail(
            job_posting_id=posting.job_posting_id,
            fetched_at=self.now,
            requested_url=f"https://jobinja.ir/jobs/{job_id}",
            final_url=f"https://jobinja.ir/jobs/{job_id}",
            status_code=200,
            content_sha256=f"raw-{job_id}-{version}",
            semantic_sha256=f"semantic-{job_id}-{version}",
            evidence_path=Path(f"{job_id}-{version}.html"),
            metadata_path=Path(f"{job_id}-{version}.json"),
            parser_version="jobinja-detail-v2",
            parse_status="parsed",
            fields={
                "title": "Applied AI Engineer",
                "description": "Build production AI systems.",
                "language": "en",
            },
        )
        translation = self.translation_service.translate_job(job_id)
        return detail.version_id, translation.artifact_id

    def analysis(
        self,
        detail_id: int,
        translation_id: int,
        *,
        review_status: str,
        created_at: datetime | None = None,
    ) -> int:
        return self.analyses.record_artifact(
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            model=_MODEL,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            analysis={
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [],
            },
            request_body={},
            raw_response={},
            created_at=created_at or self.now,
            semantic_review_status=review_status,
        )

    def membership(
        self,
        detail_id: int,
        *,
        disposition: str,
        translation_id: int | None,
        analysis_id: int | None = None,
        identity: str = "fixture-model",
        method: str = "model",
        supersedes: int | None = None,
    ):
        return self.market.record_membership(
            target_definition_version_id=self.definition.id,
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            analysis_artifact_id=analysis_id,
            classifier_contract_version=MARKET_MEMBERSHIP_CONTRACT_VERSION,
            classifier_method=method,
            classifier_identity={"provider": "fixture", "model": identity},
            disposition=disposition,
            reason="Evidence-backed target-relative fixture decision.",
            evidence_refs=("source:description",),
            confidence="high",
            supersedes_membership_id=supersedes,
            created_at=self.now,
        )

    def planner(self) -> MarketAffectedWorkPlanner:
        return MarketAffectedWorkPlanner(
            market_store=self.market,
            source_store=self.source,
            observations=JobDetailObservationStore(self.database_path),
            translation_store=self.translations,
            translation_service=self.translation_service,
            analysis_store=self.analyses,
            analysis_model=_MODEL,
            clock=lambda: self.now,
        )

    def service(self) -> MarketSnapshotService:
        return MarketSnapshotService(
            database_path=self.database_path,
            market_store=self.market,
            planner=self.planner(),
            translation_store=self.translations,
            analysis_model=_MODEL,
            clock=lambda: self.now,
        )

    def completed_run(self, *, failures: bool = False):
        run = self.market.start_run(
            self.definition.id,
            controls={"fixture": True},
            started_at=self.now,
        )
        return self.market.finish_run(
            run.id,
            status="completed_with_failures" if failures else "completed",
            ledger={"fixture": {"failed": int(failures)}},
            completed_at=self.now,
            error_summary="fixture failure" if failures else None,
        )


@pytest.fixture
def h(tmp_path: Path) -> Harness:
    return Harness(tmp_path / "jobhunter.sqlite3")


def test_snapshot_freezes_dispositions_and_all_semantic_coverage_states(h: Harness) -> None:
    membership_ids = []

    accepted_detail, accepted_translation = h.seed_source("accepted")
    accepted_analysis = h.analysis(
        accepted_detail,
        accepted_translation,
        review_status="accepted",
    )
    membership_ids.append(
        h.membership(
            accepted_detail,
            disposition="core_match",
            translation_id=accepted_translation,
            analysis_id=accepted_analysis,
        ).id
    )

    pending_detail, pending_translation = h.seed_source("pending")
    h.analysis(pending_detail, pending_translation, review_status="pending")
    membership_ids.append(
        h.membership(
            pending_detail,
            disposition="core_match",
            translation_id=pending_translation,
        ).id
    )

    missing_detail, missing_translation = h.seed_source("missing")
    membership_ids.append(
        h.membership(
            missing_detail,
            disposition="core_match",
            translation_id=missing_translation,
        ).id
    )

    rejected_detail, rejected_translation = h.seed_source("rejected")
    h.analysis(rejected_detail, rejected_translation, review_status="pending")
    h.analyses.review_current(
        "rejected",
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        disposition="rejected",
        reviewed_at=h.now + timedelta(minutes=2),
        note="Rejected fixture semantic artifact.",
        translation_artifact_id=rejected_translation,
        require_translation_dependency=True,
    )
    membership_ids.append(
        h.membership(
            rejected_detail,
            disposition="adjacent_match",
            translation_id=rejected_translation,
        ).id
    )

    failed_detail, failed_translation = h.seed_source("failed")
    h.analyses.record_attempt(
        job_detail_version_id=failed_detail,
        attempted_at=h.now + timedelta(minutes=3),
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        outcome="failed",
        error=RuntimeError("fixture generation failure"),
    )
    membership_ids.append(
        h.membership(
            failed_detail,
            disposition="excluded",
            translation_id=failed_translation,
        ).id
    )

    run = h.completed_run(failures=True)
    result = h.service().build_snapshot(
        run_id=run.id,
        membership_ids=tuple(membership_ids),
    )
    by_job = {item.source_job_id: item for item in result.members}

    assert by_job["accepted"].semantic_coverage_status == "accepted"
    assert by_job["accepted"].included_in_primary_corpus is True
    assert by_job["pending"].semantic_coverage_status == "pending"
    assert by_job["pending"].included_in_primary_corpus is True
    assert by_job["missing"].semantic_coverage_status == "missing"
    assert by_job["missing"].included_in_primary_corpus is True
    assert by_job["rejected"].semantic_coverage_status == "rejected"
    assert by_job["rejected"].included_in_primary_corpus is False
    assert by_job["failed"].semantic_coverage_status == "failed"
    assert by_job["failed"].included_in_primary_corpus is False

    metadata = result.snapshot.metadata
    assert metadata["primary_core_postings"] == 3
    assert metadata["accepted_semantic_core_postings"] == 1
    assert metadata["core_semantic_coverage"] == {
        "accepted": 1,
        "pending": 1,
        "missing": 1,
        "failed": 0,
        "rejected": 0,
    }
    assert metadata["repost_adjustment"] == "not_implemented"
    assert metadata["denominator_language"] == "qualified source postings"


def test_snapshot_rejects_superseded_membership(h: Harness) -> None:
    detail, translation = h.seed_source("corrected")
    original = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
    )
    corrected = h.membership(
        detail,
        disposition="adjacent_match",
        translation_id=translation,
        supersedes=original.id,
    )
    run = h.completed_run()

    with pytest.raises(MarketSnapshotError, match="superseded"):
        h.service().build_snapshot(run_id=run.id, membership_ids=(original.id,))

    result = h.service().build_snapshot(run_id=run.id, membership_ids=(corrected.id,))
    assert result.members[0].membership_id == corrected.id
    assert result.members[0].disposition == "adjacent_match"


def test_snapshot_rejects_membership_from_stale_source_version(h: Harness) -> None:
    first_detail, first_translation = h.seed_source("changing", version=1)
    old = h.membership(
        first_detail,
        disposition="core_match",
        translation_id=first_translation,
    )
    h.now += timedelta(minutes=1)
    h.seed_source("changing", version=2)
    run = h.completed_run()

    with pytest.raises(MarketSnapshotError, match="stale source version"):
        h.service().build_snapshot(run_id=run.id, membership_ids=(old.id,))


def test_model_membership_must_consume_newly_accepted_current_p16(h: Harness) -> None:
    detail, translation = h.seed_source("enriched")
    old = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
    )
    analysis = h.analysis(detail, translation, review_status="accepted")
    run = h.completed_run()

    with pytest.raises(MarketSnapshotError, match="current accepted P1.6"):
        h.service().build_snapshot(run_id=run.id, membership_ids=(old.id,))

    current = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
        analysis_id=analysis,
        identity="fixture-model-with-p16",
    )
    second_run = h.completed_run()
    result = h.service().build_snapshot(
        run_id=second_run.id,
        membership_ids=(current.id,),
    )
    assert result.members[0].analysis_artifact_id == analysis
    assert result.members[0].semantic_coverage_status == "accepted"


def test_deterministic_source_only_membership_does_not_gain_derived_dependencies(
    h: Harness,
) -> None:
    detail, translation = h.seed_source("deterministic")
    analysis = h.analysis(detail, translation, review_status="accepted")
    membership = h.membership(
        detail,
        disposition="excluded",
        translation_id=None,
        analysis_id=None,
        method="deterministic",
    )
    run = h.completed_run()

    result = h.service().build_snapshot(run_id=run.id, membership_ids=(membership.id,))
    item = result.members[0]
    assert item.membership_id == membership.id
    assert item.translation_artifact_id == translation
    assert item.analysis_artifact_id == analysis
    assert item.semantic_coverage_status == "accepted"


def test_snapshot_requires_terminal_nonfailed_run(h: Harness) -> None:
    detail, translation = h.seed_source("run-state")
    membership = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
    )
    running = h.market.start_run(
        h.definition.id,
        controls={},
        started_at=h.now,
    )
    with pytest.raises(MarketSnapshotError, match="completed"):
        h.service().build_snapshot(run_id=running.id, membership_ids=(membership.id,))

    failed = h.market.start_run(h.definition.id, controls={}, started_at=h.now)
    h.market.finish_run(
        failed.id,
        status="failed",
        ledger={"failed": 1},
        completed_at=h.now,
        error_summary="terminal fixture failure",
    )
    with pytest.raises(MarketSnapshotError, match="completed"):
        h.service().build_snapshot(run_id=failed.id, membership_ids=(membership.id,))


def test_snapshot_rejects_two_memberships_for_same_source(h: Harness) -> None:
    detail, translation = h.seed_source("duplicate")
    first = h.membership(
        detail,
        disposition="core_match",
        translation_id=translation,
        identity="model-a",
    )
    second = h.membership(
        detail,
        disposition="adjacent_match",
        translation_id=translation,
        identity="model-b",
    )
    run = h.completed_run()

    with pytest.raises(MarketSnapshotError, match="at most one membership"):
        h.service().build_snapshot(
            run_id=run.id,
            membership_ids=(first.id, second.id),
        )


def test_latest_failed_or_rejected_processing_event_controls_coverage(h: Harness) -> None:
    failed_latest_detail, failed_latest_translation = h.seed_source("failed-latest")
    artifact = h.analysis(
        failed_latest_detail,
        failed_latest_translation,
        review_status="pending",
    )
    h.analyses.review_current(
        "failed-latest",
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        disposition="rejected",
        reviewed_at=h.now + timedelta(minutes=1),
        note="Rejected before later failed retry.",
        translation_artifact_id=failed_latest_translation,
        require_translation_dependency=True,
    )
    assert h.analyses.artifact_by_id(artifact) is None
    h.analyses.record_attempt(
        job_detail_version_id=failed_latest_detail,
        attempted_at=h.now + timedelta(minutes=2),
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        outcome="failed",
        error=RuntimeError("later retry failed"),
    )
    failed_latest = h.membership(
        failed_latest_detail,
        disposition="core_match",
        translation_id=failed_latest_translation,
    )

    rejected_latest_detail, rejected_latest_translation = h.seed_source("rejected-latest")
    h.analyses.record_attempt(
        job_detail_version_id=rejected_latest_detail,
        attempted_at=h.now + timedelta(minutes=1),
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        outcome="failed",
        error=RuntimeError("earlier retry failed"),
    )
    h.analysis(
        rejected_latest_detail,
        rejected_latest_translation,
        review_status="pending",
        created_at=h.now + timedelta(minutes=2),
    )
    h.analyses.review_current(
        "rejected-latest",
        model=_MODEL,
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        disposition="rejected",
        reviewed_at=h.now + timedelta(minutes=3),
        note="Later reviewed rejection wins.",
        translation_artifact_id=rejected_latest_translation,
        require_translation_dependency=True,
    )
    rejected_latest = h.membership(
        rejected_latest_detail,
        disposition="core_match",
        translation_id=rejected_latest_translation,
    )

    run = h.completed_run(failures=True)
    result = h.service().build_snapshot(
        run_id=run.id,
        membership_ids=(failed_latest.id, rejected_latest.id),
    )
    by_job = {item.source_job_id: item for item in result.members}
    assert by_job["failed-latest"].semantic_coverage_status == "failed"
    assert by_job["rejected-latest"].semantic_coverage_status == "rejected"


def test_old_snapshot_remains_exact_after_new_source_and_membership(h: Harness) -> None:
    first_detail, first_translation = h.seed_source("historical", version=1)
    first_membership = h.membership(
        first_detail,
        disposition="core_match",
        translation_id=first_translation,
    )
    first_run = h.completed_run()
    first = h.service().build_snapshot(
        run_id=first_run.id,
        membership_ids=(first_membership.id,),
    )

    h.now += timedelta(minutes=1)
    second_detail, second_translation = h.seed_source("historical", version=2)
    second_membership = h.membership(
        second_detail,
        disposition="adjacent_match",
        translation_id=second_translation,
    )
    second_run = h.completed_run()
    second = h.service().build_snapshot(
        run_id=second_run.id,
        membership_ids=(second_membership.id,),
    )

    old_member = h.market.list_snapshot_members(first.snapshot.id)[0]
    new_member = h.market.list_snapshot_members(second.snapshot.id)[0]
    assert old_member.job_detail_version_id == first_detail
    assert old_member.membership_id == first_membership.id
    assert old_member.disposition == "core_match"
    assert new_member.job_detail_version_id == second_detail
    assert new_member.membership_id == second_membership.id
    assert new_member.disposition == "adjacent_match"

    with (
        sqlite3.connect(h.database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="immutable"),
    ):
        connection.execute(
            "UPDATE market_corpus_snapshot_members SET disposition = 'excluded' WHERE id = ?",
            (old_member.id,),
        )
