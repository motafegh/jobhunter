"""I4 immutable Market snapshot assembly over exact I1-I3 identities.

The service does not acquire sources, translate, run P1.6, infer membership, aggregate
market statistics, or publish corpus state. It validates exact membership decisions
against current I2 source/dependency state and freezes one point-in-time snapshot.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.market_affected_work import (
    MarketAffectedWorkPlanner,
    MarketAnalysisStatus,
    MarketCandidateAffectedWork,
)
from jobhunter.market_membership_models import MARKET_MEMBERSHIP_CONTRACT_VERSION
from jobhunter.market_models import (
    MarketCorpusSnapshot,
    MarketCorpusSnapshotMember,
    MarketJobMembership,
    MarketRunStatus,
    MarketSnapshotMemberInput,
    P16CoverageStatus,
)
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import build_translation_service
from jobhunter.translation_store import TranslationStore


class MarketSnapshotError(ValueError):
    """Raised when current state cannot support an authoritative I4 snapshot."""


@dataclass(frozen=True, slots=True)
class MarketSnapshotBuildResult:
    snapshot: MarketCorpusSnapshot
    members: tuple[MarketCorpusSnapshotMember, ...]


@dataclass(frozen=True, slots=True)
class _Coverage:
    status: str
    translation_artifact_id: int | None
    analysis_artifact_id: int | None
    basis: dict[str, Any]


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _as_utc(raw: str) -> datetime:
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _normalize_ids(values: tuple[int, ...]) -> tuple[int, ...]:
    if any(not isinstance(value, int) or value <= 0 for value in values):
        raise MarketSnapshotError("membership_ids must contain positive integers")
    normalized = tuple(dict.fromkeys(values))
    if len(normalized) != len(values):
        raise MarketSnapshotError("membership_ids must not contain duplicates")
    if len(normalized) > 5000:
        raise MarketSnapshotError("At most 5000 memberships may enter one snapshot")
    return normalized


class MarketSnapshotService:
    """Validate exact current memberships and freeze one immutable Market snapshot."""

    def __init__(
        self,
        *,
        database_path: Path,
        market_store: MarketStore,
        planner: MarketAffectedWorkPlanner,
        translation_store: TranslationStore,
        analysis_model: str | None,
        clock=_utc_now,
    ) -> None:
        self._database_path = database_path
        self._market = market_store
        self._planner = planner
        self._translations = translation_store
        self._analysis_model = analysis_model.strip() if analysis_model else None
        self._clock = clock

    def build_snapshot(
        self,
        *,
        run_id: int,
        membership_ids: tuple[int, ...],
        refresh_after_hours: float = 24,
    ) -> MarketSnapshotBuildResult:
        """Freeze exact qualified membership decisions for one terminal Market run."""

        if refresh_after_hours <= 0:
            raise ValueError("refresh_after_hours must be greater than zero")
        membership_ids = _normalize_ids(membership_ids)
        run = self._market.get_run(run_id)
        if run is None:
            raise LookupError(f"Unknown Market run {run_id}")
        if run.status not in {
            MarketRunStatus.COMPLETED,
            MarketRunStatus.COMPLETED_WITH_FAILURES,
        }:
            raise MarketSnapshotError(
                "I4 snapshots require a completed or completed-with-failures Market run"
            )
        definition = self._market.get_definition_version(
            run.target_definition_version_id
        )
        if definition is None:
            raise RuntimeError("Market run lost its target-definition dependency")

        memberships = tuple(self._require_membership(value) for value in membership_ids)
        source_ids = tuple(item.source_job_id for item in memberships)
        if len(source_ids) != len(set(source_ids)):
            raise MarketSnapshotError(
                "One source job may contribute at most one membership to a snapshot"
            )
        if any(
            item.target_definition_version_id != definition.id for item in memberships
        ):
            raise MarketSnapshotError(
                "All snapshot memberships must belong to the run target definition"
            )

        plan = self._planner.plan(
            target_definition_version_id=definition.id,
            candidate_source_job_ids=source_ids,
            missing_limit=0,
            refresh_limit=0,
            refresh_after_hours=refresh_after_hours,
            translation_limit=0,
            analysis_limit=0,
        )
        candidates = {item.source_job_id: item for item in plan.candidates}
        prepared: list[MarketSnapshotMemberInput] = []
        dispositions = {
            "core_match": 0,
            "adjacent_match": 0,
            "uncertain": 0,
            "excluded": 0,
        }
        coverage_counts = {value.value: 0 for value in P16CoverageStatus}
        core_coverage_counts = {value.value: 0 for value in P16CoverageStatus}

        for membership in memberships:
            candidate = candidates.get(membership.source_job_id)
            if candidate is None:
                raise RuntimeError("I2 planner omitted a requested snapshot candidate")
            self._validate_membership(membership, candidate)
            coverage = self._coverage(candidate)
            state = {
                "membership_dependency_fingerprint": membership.dependency_fingerprint,
                "membership_classifier_contract": membership.classifier_contract_version,
                "membership_classifier_method": membership.classifier_method,
                "source_status": candidate.source_status,
                "lifecycle_state": candidate.lifecycle_state,
                "latest_detail_at": candidate.latest_detail_at,
                "latest_observation_outcome": candidate.latest_observation_outcome,
                "warnings": list(candidate.warnings),
                "translation_status": candidate.translation_status,
                "analysis_status": candidate.analysis_status,
                "analysis_review_status": candidate.analysis_review_status,
                "coverage_basis": coverage.basis,
            }
            prepared.append(
                MarketSnapshotMemberInput(
                    membership_id=membership.id,
                    semantic_coverage_status=coverage.status,
                    translation_artifact_id=coverage.translation_artifact_id,
                    analysis_artifact_id=coverage.analysis_artifact_id,
                    state=state,
                )
            )
            dispositions[membership.disposition] += 1
            coverage_counts[coverage.status] += 1
            if membership.disposition == "core_match":
                core_coverage_counts[coverage.status] += 1

        source_scope = {
            "source": definition.spec.source,
            "search_catalog_version": definition.spec.search_catalog_version,
            "search_profiles": list(definition.spec.search_profiles),
            "search_packs": list(definition.spec.search_packs),
            "extra_search_terms": list(definition.spec.extra_search_terms),
            "raw_searches": list(definition.spec.raw_searches),
            "target_definition_fingerprint": definition.definition_fingerprint,
            "membership_ids": list(membership_ids),
        }
        metadata = {
            "member_count": len(memberships),
            "dispositions": dispositions,
            "primary_core_postings": dispositions["core_match"],
            "semantic_coverage": coverage_counts,
            "core_semantic_coverage": core_coverage_counts,
            "accepted_semantic_core_postings": core_coverage_counts["accepted"],
            "denominator_language": "qualified source postings",
            "repost_adjustment": "not_implemented",
            "membership_contract": MARKET_MEMBERSHIP_CONTRACT_VERSION,
            "analysis_contract": {
                "model": self._analysis_model,
                "prompt_version": ENGLISH_PROMPT_VERSION,
                "schema_version": ENGLISH_ANALYSIS_SCHEMA_VERSION,
            },
        }
        snapshot = self._market.record_snapshot(
            target_definition_version_id=definition.id,
            run_id=run.id,
            freshness_rule=definition.spec.freshness_rule,
            source_scope=source_scope,
            metadata=metadata,
            members=tuple(prepared),
            created_at=self._clock(),
        )
        return MarketSnapshotBuildResult(
            snapshot=snapshot,
            members=self._market.list_snapshot_members(snapshot.id),
        )

    def _require_membership(self, membership_id: int) -> MarketJobMembership:
        membership = self._market.get_membership(membership_id)
        if membership is None:
            raise LookupError(f"Unknown Market membership {membership_id}")
        return membership

    def _validate_membership(
        self,
        membership: MarketJobMembership,
        candidate: MarketCandidateAffectedWork,
    ) -> None:
        if membership.classifier_contract_version != MARKET_MEMBERSHIP_CONTRACT_VERSION:
            raise MarketSnapshotError(
                "Snapshot membership does not use the current I3 membership contract"
            )
        if not candidate.source_eligible:
            raise MarketSnapshotError(
                f"Snapshot membership {membership.id} no longer has current source evidence"
            )
        if membership.job_detail_version_id != candidate.job_detail_version_id:
            raise MarketSnapshotError(
                f"Snapshot membership {membership.id} names a stale source version"
            )
        latest = self._market.find_reusable_membership(
            target_definition_version_id=membership.target_definition_version_id,
            job_detail_version_id=membership.job_detail_version_id,
            translation_artifact_id=membership.translation_artifact_id,
            analysis_artifact_id=membership.analysis_artifact_id,
            classifier_contract_version=membership.classifier_contract_version,
            classifier_method=membership.classifier_method,
            classifier_identity=membership.classifier_identity,
        )
        if latest is None or latest.id != membership.id:
            raise MarketSnapshotError(
                f"Snapshot membership {membership.id} has been superseded"
            )

        if membership.classifier_method == "deterministic":
            if (
                membership.translation_artifact_id is not None
                or membership.analysis_artifact_id is not None
            ):
                raise MarketSnapshotError(
                    "Deterministic membership must remain source-only"
                )
            return
        if membership.classifier_method != "model":
            raise MarketSnapshotError(
                f"Unsupported membership classifier method {membership.classifier_method!r}"
            )

        expected_translation = candidate.translation_artifact_id
        expected_analysis = (
            candidate.analysis_artifact_id
            if candidate.analysis_review_status == "accepted"
            else None
        )
        if membership.translation_artifact_id != expected_translation:
            raise MarketSnapshotError(
                f"Snapshot membership {membership.id} does not consume the current translation"
            )
        if membership.analysis_artifact_id != expected_analysis:
            raise MarketSnapshotError(
                f"Snapshot membership {membership.id} does not consume current accepted P1.6"
            )

    def _coverage(self, candidate: MarketCandidateAffectedWork) -> _Coverage:
        translation_id = candidate.translation_artifact_id
        if candidate.analysis_status == MarketAnalysisStatus.CURRENT_ACCEPTED:
            if candidate.analysis_artifact_id is None:
                raise RuntimeError("Accepted current P1.6 lost its artifact identity")
            return _Coverage(
                status=P16CoverageStatus.ACCEPTED,
                translation_artifact_id=translation_id,
                analysis_artifact_id=candidate.analysis_artifact_id,
                basis={"kind": "live_artifact", "review_status": "accepted"},
            )
        if candidate.analysis_status == MarketAnalysisStatus.CURRENT_PENDING_REVIEW:
            if candidate.analysis_artifact_id is None:
                raise RuntimeError("Pending current P1.6 lost its artifact identity")
            return _Coverage(
                status=P16CoverageStatus.PENDING,
                translation_artifact_id=translation_id,
                analysis_artifact_id=candidate.analysis_artifact_id,
                basis={"kind": "live_artifact", "review_status": "pending"},
            )

        if self._analysis_model is None or translation_id is None:
            return _Coverage(
                status=P16CoverageStatus.MISSING,
                translation_artifact_id=translation_id,
                analysis_artifact_id=None,
                basis={"kind": "no_current_analysis_dependency"},
            )

        translation = self._translations.artifact_by_id(translation_id)
        if translation is None:
            raise RuntimeError("I2 current translation disappeared during snapshot assembly")
        rejected = self._latest_rejected(
            job_detail_version_id=candidate.job_detail_version_id,
            translation_artifact_id=translation_id,
        )
        failed = self._latest_failed_attempt(
            job_detail_version_id=candidate.job_detail_version_id,
            not_before=translation.created_at,
        )
        events: list[tuple[datetime, str, dict[str, Any]]] = []
        if rejected is not None:
            events.append(
                (
                    _as_utc(str(rejected["rejected_at"])),
                    P16CoverageStatus.REJECTED,
                    {
                        "kind": "rejected_artifact",
                        "rejected_artifact_id": int(rejected["id"]),
                        "original_artifact_id": int(rejected["original_artifact_id"]),
                        "rejected_at": str(rejected["rejected_at"]),
                    },
                )
            )
        if failed is not None:
            events.append(
                (
                    _as_utc(str(failed["attempted_at"])),
                    P16CoverageStatus.FAILED,
                    {
                        "kind": "failed_attempt",
                        "attempt_id": int(failed["id"]),
                        "attempted_at": str(failed["attempted_at"]),
                        "error_type": failed["error_type"],
                    },
                )
            )
        if events:
            _stamp, status, basis = max(events, key=lambda value: value[0])
            return _Coverage(
                status=status,
                translation_artifact_id=translation_id,
                analysis_artifact_id=None,
                basis=basis,
            )
        return _Coverage(
            status=P16CoverageStatus.MISSING,
            translation_artifact_id=translation_id,
            analysis_artifact_id=None,
            basis={"kind": "no_current_p16_artifact_or_processing_event"},
        )

    def _latest_rejected(
        self,
        *,
        job_detail_version_id: int | None,
        translation_artifact_id: int,
    ) -> sqlite3.Row | None:
        if job_detail_version_id is None:
            return None
        with self._connect_readonly() as connection:
            return connection.execute(
                """
                SELECT id, original_artifact_id, rejected_at
                FROM job_analysis_rejected_artifacts
                WHERE job_detail_version_id = ?
                  AND translation_artifact_id = ?
                  AND model = ?
                  AND prompt_version = ?
                  AND schema_version = ?
                ORDER BY rejected_at DESC, id DESC
                LIMIT 1
                """,
                (
                    job_detail_version_id,
                    translation_artifact_id,
                    self._analysis_model,
                    ENGLISH_PROMPT_VERSION,
                    ENGLISH_ANALYSIS_SCHEMA_VERSION,
                ),
            ).fetchone()

    def _latest_failed_attempt(
        self,
        *,
        job_detail_version_id: int | None,
        not_before: str,
    ) -> sqlite3.Row | None:
        if job_detail_version_id is None:
            return None
        with self._connect_readonly() as connection:
            return connection.execute(
                """
                SELECT id, attempted_at, error_type
                FROM job_analysis_attempts
                WHERE job_detail_version_id = ?
                  AND model = ?
                  AND prompt_version = ?
                  AND schema_version = ?
                  AND outcome = 'failed'
                  AND attempted_at >= ?
                ORDER BY attempted_at DESC, id DESC
                LIMIT 1
                """,
                (
                    job_detail_version_id,
                    self._analysis_model,
                    ENGLISH_PROMPT_VERSION,
                    ENGLISH_ANALYSIS_SCHEMA_VERSION,
                    not_before,
                ),
            ).fetchone()

    def _connect_readonly(self) -> sqlite3.Connection:
        connection = sqlite3.connect(f"file:{self._database_path.resolve()}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection


def build_market_snapshot_service(settings: Settings) -> MarketSnapshotService:
    """Compose I4 from existing I1/I2 source, translation, and P1.6 owners."""

    market = MarketStore(settings.database_path)
    translations = TranslationStore(settings.database_path)
    analyses = AnalysisStore(settings.database_path)
    analysis_model = settings.effective_analysis_lm_studio_model()
    planner = MarketAffectedWorkPlanner(
        market_store=market,
        source_store=JobHunterStore(settings.database_path),
        observations=JobDetailObservationStore(settings.database_path),
        translation_store=translations,
        translation_service=build_translation_service(settings),
        analysis_store=analyses,
        analysis_model=analysis_model,
    )
    return MarketSnapshotService(
        database_path=settings.database_path,
        market_store=market,
        planner=planner,
        translation_store=translations,
        analysis_model=analysis_model,
    )
