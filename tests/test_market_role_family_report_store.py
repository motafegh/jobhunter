import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from jobhunter.market_models import (
    ROLE_FAMILY_REPORT_CONTRACT_VERSION,
    ROLE_FAMILY_REPORT_REVIEW_CONTRACT_VERSION,
    MarketDefinitionSpec,
)
from jobhunter.market_role_family_report_store import (
    MarketRoleFamilyReportStore,
    MarketRoleFamilyReportStoreError,
    canonical_json_sha256,
    role_family_generation_fingerprint,
    role_family_input_fingerprint,
    role_family_report_sha256,
)
from jobhunter.market_store import MarketStore

_NOW = datetime(2026, 10, 4, 12, tzinfo=UTC)
_CANDIDATE_CONTRACT = "market-role-family-candidate-v6"
_PROMPT_VERSION = "market-role-family-candidate-prompt-v6"
_MODEL = "gemma-4-e4b-it-ud"


def _identity(**overrides):
    value = {
        "provider": "lm-studio",
        "model": _MODEL,
        "context_length": 16384,
        "max_tokens": 2048,
        "seed": 0,
        "structured_schema": "jobhunter_market_candidate_report",
    }
    value.update(overrides)
    return value


def _candidate_input(snapshot_id: int) -> dict:
    return {
        "snapshot": {
            "id": snapshot_id,
            "contract": "market-corpus-snapshot-v1",
            "definition_id": 1,
        },
        "claims": [
            ["C1", "J1", "responsibility", "Build agent workflows."],
            ["C2", "J2", "requirement", "Production LLM experience."],
        ],
    }


def _report_payload(label: str = "Agent engineering") -> dict:
    return {
        "contract": _CANDIDATE_CONTRACT,
        "work_clusters": [
            {
                "label": label,
                "evidence_refs": ["W:job-a:0"],
                "supporting_source_job_ids": ["job-a"],
            }
        ],
        "integrity_rejections": [],
    }


def _snapshot(database_path: Path) -> int:
    market = MarketStore(database_path)
    target = market.create_target(
        slug="applied-ai",
        name="Applied AI",
        description=None,
        created_at=_NOW,
    )
    definition = market.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI engineering work",
            search_catalog_version="fixture-v1",
        ),
        created_at=_NOW,
    )
    run = market.start_run(
        definition.id,
        controls={"fixture": True},
        started_at=_NOW,
    )
    market.finish_run(
        run.id,
        status="completed",
        ledger={"fixture": True},
        completed_at=_NOW,
    )
    return market.record_snapshot(
        target_definition_version_id=definition.id,
        run_id=run.id,
        freshness_rule="current-active",
        source_scope={"source": "jobinja"},
        metadata={"fixture": True},
        members=(),
        created_at=_NOW,
    ).id


def _record_report(
    store: MarketRoleFamilyReportStore,
    snapshot_id: int,
    *,
    label: str = "Agent engineering",
    created_at: datetime = _NOW,
):
    return store.record_report(
        snapshot_id=snapshot_id,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
        report=_report_payload(label),
        request_body={"request": "fixture"},
        raw_response={"response": "fixture"},
        created_at=created_at,
    )


def test_role_family_fingerprints_use_canonical_json() -> None:
    first_input = {"snapshot": {"id": 15}, "claims": [{"b": 2, "a": 1}]}
    reordered_input = {"claims": [{"a": 1, "b": 2}], "snapshot": {"id": 15}}

    first_input_hash = role_family_input_fingerprint(first_input)
    assert first_input_hash == role_family_input_fingerprint(reordered_input)
    assert first_input_hash == canonical_json_sha256(first_input)

    first_generation = role_family_generation_fingerprint(
        input_fingerprint=first_input_hash,
        report_contract_version=ROLE_FAMILY_REPORT_CONTRACT_VERSION,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
    )
    reordered_generation = role_family_generation_fingerprint(
        input_fingerprint=first_input_hash,
        report_contract_version=ROLE_FAMILY_REPORT_CONTRACT_VERSION,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity={
            "seed": 0,
            "max_tokens": 2048,
            "context_length": 16384,
            "structured_schema": "jobhunter_market_candidate_report",
            "provider": "lm-studio",
            "model": _MODEL,
        },
    )
    assert first_generation == reordered_generation

    first_report = {"b": [2, 1], "a": {"value": True}}
    second_report = {"a": {"value": True}, "b": [2, 1]}
    assert role_family_report_sha256(first_report) == role_family_report_sha256(
        second_report
    )


