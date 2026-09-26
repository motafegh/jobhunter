import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.analysis_store import SEMANTIC_REVIEW_PENDING, AnalysisStore
from jobhunter.market_models import MarketDefinitionSpec, MarketSnapshotMemberInput
from jobhunter.market_store import MarketStore, MarketStoreError
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 16, 12, tzinfo=UTC)


def _target_definition(store: MarketStore):
    target = store.create_target(
        slug="applied-ai",
        name="Applied AI / ML Engineering",
        description="Applied production AI and ML engineering work.",
        created_at=_NOW,
    )
    definition = store.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI and ML engineering work",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused",),
            include_hints=("production ML", "AI systems"),
            exclude_hints=("content creation",),
            geography_scope="Tehran",
            freshness_rule="current-active",
        ),
        created_at=_NOW,
    )
    return target, definition


def _seed_job(
    database_path: Path,
    *,
    job_id: str,
    semantic: str,
    review_status: str = "accepted",
):
    source = JobHunterStore(database_path)
    source.initialize()
    posting = source.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="example",
            canonical_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
            observed_text="Applied AI Engineer",
        ),
        observed_at=_NOW,
    )
    detail = source.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW,
        requested_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        final_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        status_code=200,
        content_sha256=f"content-{semantic}",
        semantic_sha256=semantic,
        evidence_path=Path(f"{job_id}-{semantic}.html"),
        metadata_path=Path(f"{job_id}-{semantic}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": "Applied AI Engineer",
            "description": "Build production AI systems.",
            "skills": ["Python"],
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job(job_id)
    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        analysis={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [],
        },
        request_body={},
        raw_response={},
        created_at=_NOW,
        semantic_review_status=review_status,
    )
    return detail.version_id, translation.artifact_id, analysis_id


def _membership(
    store: MarketStore,
    *,
    definition_id: int,
    detail_id: int,
    disposition: str = "core_match",
    translation_id: int | None = None,
    analysis_id: int | None = None,
):
    return store.record_membership(
        target_definition_version_id=definition_id,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        classifier_contract_version="market-membership-v1",
        classifier_method="model" if translation_id else "deterministic",
        classifier_identity=(
            {"model": "membership-model", "prompt": "v1"}
            if translation_id
            else {"rule": "source-only"}
        ),
        disposition=disposition,
        reason="Evidence-backed representative decision.",
        evidence_refs=("source:title", "source:description"),
        confidence="high",
        created_at=_NOW,
    )


def test_target_definition_is_versioned_normalized_and_immutable(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = MarketStore(database_path)
    target, first = _target_definition(store)

    same = store.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI and ML engineering work",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused", "ai-focused"),
            include_hints=("AI systems", "production ML"),
            exclude_hints=("content creation",),
            geography_scope="Tehran",
            freshness_rule="current-active",
        ),
        created_at=_NOW,
    )
    assert same.id == first.id
    assert same.definition_fingerprint == first.definition_fingerprint

    second = store.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI engineering work including adjacent backend",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused",),
            freshness_rule="current-active",
        ),
        created_at=_NOW,
    )
    assert second.version_number == 2
    assert second.id != first.id

    renamed = store.update_target(
        target.id,
        name="Applied AI Engineering",
        description="Updated display copy only.",
        updated_at=_NOW,
    )
    assert renamed.id == target.id
    assert store.get_definition_version(first.id) == first

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="immutable"),
    ):
        connection.execute(
            """
            UPDATE market_target_definition_versions
            SET definition_json = '{}'
            WHERE id = ?
            """,
            (first.id,),
        )


def test_market_run_ledger_moves_once_from_running_to_terminal(tmp_path: Path) -> None:
    store = MarketStore(tmp_path / "jobhunter.sqlite3")
    _target, definition = _target_definition(store)
    run = store.start_run(
        definition.id,
        controls={"detail_limit": 5, "analysis_limit": 3},
        started_at=_NOW,
    )
    assert run.status == "running"
    updated = store.update_run_ledger(
        run.id,
        ledger={"candidate": 8, "attempted": 3, "failed": 1},
    )
    assert updated.ledger["failed"] == 1

    finished = store.finish_run(
        run.id,
        status="completed_with_failures",
        ledger={"candidate": 8, "attempted": 3, "failed": 1, "remaining": 5},
        completed_at=_NOW,
        error_summary="One bounded source operation failed.",
    )
    assert finished.status == "completed_with_failures"
    assert finished.completed_at is not None

    with pytest.raises(MarketStoreError, match="running"):
        store.update_run_ledger(run.id, ledger={})
    with pytest.raises(MarketStoreError, match="terminal"):
        store.finish_run(
            run.id,
            status="completed",
            ledger={},
            completed_at=_NOW,
        )


