from datetime import UTC, datetime, timedelta
from pathlib import Path

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import SEMANTIC_REVIEW_PENDING, AnalysisStore
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.lifecycle import LifecycleStore
from jobhunter.market_affected_work import MarketAffectedWorkPlanner
from jobhunter.market_models import MarketDefinitionSpec
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 16, 15, tzinfo=UTC)


def _definition(database_path: Path) -> int:
    market = MarketStore(database_path)
    target = market.create_target(
        slug="applied-ai",
        name="Applied AI / ML Engineering",
        description="Applied production AI and ML engineering work.",
        created_at=_NOW,
    )
    definition = market.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI and ML engineering work",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused",),
            freshness_rule="current-active",
        ),
        created_at=_NOW,
    )
    return definition.id


def _discover_job(
    database_path: Path,
    source_job_id: str,
    *,
    observed_at: datetime = _NOW,
):
    store = JobHunterStore(database_path)
    store.initialize()
    return store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=source_job_id,
            company_slug=f"company-{source_job_id}",
            canonical_url=(
                f"https://jobinja.ir/companies/example/jobs/{source_job_id}/role"
            ),
            observed_text=f"Role {source_job_id}",
        ),
        observed_at=observed_at,
    )


def _record_detail(
    database_path: Path,
    source_job_id: str,
    *,
    fetched_at: datetime,
    semantic: str,
    parse_status: str = "parsed",
    language: str = "en",
) -> int:
    store = JobHunterStore(database_path)
    posting = store.get_job(source_job_id)
    assert posting is not None
    result = store.record_job_detail(
        job_posting_id=posting.id,
        fetched_at=fetched_at,
        requested_url=f"https://jobinja.ir/jobs/{source_job_id}",
        final_url=f"https://jobinja.ir/jobs/{source_job_id}",
        status_code=200,
        content_sha256=f"content-{semantic}",
        semantic_sha256=semantic,
        evidence_path=Path(f"{source_job_id}-{semantic}.html"),
        metadata_path=Path(f"{source_job_id}-{semantic}.json"),
        parser_version="jobinja-detail-v2",
        parse_status=parse_status,
        fields={
            "language": language,
            "title": f"Role {source_job_id}",
            "description": "Build production AI systems.",
            "skills": ["Python"],
        },
    )
    return result.version_id


def _translate(database_path: Path, source_job_id: str) -> int:
    result = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job(source_job_id)
    return result.artifact_id


def _record_analysis(
    database_path: Path,
    *,
    detail_id: int,
    translation_id: int,
    review_status: str = "accepted",
) -> int:
    return AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={"role_purpose": [], "responsibilities": [], "requirements": []},
        request_body={},
        raw_response={},
        created_at=_NOW,
        semantic_review_status=review_status,
    )


def _planner(
    database_path: Path,
    *,
    analysis_model: str | None = "analysis-model",
) -> MarketAffectedWorkPlanner:
    translation_store = TranslationStore(database_path)
    return MarketAffectedWorkPlanner(
        market_store=MarketStore(database_path),
        source_store=JobHunterStore(database_path),
        observations=JobDetailObservationStore(database_path),
        translation_store=translation_store,
        translation_service=TranslationService(
            store=translation_store,
            provider=None,
        ),
        analysis_store=AnalysisStore(database_path),
        analysis_model=analysis_model,
        clock=lambda: _NOW,
    )


def _plan(
    planner: MarketAffectedWorkPlanner,
    definition_id: int,
    candidate_ids: tuple[str, ...],
    *,
    missing_limit: int = 5,
    refresh_limit: int = 5,
    translation_limit: int = 5,
    analysis_limit: int = 5,
):
    return planner.plan(
        target_definition_version_id=definition_id,
        candidate_source_job_ids=candidate_ids,
        missing_limit=missing_limit,
        refresh_limit=refresh_limit,
        refresh_after_hours=24,
        translation_limit=translation_limit,
        analysis_limit=analysis_limit,
    )


def test_missing_detail_plan_never_spills_into_unrelated_global_backlog(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)
    _discover_job(database_path, "unrelated-missing", observed_at=_NOW - timedelta(days=2))
    _discover_job(database_path, "target-missing")

    plan = _plan(
        _planner(database_path),
        definition_id,
        ("target-missing",),
        missing_limit=5,
    )

    assert plan.candidate_ids == ("target-missing",)
    assert plan.missing_selected == ("target-missing",)
    assert plan.missing_remaining == ()
    assert "unrelated-missing" not in plan.missing_selected
    assert plan.ledger()["source"]["candidate"] == 1