def test_generation_identity_requires_semantic_settings() -> None:
    input_hash = role_family_input_fingerprint({"snapshot": 15})

    with pytest.raises(
        MarketRoleFamilyReportStoreError,
        match="generation_identity.model must match model",
    ):
        role_family_generation_fingerprint(
            input_fingerprint=input_hash,
            report_contract_version=ROLE_FAMILY_REPORT_CONTRACT_VERSION,
            candidate_contract_version=_CANDIDATE_CONTRACT,
            prompt_version=_PROMPT_VERSION,
            model=_MODEL,
            generation_identity=_identity(model="other-model"),
        )

    with pytest.raises(
        MarketRoleFamilyReportStoreError,
        match="context_length must be a positive integer",
    ):
        role_family_generation_fingerprint(
            input_fingerprint=input_hash,
            report_contract_version=ROLE_FAMILY_REPORT_CONTRACT_VERSION,
            candidate_contract_version=_CANDIDATE_CONTRACT,
            prompt_version=_PROMPT_VERSION,
            model=_MODEL,
            generation_identity=_identity(context_length=0),
        )


def test_reports_are_immutable_and_explicit_regeneration_is_allowed(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)

    first = _record_report(store, snapshot_id)
    second = _record_report(
        store,
        snapshot_id,
        label="Agent engineering alternative sample",
        created_at=_NOW + timedelta(minutes=1),
    )

    assert first.id != second.id
    assert first.generation_fingerprint == second.generation_fingerprint
    assert first.report_sha256 != second.report_sha256
    assert store.find_reusable_report(
        snapshot_id=snapshot_id,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
    ) == second
    assert store.list_reports(snapshot_id) == (second, first)

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="reports are immutable"),
    ):
        connection.execute(
            "UPDATE market_role_family_reports SET report_json = '{}' WHERE id = ?",
            (first.id,),
        )

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="reports are immutable"),
    ):
        connection.execute(
            "DELETE FROM market_role_family_reports WHERE id = ?",
            (first.id,),
        )


def test_attempt_history_is_terminal_append_only_and_generation_bound(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)
    report = _record_report(store, snapshot_id)

    completed = store.record_attempt(
        snapshot_id=snapshot_id,
        attempted_at=_NOW,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
        outcome="completed",
        artifact_id=report.id,
    )
    reused = store.record_attempt(
        snapshot_id=snapshot_id,
        attempted_at=_NOW + timedelta(minutes=1),
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
        outcome="reused",
        artifact_id=report.id,
    )
    failed = store.record_attempt(
        snapshot_id=snapshot_id,
        attempted_at=_NOW + timedelta(minutes=2),
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
        outcome="failed",
        error=RuntimeError("fixture inference failure"),
    )

    assert completed.artifact_id == report.id
    assert reused.artifact_id == report.id
    assert failed.artifact_id is None
    assert failed.error_type == "RuntimeError"
    assert [item.outcome for item in store.list_attempts(snapshot_id)] == [
        "completed",
        "reused",
        "failed",
    ]

    with pytest.raises(
        MarketRoleFamilyReportStoreError,
        match="failed attempt must not reference an artifact",
    ):
        store.record_attempt(
            snapshot_id=snapshot_id,
            attempted_at=_NOW,
            candidate_contract_version=_CANDIDATE_CONTRACT,
            prompt_version=_PROMPT_VERSION,
            model=_MODEL,
            generation_identity=_identity(),
            candidate_input=_candidate_input(snapshot_id),
            outcome="failed",
            artifact_id=report.id,
        )

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="attempts are immutable"),
    ):
        connection.execute(
            "UPDATE market_role_family_report_attempts SET outcome = 'failed' "
            "WHERE id = ?",
            (completed.id,),
        )