def test_membership_reuse_exact_dependencies_and_explicit_correction(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = MarketStore(database_path)
    _target, definition = _target_definition(store)
    detail_id, translation_id, analysis_id = _seed_job(
        database_path,
        job_id="core",
        semantic="v1",
    )
    membership = _membership(
        store,
        definition_id=definition.id,
        detail_id=detail_id,
        translation_id=translation_id,
        analysis_id=analysis_id,
    )
    assert store.find_reusable_membership(
        target_definition_version_id=definition.id,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        classifier_contract_version="market-membership-v1",
        classifier_method="model",
        classifier_identity={"model": "membership-model", "prompt": "v1"},
    ) == membership

    assert _membership(
        store,
        definition_id=definition.id,
        detail_id=detail_id,
        translation_id=translation_id,
        analysis_id=analysis_id,
    ).id == membership.id

    with pytest.raises(MarketStoreError, match="superseding correction"):
        store.record_membership(
            target_definition_version_id=definition.id,
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            analysis_artifact_id=analysis_id,
            classifier_contract_version="market-membership-v1",
            classifier_method="model",
            classifier_identity={"model": "membership-model", "prompt": "v1"},
            disposition="adjacent_match",
            reason="Changed judgment without explicit correction.",
            evidence_refs=("source:title",),
            confidence="medium",
            created_at=_NOW,
        )

    corrected = store.record_membership(
        target_definition_version_id=definition.id,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        classifier_contract_version="market-membership-v1",
        classifier_method="model",
        classifier_identity={"model": "membership-model", "prompt": "v1"},
        disposition="adjacent_match",
        reason="Explicit reviewed correction.",
        evidence_refs=("source:title", "source:description"),
        confidence="medium",
        supersedes_membership_id=membership.id,
        created_at=_NOW,
    )
    assert corrected.supersedes_membership_id == membership.id
    reusable = store.find_reusable_membership(
        target_definition_version_id=definition.id,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        classifier_contract_version="market-membership-v1",
        classifier_method="model",
        classifier_identity={"model": "membership-model", "prompt": "v1"},
    )
    assert reusable is not None
    assert reusable.id == corrected.id

    pending_detail, pending_translation, pending_analysis = _seed_job(
        database_path,
        job_id="pending",
        semantic="pending-v1",
        review_status=SEMANTIC_REVIEW_PENDING,
    )
    with pytest.raises(MarketStoreError, match="accepted P1.6"):
        _membership(
            store,
            definition_id=definition.id,
            detail_id=pending_detail,
            translation_id=pending_translation,
            analysis_id=pending_analysis,
        )


def test_new_source_version_does_not_reuse_old_membership(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = MarketStore(database_path)
    _target, definition = _target_definition(store)
    first_detail, _translation, _analysis = _seed_job(
        database_path,
        job_id="changing",
        semantic="v1",
    )
    first = _membership(
        store,
        definition_id=definition.id,
        detail_id=first_detail,
    )

    second_detail, _translation2, _analysis2 = _seed_job(
        database_path,
        job_id="changing",
        semantic="v2",
    )
    assert second_detail != first_detail
    assert store.find_reusable_membership(
        target_definition_version_id=definition.id,
        job_detail_version_id=second_detail,
        classifier_contract_version="market-membership-v1",
        classifier_method="deterministic",
        classifier_identity={"rule": "source-only"},
    ) is None
    assert store.get_membership(first.id) == first


def test_snapshot_freezes_membership_and_p16_coverage_without_zero_filling(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = MarketStore(database_path)
    _target, definition = _target_definition(store)
    run = store.start_run(definition.id, controls={}, started_at=_NOW)

    core_detail, core_translation, core_analysis = _seed_job(
        database_path,
        job_id="core",
        semantic="core-v1",
    )
    core = _membership(
        store,
        definition_id=definition.id,
        detail_id=core_detail,
        translation_id=core_translation,
        analysis_id=core_analysis,
    )

    pending_detail, pending_translation, pending_analysis = _seed_job(
        database_path,
        job_id="pending",
        semantic="pending-v1",
        review_status=SEMANTIC_REVIEW_PENDING,
    )
    pending = _membership(
        store,
        definition_id=definition.id,
        detail_id=pending_detail,
        disposition="uncertain",
    )

    missing_detail, _translation, _analysis = _seed_job(
        database_path,
        job_id="missing",
        semantic="missing-v1",
    )
    missing = _membership(
        store,
        definition_id=definition.id,
        detail_id=missing_detail,
        disposition="adjacent_match",
    )

    snapshot = store.record_snapshot(
        target_definition_version_id=definition.id,
        run_id=run.id,
        freshness_rule="current-active",
        source_scope={"source": "jobinja", "profile": "ai-focused"},
        metadata={"repost_adjustment": "not_implemented"},
        members=(
            MarketSnapshotMemberInput(
                membership_id=core.id,
                semantic_coverage_status="accepted",
                translation_artifact_id=core_translation,
                analysis_artifact_id=core_analysis,
            ),
            MarketSnapshotMemberInput(
                membership_id=pending.id,
                semantic_coverage_status="pending",
                translation_artifact_id=pending_translation,
                analysis_artifact_id=pending_analysis,
            ),
            MarketSnapshotMemberInput(
                membership_id=missing.id,
                semantic_coverage_status="missing",
            ),
        ),
        created_at=_NOW,
    )
    members = store.list_snapshot_members(snapshot.id)
    by_job = {member.source_job_id: member for member in members}
    assert by_job["core"].included_in_primary_corpus is True
    assert by_job["core"].semantic_coverage_status == "accepted"
    assert by_job["pending"].included_in_primary_corpus is False
    assert by_job["pending"].semantic_coverage_status == "pending"
    assert by_job["missing"].semantic_coverage_status == "missing"
    assert by_job["missing"].analysis_artifact_id is None
    assert store.latest_nonempty_snapshot_source_ids(definition.id) == (
        "core", "pending", "missing",
    )

    later_run = store.start_run(definition.id, controls={}, started_at=_NOW)
    store.record_snapshot(
        target_definition_version_id=definition.id,
        run_id=later_run.id,
        freshness_rule="current-active",
        source_scope={"source": "jobinja"},
        metadata={},
        members=(),
        created_at=_NOW,
    )
    assert store.latest_nonempty_snapshot_source_ids(definition.id) == (
        "core", "pending", "missing",
    )

    with pytest.raises(MarketStoreError, match="already has an immutable snapshot"):
        store.record_snapshot(
            target_definition_version_id=definition.id,
            run_id=run.id,
            freshness_rule="current-active",
            source_scope={},
            metadata={},
            members=(),
            created_at=_NOW,
        )

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="immutable"),
    ):
        connection.execute(
            "UPDATE market_corpus_snapshots SET freshness_rule = 'changed' WHERE id = ?",
            (snapshot.id,),
        )


def test_aggregate_profile_is_deterministic_for_one_snapshot_contract(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = MarketStore(database_path)
    _target, definition = _target_definition(store)
    run = store.start_run(definition.id, controls={}, started_at=_NOW)
    snapshot = store.record_snapshot(
        target_definition_version_id=definition.id,
        run_id=run.id,
        freshness_rule="current-active",
        source_scope={"source": "jobinja"},
        metadata={"repost_adjustment": "not_implemented"},
        members=(),
        created_at=_NOW,
    )

    first = store.record_aggregate_profile(
        snapshot_id=snapshot.id,
        profile={"core_postings": 0, "repost_adjustment": "not_implemented"},
        created_at=_NOW,
    )
    repeated = store.record_aggregate_profile(
        snapshot_id=snapshot.id,
        profile={"repost_adjustment": "not_implemented", "core_postings": 0},
        created_at=_NOW,
    )
    assert repeated.id == first.id

    with pytest.raises(MarketStoreError, match="different profile"):
        store.record_aggregate_profile(
            snapshot_id=snapshot.id,
            profile={"core_postings": 1, "repost_adjustment": "not_implemented"},
            created_at=_NOW,
        )

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="immutable"),
    ):
        connection.execute(
            "UPDATE market_aggregate_profiles SET profile_json = '{}' WHERE id = ?",
            (first.id,),
        )