def test_failed_refresh_does_not_freshen_or_remove_prior_valid_source(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)
    target = _discover_job(database_path, "target-stale")
    _discover_job(database_path, "unrelated-stale")
    _record_detail(
        database_path,
        "target-stale",
        fetched_at=_NOW - timedelta(days=10),
        semantic="target-v1",
    )
    _record_detail(
        database_path,
        "unrelated-stale",
        fetched_at=_NOW - timedelta(days=20),
        semantic="unrelated-v1",
    )
    observations = JobDetailObservationStore(database_path)
    observations.record_failure(
        job_posting_id=target.job_posting_id,
        checked_at=_NOW - timedelta(hours=1),
        requested_url="https://jobinja.ir/jobs/target-stale",
        error=RuntimeError("temporary network failure"),
    )

    plan = _plan(
        _planner(database_path),
        definition_id,
        ("target-stale",),
        refresh_limit=5,
    )
    state = plan.candidates[0]

    assert plan.refresh_selected == ("target-stale",)
    assert "unrelated-stale" not in plan.refresh_selected
    assert plan.latest_failed_refresh == ("target-stale",)
    assert state.lifecycle_state == "active"
    assert state.source_status == "refresh_due"
    assert state.source_action == "refresh_selected"
    assert state.latest_observation_outcome == "failed"
    assert state.source_eligible is False
    assert any("prior valid source evidence is retained" in item for item in state.warnings)