def test_failed_attempt_creates_no_report_and_does_not_mutate_upstream_state(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)
    store.initialize()

    with sqlite3.connect(database_path) as connection:
        before = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in (
                "market_corpus_snapshots",
                "market_corpus_snapshot_members",
                "market_aggregate_profiles",
                "job_analysis_artifacts",
                "market_role_family_reports",
            )
        }

    store.record_attempt(
        snapshot_id=snapshot_id,
        attempted_at=_NOW,
        candidate_contract_version=_CANDIDATE_CONTRACT,
        prompt_version=_PROMPT_VERSION,
        model=_MODEL,
        generation_identity=_identity(),
        candidate_input=_candidate_input(snapshot_id),
        outcome="failed",
        error=RuntimeError("fixture inference failure"),
    )

    with sqlite3.connect(database_path) as connection:
        after = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in before
        }
        attempt_count = connection.execute(
            "SELECT COUNT(*) FROM market_role_family_report_attempts"
        ).fetchone()[0]

    assert after == before
    assert attempt_count == 1


def test_review_history_is_append_only_and_controls_accepted_selection(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)
    first = _record_report(store, snapshot_id)
    second = _record_report(
        store,
        snapshot_id,
        label="Second report",
        created_at=_NOW + timedelta(minutes=1),
    )

    assert store.effective_review_state(first.id) == "pending"
    assert store.latest_accepted_for_snapshot(snapshot_id) is None

    first_accept = store.record_review(
        report_artifact_id=first.id,
        disposition="accepted_for_bounded_use",
        note="Useful bounded interpretation.",
        reviewed_at=_NOW,
    )
    assert (
        first_accept.review_contract_version
        == ROLE_FAMILY_REPORT_REVIEW_CONTRACT_VERSION
    )
    assert store.effective_review_state(first.id) == "accepted_for_bounded_use"
    assert store.latest_accepted_for_snapshot(snapshot_id) == first

    store.record_review(
        report_artifact_id=second.id,
        disposition="accepted_for_bounded_use",
        reviewed_at=_NOW + timedelta(minutes=1),
    )
    assert store.latest_accepted_for_snapshot(snapshot_id) == second

    second_reject = store.record_review(
        report_artifact_id=second.id,
        disposition="rejected",
        note="Later owner review rejected this generation.",
        reviewed_at=_NOW + timedelta(minutes=2),
    )
    assert store.effective_review(second.id) == second_reject
    assert store.latest_accepted_for_snapshot(snapshot_id) == first

    store.record_review(
        report_artifact_id=first.id,
        disposition="rejected",
        reviewed_at=_NOW + timedelta(minutes=3),
    )
    assert store.latest_accepted_for_snapshot(snapshot_id) is None
    assert [review.disposition for review in store.list_reviews(first.id)] == [
        "accepted_for_bounded_use",
        "rejected",
    ]

    with (
        sqlite3.connect(database_path) as connection,
        pytest.raises(sqlite3.IntegrityError, match="reviews are immutable"),
    ):
        connection.execute(
            "UPDATE market_role_family_report_reviews SET disposition = 'rejected' "
            "WHERE id = ?",
            (first_accept.id,),
        )


def test_attempt_cannot_reference_artifact_from_other_generation(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)
    report = _record_report(store, snapshot_id)

    with pytest.raises(
        MarketRoleFamilyReportStoreError,
        match="generation identity does not match",
    ):
        store.record_attempt(
            snapshot_id=snapshot_id,
            attempted_at=_NOW,
            candidate_contract_version=_CANDIDATE_CONTRACT,
            prompt_version=_PROMPT_VERSION,
            model=_MODEL,
            generation_identity=_identity(seed=1),
            candidate_input=_candidate_input(snapshot_id),
            outcome="reused",
            artifact_id=report.id,
        )


def test_persisted_report_fingerprint_corruption_fails_closed(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    snapshot_id = _snapshot(database_path)
    store = MarketRoleFamilyReportStore(database_path)
    report = _record_report(store, snapshot_id)

    with sqlite3.connect(database_path) as connection:
        connection.execute("DROP TRIGGER market_role_family_reports_immutable_update")
        connection.execute(
            "UPDATE market_role_family_reports SET report_json = '{}' WHERE id = ?",
            (report.id,),
        )

    with pytest.raises(
        MarketRoleFamilyReportStoreError,
        match="report fingerprint is corrupt",
    ):
        store.get_report(report.id)
