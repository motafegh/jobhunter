"""Target-scoped source eligibility and affected-work planning for Market I2.

This module is intentionally read-only. It composes the existing source, lifecycle,
observation, translation, and P1.6 currentness owners to decide which work belongs
inside one already-discovered target candidate set. It never falls through to the
global JobHunter backlog when target work is exhausted.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import (
    SEMANTIC_REVIEW_ACCEPTED,
    SEMANTIC_REVIEW_PENDING,
    AnalysisStore,
)
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import (
    TranslationProviderUnavailableError,
    TranslationService,
)
from jobhunter.translation_store import TranslationStore


class MarketPlanningError(ValueError):
    """Raised when an I2 target-scoped plan would violate its integrity boundary."""


class MarketSourceStatus(StrEnum):
    CURRENT = "current"
    MISSING_DETAIL = "missing_detail"
    REFRESH_DUE = "refresh_due"
    INVALID_CURRENT_DETAIL = "invalid_current_detail"
    EXPIRED = "expired"
    REMOVED = "removed"
    INELIGIBLE_LIFECYCLE = "ineligible_lifecycle"


class MarketSourceAction(StrEnum):
    NONE = "none"
    FETCH_MISSING_SELECTED = "fetch_missing_selected"
    FETCH_MISSING_REMAINING = "fetch_missing_remaining"
    REFRESH_SELECTED = "refresh_selected"
    REFRESH_REMAINING = "refresh_remaining"


class MarketTranslationStatus(StrEnum):
    BLOCKED_SOURCE = "blocked_source"
    CURRENT = "current"
    NEEDED_SELECTED = "needed_selected"
    NEEDED_REMAINING = "needed_remaining"
    UNAVAILABLE_PROVIDER = "unavailable_provider"


class MarketAnalysisStatus(StrEnum):
    BLOCKED_SOURCE = "blocked_source"
    BLOCKED_TRANSLATION = "blocked_translation"
    CURRENT_ACCEPTED = "current_accepted"
    CURRENT_PENDING_REVIEW = "current_pending_review"
    NEEDED_SELECTED = "needed_selected"
    NEEDED_REMAINING = "needed_remaining"
    UNAVAILABLE_MODEL = "unavailable_model"


@dataclass(frozen=True, slots=True)
class MarketCandidateAffectedWork:
    """Deterministic current planning state for one target candidate."""

    source_job_id: str
    title: str | None
    company_slug: str
    lifecycle_state: str
    source_status: str
    source_action: str
    source_eligible: bool
    job_detail_version_id: int | None
    latest_detail_at: str | None
    latest_observation_outcome: str | None
    warnings: tuple[str, ...]
    translation_status: str
    translation_artifact_id: int | None
    analysis_status: str
    analysis_artifact_id: int | None
    analysis_review_status: str | None


@dataclass(frozen=True, slots=True)
class MarketAffectedWorkPlan:
    """One exact target-only affected-work plan before mutable stage execution."""

    target_definition_version_id: int
    candidate_ids: tuple[str, ...]
    candidates: tuple[MarketCandidateAffectedWork, ...]
    missing_selected: tuple[str, ...]
    missing_remaining: tuple[str, ...]
    refresh_selected: tuple[str, ...]
    refresh_remaining: tuple[str, ...]
    source_ready: tuple[str, ...]
    translation_reused: tuple[str, ...]
    translation_selected: tuple[str, ...]
    translation_remaining: tuple[str, ...]
    translation_unavailable: tuple[str, ...]
    analysis_current_accepted: tuple[str, ...]
    analysis_current_pending: tuple[str, ...]
    analysis_selected: tuple[str, ...]
    analysis_remaining: tuple[str, ...]
    analysis_unavailable: tuple[str, ...]
    latest_failed_refresh: tuple[str, ...]

    def ledger(self) -> dict[str, dict[str, int]]:
        """Return deterministic counts suitable for the later Market run ledger."""

        source_blocked = len(self.candidate_ids) - len(self.source_ready)
        translation_blocked = sum(
            item.translation_status == MarketTranslationStatus.BLOCKED_SOURCE
            for item in self.candidates
        )
        analysis_blocked = sum(
            item.analysis_status
            in {
                MarketAnalysisStatus.BLOCKED_SOURCE,
                MarketAnalysisStatus.BLOCKED_TRANSLATION,
            }
            for item in self.candidates
        )
        return {
            "source": {
                "candidate": len(self.candidate_ids),
                "ready": len(self.source_ready),
                "blocked": source_blocked,
                "missing_selected": len(self.missing_selected),
                "missing_remaining": len(self.missing_remaining),
                "refresh_selected": len(self.refresh_selected),
                "refresh_remaining": len(self.refresh_remaining),
                "latest_failed_refresh": len(self.latest_failed_refresh),
            },
            "translation": {
                "reused": len(self.translation_reused),
                "selected": len(self.translation_selected),
                "remaining": len(self.translation_remaining),
                "unavailable": len(self.translation_unavailable),
                "blocked_source": translation_blocked,
            },
            "analysis": {
                "current_accepted": len(self.analysis_current_accepted),
                "current_pending_review": len(self.analysis_current_pending),
                "selected": len(self.analysis_selected),
                "remaining": len(self.analysis_remaining),
                "unavailable": len(self.analysis_unavailable),
                "blocked": analysis_blocked,
            },
        }


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _as_utc(raw: str) -> datetime:
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _normalize_candidate_ids(values: tuple[str, ...]) -> tuple[str, ...]:
    normalized = tuple(
        dict.fromkeys(value.strip() for value in values if value.strip())
    )
    if len(normalized) > 5000:
        raise MarketPlanningError("At most 5000 target candidates may be planned at once")
    return normalized


class MarketAffectedWorkPlanner:
    """Plan exact target-only source, translation, and P1.6 affected work."""

    def __init__(
        self,
        *,
        market_store: MarketStore,
        source_store: JobHunterStore,
        observations: JobDetailObservationStore,
        translation_store: TranslationStore,
        translation_service: TranslationService,
        analysis_store: AnalysisStore,
        analysis_model: str | None,
        clock=_utc_now,
    ) -> None:
        self._market_store = market_store
        self._source_store = source_store
        self._observations = observations
        self._translation_store = translation_store
        self._translation_service = translation_service
        self._analysis_store = analysis_store
        self._analysis_model = analysis_model.strip() if analysis_model else None
        self._clock = clock

    def plan(
        self,
        *,
        target_definition_version_id: int,
        candidate_source_job_ids: tuple[str, ...],
        missing_limit: int,
        refresh_limit: int,
        refresh_after_hours: float,
        translation_limit: int,
        analysis_limit: int,
    ) -> MarketAffectedWorkPlan:
        """Build one read-only plan constrained to the supplied target candidates."""

        if not 0 <= missing_limit <= 50:
            raise ValueError("missing_limit must be between 0 and 50")
        if not 0 <= refresh_limit <= 50:
            raise ValueError("refresh_limit must be between 0 and 50")
        if missing_limit + refresh_limit > 50:
            raise ValueError("combined missing and refresh limits may not exceed 50")
        if refresh_after_hours <= 0:
            raise ValueError("refresh_after_hours must be greater than zero")
        if not 0 <= translation_limit <= 50:
            raise ValueError("translation_limit must be between 0 and 50")
        if not 0 <= analysis_limit <= 20:
            raise ValueError("analysis_limit must be between 0 and 20")

        definition = self._market_store.get_definition_version(
            target_definition_version_id
        )
        if definition is None:
            raise LookupError(
                f"Unknown Market target definition {target_definition_version_id}"
            )
        if definition.spec.source != "jobinja":
            raise MarketPlanningError("Market I2 supports only the approved Jobinja source")
        if definition.spec.freshness_rule != "current-active":
            raise MarketPlanningError(
                "Market I2 currently supports only freshness_rule='current-active'"
            )

        candidate_ids = _normalize_candidate_ids(candidate_source_job_ids)
        if not candidate_ids:
            return self._empty_plan(target_definition_version_id)

        self._source_store.initialize()
        self._observations.initialize()
        self._translation_store.initialize()
        self._analysis_store.initialize()

        now = self._clock().astimezone(UTC)
        cutoff = now - timedelta(hours=refresh_after_hours)
        state: dict[str, dict[str, Any]] = {}
        missing_candidates: list[str] = []
        invalid_detail_candidates: list[str] = []
        refresh_due_candidates: list[str] = []
        latest_failed_refresh: list[str] = []

        for source_job_id in candidate_ids:
            posting = self._source_store.get_job(source_job_id)
            if posting is None:
                raise MarketPlanningError(
                    "Target candidate IDs must come from persisted Jobinja discovery; "
                    f"unknown candidate {source_job_id!r}"
                )
            detail = self._source_store.get_latest_job_detail(source_job_id)
            latest_observations = self._observations.list_for_job(
                source_job_id,
                limit=1,
            )
            latest_observation = latest_observations[0] if latest_observations else None
            latest_outcome = latest_observation.outcome if latest_observation else None
            warnings: list[str] = []
            if latest_outcome == "failed":
                latest_failed_refresh.append(source_job_id)
                warnings.append(
                    "latest detail refresh failed; prior valid source evidence is retained"
                )

            source_status: MarketSourceStatus
            source_action = MarketSourceAction.NONE
            source_eligible = False
            current_source_version = None

            if posting.lifecycle_state == "expired":
                source_status = MarketSourceStatus.EXPIRED
            elif posting.lifecycle_state == "removed":
                source_status = MarketSourceStatus.REMOVED
            elif posting.lifecycle_state not in {"active", "possibly_unavailable"}:
                source_status = MarketSourceStatus.INELIGIBLE_LIFECYCLE
                warnings.append(
                    f"unsupported lifecycle state {posting.lifecycle_state!r}; excluded"
                )
            elif detail is None:
                source_status = MarketSourceStatus.MISSING_DETAIL
                missing_candidates.append(source_job_id)
            elif detail.parse_status != "parsed":
                source_status = MarketSourceStatus.INVALID_CURRENT_DETAIL
                invalid_detail_candidates.append(source_job_id)
            else:
                current_source_version = self._translation_store.latest_source_version(
                    source_job_id
                )
                if current_source_version is None:
                    raise RuntimeError(
                        "Parsed current source disappeared from TranslationStore currentness"
                    )
                last_success_raw = self._observations.latest_successful_check_at(
                    source_job_id
                )
                freshness_at = _as_utc(last_success_raw or detail.fetched_at)
                if freshness_at <= cutoff:
                    source_status = MarketSourceStatus.REFRESH_DUE
                    refresh_due_candidates.append(source_job_id)
                    warnings.append(
                        "valid source evidence is older than the target refresh threshold"
                    )
                else:
                    source_status = MarketSourceStatus.CURRENT
                    source_eligible = True
                    if posting.lifecycle_state == "possibly_unavailable":
                        warnings.append(
                            "posting is possibly unavailable; recent valid evidence is retained"
                        )

            state[source_job_id] = {
                "source_job_id": source_job_id,
                "title": posting.title_observed,
                "company_slug": posting.company_slug,
                "lifecycle_state": posting.lifecycle_state,
                "source_status": source_status,
                "source_action": source_action,
                "source_eligible": source_eligible,
                "job_detail_version_id": (
                    current_source_version.job_detail_version_id
                    if current_source_version is not None
                    else None
                ),
                "latest_detail_at": detail.fetched_at if detail is not None else None,
                "latest_observation_outcome": latest_outcome,
                "warnings": warnings,
                "translation_status": MarketTranslationStatus.BLOCKED_SOURCE,
                "translation_artifact_id": None,
                "analysis_status": MarketAnalysisStatus.BLOCKED_SOURCE,
                "analysis_artifact_id": None,
                "analysis_review_status": None,
            }

        missing_selected = tuple(missing_candidates[:missing_limit])
        missing_remaining = tuple(missing_candidates[missing_limit:])
        invalid_set = set(invalid_detail_candidates)
        refresh_candidates = tuple(
            [*invalid_detail_candidates]
            + [
                source_job_id
                for source_job_id in refresh_due_candidates
                if source_job_id not in invalid_set
            ]
        )
        refresh_selected = tuple(refresh_candidates[:refresh_limit])
        refresh_remaining = tuple(refresh_candidates[refresh_limit:])

        for source_job_id in missing_selected:
            state[source_job_id]["source_action"] = (
                MarketSourceAction.FETCH_MISSING_SELECTED
            )
        for source_job_id in missing_remaining:
            state[source_job_id]["source_action"] = (
                MarketSourceAction.FETCH_MISSING_REMAINING
            )
        for source_job_id in refresh_selected:
            state[source_job_id]["source_action"] = MarketSourceAction.REFRESH_SELECTED
        for source_job_id in refresh_remaining:
            state[source_job_id]["source_action"] = MarketSourceAction.REFRESH_REMAINING

        source_ready = tuple(
            source_job_id
            for source_job_id in candidate_ids
            if bool(state[source_job_id]["source_eligible"])
        )

        translation_needed: list[str] = []
        translation_reused: list[str] = []
        translation_unavailable: list[str] = []
        for source_job_id in source_ready:
            source = self._translation_store.latest_source_version(source_job_id)
            if source is None:
                raise RuntimeError("Source-ready job lost its current parsed source version")
            try:
                self._translation_service.effective_identity_for_source(source)
            except TranslationProviderUnavailableError:
                state[source_job_id]["translation_status"] = (
                    MarketTranslationStatus.UNAVAILABLE_PROVIDER
                )
                state[source_job_id]["analysis_status"] = (
                    MarketAnalysisStatus.BLOCKED_TRANSLATION
                )
                translation_unavailable.append(source_job_id)
                continue
            artifact = self._translation_service.current_artifact(source_job_id)
            if artifact is not None:
                state[source_job_id]["translation_status"] = (
                    MarketTranslationStatus.CURRENT
                )
                state[source_job_id]["translation_artifact_id"] = artifact.id
                translation_reused.append(source_job_id)
            else:
                translation_needed.append(source_job_id)

        translation_selected = tuple(translation_needed[:translation_limit])
        translation_remaining = tuple(translation_needed[translation_limit:])
        for source_job_id in translation_selected:
            state[source_job_id]["translation_status"] = (
                MarketTranslationStatus.NEEDED_SELECTED
            )
            state[source_job_id]["analysis_status"] = (
                MarketAnalysisStatus.BLOCKED_TRANSLATION
            )
        for source_job_id in translation_remaining:
            state[source_job_id]["translation_status"] = (
                MarketTranslationStatus.NEEDED_REMAINING
            )
            state[source_job_id]["analysis_status"] = (
                MarketAnalysisStatus.BLOCKED_TRANSLATION
            )

        analysis_needed: list[str] = []
        analysis_current_accepted: list[str] = []
        analysis_current_pending: list[str] = []
        analysis_unavailable: list[str] = []
        for source_job_id in translation_reused:
            translation_artifact_id = state[source_job_id]["translation_artifact_id"]
            if not isinstance(translation_artifact_id, int):
                raise RuntimeError("Current translation identity disappeared during planning")
            if self._analysis_model is None:
                state[source_job_id]["analysis_status"] = (
                    MarketAnalysisStatus.UNAVAILABLE_MODEL
                )
                analysis_unavailable.append(source_job_id)
                continue
            artifact = self._analysis_store.latest_current(
                source_job_id,
                model=self._analysis_model,
                prompt_version=ENGLISH_PROMPT_VERSION,
                schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
                translation_artifact_id=translation_artifact_id,
                require_translation_dependency=True,
            )
            if artifact is None:
                analysis_needed.append(source_job_id)
                continue
            state[source_job_id]["analysis_artifact_id"] = artifact.id
            state[source_job_id]["analysis_review_status"] = (
                artifact.semantic_review_status
            )
            if artifact.semantic_review_status == SEMANTIC_REVIEW_ACCEPTED:
                state[source_job_id]["analysis_status"] = (
                    MarketAnalysisStatus.CURRENT_ACCEPTED
                )
                analysis_current_accepted.append(source_job_id)
            elif artifact.semantic_review_status == SEMANTIC_REVIEW_PENDING:
                state[source_job_id]["analysis_status"] = (
                    MarketAnalysisStatus.CURRENT_PENDING_REVIEW
                )
                analysis_current_pending.append(source_job_id)
            else:
                raise RuntimeError(
                    "Current P1.6 artifact has an unsupported semantic review state"
                )

        analysis_selected = tuple(analysis_needed[:analysis_limit])
        analysis_remaining = tuple(analysis_needed[analysis_limit:])
        for source_job_id in analysis_selected:
            state[source_job_id]["analysis_status"] = (
                MarketAnalysisStatus.NEEDED_SELECTED
            )
        for source_job_id in analysis_remaining:
            state[source_job_id]["analysis_status"] = (
                MarketAnalysisStatus.NEEDED_REMAINING
            )

        candidates = tuple(
            MarketCandidateAffectedWork(
                source_job_id=source_job_id,
                title=state[source_job_id]["title"],
                company_slug=str(state[source_job_id]["company_slug"]),
                lifecycle_state=str(state[source_job_id]["lifecycle_state"]),
                source_status=str(state[source_job_id]["source_status"]),
                source_action=str(state[source_job_id]["source_action"]),
                source_eligible=bool(state[source_job_id]["source_eligible"]),
                job_detail_version_id=state[source_job_id]["job_detail_version_id"],
                latest_detail_at=state[source_job_id]["latest_detail_at"],
                latest_observation_outcome=state[source_job_id][
                    "latest_observation_outcome"
                ],
                warnings=tuple(state[source_job_id]["warnings"]),
                translation_status=str(state[source_job_id]["translation_status"]),
                translation_artifact_id=state[source_job_id][
                    "translation_artifact_id"
                ],
                analysis_status=str(state[source_job_id]["analysis_status"]),
                analysis_artifact_id=state[source_job_id]["analysis_artifact_id"],
                analysis_review_status=state[source_job_id][
                    "analysis_review_status"
                ],
            )
            for source_job_id in candidate_ids
        )

        return MarketAffectedWorkPlan(
            target_definition_version_id=target_definition_version_id,
            candidate_ids=candidate_ids,
            candidates=candidates,
            missing_selected=missing_selected,
            missing_remaining=missing_remaining,
            refresh_selected=refresh_selected,
            refresh_remaining=refresh_remaining,
            source_ready=source_ready,
            translation_reused=tuple(translation_reused),
            translation_selected=translation_selected,
            translation_remaining=translation_remaining,
            translation_unavailable=tuple(translation_unavailable),
            analysis_current_accepted=tuple(analysis_current_accepted),
            analysis_current_pending=tuple(analysis_current_pending),
            analysis_selected=analysis_selected,
            analysis_remaining=analysis_remaining,
            analysis_unavailable=tuple(analysis_unavailable),
            latest_failed_refresh=tuple(latest_failed_refresh),
        )

    @staticmethod
    def _empty_plan(target_definition_version_id: int) -> MarketAffectedWorkPlan:
        return MarketAffectedWorkPlan(
            target_definition_version_id=target_definition_version_id,
            candidate_ids=(),
            candidates=(),
            missing_selected=(),
            missing_remaining=(),
            refresh_selected=(),
            refresh_remaining=(),
            source_ready=(),
            translation_reused=(),
            translation_selected=(),
            translation_remaining=(),
            translation_unavailable=(),
            analysis_current_accepted=(),
            analysis_current_pending=(),
            analysis_selected=(),
            analysis_remaining=(),
            analysis_unavailable=(),
            latest_failed_refresh=(),
        )