def test_recent_unchanged_success_refreshes_freshness_without_new_semantic_version(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)
    posting = _discover_job(database_path, "unchanged")
    detail_id = _record_detail(
        database_path,
        "unchanged",
        fetched_at=_NOW - timedelta(days=10),
        semantic="same-v1",
    )
    observations = JobDetailObservationStore(database_path)
    observations.record_success(
        job_posting_id=posting.job_posting_id,
        checked_at=_NOW - timedelta(hours=1),
        requested_url="https://jobinja.ir/jobs/unchanged",
        final_url="https://jobinja.ir/jobs/unchanged",
        status_code=200,
        content_sha256="content-same-v1-refetch",
        semantic_sha256="same-v1",
        evidence_path=Path("unchanged-latest.html"),
        metadata_path=Path("unchanged-latest.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        job_detail_version_id=detail_id,
        is_new_version=False,
    )

    plan = _plan(_planner(database_path), definition_id, ("unchanged",))
    state = plan.candidates[0]

    assert plan.refresh_selected == ()
    assert state.source_status == "current"
    assert state.source_eligible is True
    assert state.latest_observation_outcome == "unchanged"


def test_lifecycle_keeps_recent_possibly_unavailable_but_excludes_removed_and_expired(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)
    for job_id in ("maybe", "removed", "expired"):
        _discover_job(database_path, job_id)
        _record_detail(
            database_path,
            job_id,
            fetched_at=_NOW - timedelta(hours=2),
            semantic=f"{job_id}-v1",
        )

    lifecycle = LifecycleStore(database_path)
    lifecycle.record(
        "maybe",
        classification="not_found",
        status_code=404,
        checked_at=_NOW - timedelta(hours=1),
    )
    lifecycle.record(
        "removed",
        classification="not_found",
        status_code=404,
        checked_at=_NOW - timedelta(hours=2),
    )
    lifecycle.record(
        "removed",
        classification="gone",
        status_code=410,
        checked_at=_NOW - timedelta(hours=1),
    )
    lifecycle.record(
        "expired",
        classification="expired_explicit",
        status_code=200,
        checked_at=_NOW - timedelta(hours=1),
    )

    plan = _plan(
        _planner(database_path),
        definition_id,
        ("maybe", "removed", "expired"),
    )
    by_id = {item.source_job_id: item for item in plan.candidates}

    assert plan.source_ready == ("maybe",)
    assert by_id["maybe"].lifecycle_state == "possibly_unavailable"
    assert by_id["maybe"].source_eligible is True
    assert any("possibly unavailable" in item for item in by_id["maybe"].warnings)
    assert by_id["removed"].source_status == "removed"
    assert by_id["removed"].source_eligible is False
    assert by_id["expired"].source_status == "expired"
    assert by_id["expired"].source_eligible is False


def test_downstream_plan_reuses_exact_current_artifacts_and_keeps_pending_review(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)

    _discover_job(database_path, "accepted")
    accepted_detail = _record_detail(
        database_path,
        "accepted",
        fetched_at=_NOW - timedelta(hours=2),
        semantic="accepted-v1",
    )
    accepted_translation = _translate(database_path, "accepted")
    accepted_analysis = _record_analysis(
        database_path,
        detail_id=accepted_detail,
        translation_id=accepted_translation,
    )

    _discover_job(database_path, "pending")
    pending_detail = _record_detail(
        database_path,
        "pending",
        fetched_at=_NOW - timedelta(hours=2),
        semantic="pending-v1",
    )
    pending_translation = _translate(database_path, "pending")
    pending_analysis = _record_analysis(
        database_path,
        detail_id=pending_detail,
        translation_id=pending_translation,
        review_status=SEMANTIC_REVIEW_PENDING,
    )

    _discover_job(database_path, "needs-translation")
    _record_detail(
        database_path,
        "needs-translation",
        fetched_at=_NOW - timedelta(hours=2),
        semantic="needs-translation-v1",
    )

    _discover_job(database_path, "unrelated-ready")
    _record_detail(
        database_path,
        "unrelated-ready",
        fetched_at=_NOW - timedelta(hours=2),
        semantic="unrelated-v1",
    )

    plan = _plan(
        _planner(database_path),
        definition_id,
        ("accepted", "pending", "needs-translation"),
        translation_limit=5,
        analysis_limit=5,
    )
    by_id = {item.source_job_id: item for item in plan.candidates}

    assert plan.translation_reused == ("accepted", "pending")
    assert plan.translation_selected == ("needs-translation",)
    assert plan.analysis_current_accepted == ("accepted",)
    assert plan.analysis_current_pending == ("pending",)
    assert by_id["accepted"].analysis_artifact_id == accepted_analysis
    assert by_id["pending"].analysis_artifact_id == pending_analysis
    assert by_id["pending"].analysis_status == "current_pending_review"
    assert by_id["needs-translation"].analysis_status == "blocked_translation"
    assert "unrelated-ready" not in plan.candidate_ids
    assert "unrelated-ready" not in plan.translation_selected
    assert "unrelated-ready" not in plan.analysis_selected


def test_new_source_version_invalidates_old_translation_and_analysis_reuse(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)
    _discover_job(database_path, "changing")
    first_detail = _record_detail(
        database_path,
        "changing",
        fetched_at=_NOW - timedelta(hours=4),
        semantic="changing-v1",
    )
    first_translation = _translate(database_path, "changing")
    _record_analysis(
        database_path,
        detail_id=first_detail,
        translation_id=first_translation,
    )
    second_detail = _record_detail(
        database_path,
        "changing",
        fetched_at=_NOW - timedelta(hours=1),
        semantic="changing-v2",
    )

    plan = _plan(_planner(database_path), definition_id, ("changing",))
    state = plan.candidates[0]

    assert second_detail != first_detail
    assert state.job_detail_version_id == second_detail
    assert plan.translation_reused == ()
    assert plan.translation_selected == ("changing",)
    assert state.translation_artifact_id is None
    assert state.analysis_status == "blocked_translation"
    assert state.analysis_artifact_id is None


def test_target_budgets_leave_target_work_remaining_without_global_fill(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    definition_id = _definition(database_path)

    for job_id in ("missing-a", "missing-b", "unrelated-missing"):
        _discover_job(database_path, job_id)

    for job_id in ("translate-a", "translate-b", "unrelated-translate"):
        _discover_job(database_path, job_id)
        _record_detail(
            database_path,
            job_id,
            fetched_at=_NOW - timedelta(hours=1),
            semantic=f"{job_id}-v1",
        )

    for job_id in ("analyze-a", "analyze-b", "unrelated-analyze"):
        _discover_job(database_path, job_id)
        _record_detail(
            database_path,
            job_id,
            fetched_at=_NOW - timedelta(hours=1),
            semantic=f"{job_id}-v1",
        )
        _translate(database_path, job_id)

    target_ids = (
        "missing-a",
        "missing-b",
        "translate-a",
        "translate-b",
        "analyze-a",
        "analyze-b",
    )
    plan = _plan(
        _planner(database_path),
        definition_id,
        target_ids,
        missing_limit=1,
        translation_limit=1,
        analysis_limit=1,
    )

    assert plan.missing_selected == ("missing-a",)
    assert plan.missing_remaining == ("missing-b",)
    assert plan.translation_selected == ("translate-a",)
    assert plan.translation_remaining == ("translate-b",)
    assert plan.analysis_selected == ("analyze-a",)
    assert plan.analysis_remaining == ("analyze-b",)
    assert all("unrelated" not in job_id for job_id in plan.candidate_ids)
    assert all("unrelated" not in job_id for job_id in plan.missing_selected)
    assert all("unrelated" not in job_id for job_id in plan.translation_selected)
    assert all("unrelated" not in job_id for job_id in plan.analysis_selected)
