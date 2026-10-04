"""Shared service for durable bounded Market role-family intelligence reports."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from jobhunter.config import Settings
from jobhunter.market_candidate_report import (
    PROMPT_VERSION,
    REPORT_CONTRACT,
    PreparedMarketCandidateReport,
    generate_market_candidate_report,
    prepare_market_candidate_report,
)
from jobhunter.market_models import (
    MarketRoleFamilyIntelligenceReport,
    MarketRoleFamilyReportAttempt,
    MarketRoleFamilyReportReview,
    MarketRoleFamilyReportReviewDisposition,
)
from jobhunter.market_role_family_report_store import MarketRoleFamilyReportStore


def _utc_now() -> datetime:
    return datetime.now(UTC)


class MarketRoleFamilyReportService:
    """Compose accepted V6 generation with immutable report persistence."""

    def __init__(
        self,
        settings: Settings,
        *,
        store: MarketRoleFamilyReportStore | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._settings = settings
        self._store = store or MarketRoleFamilyReportStore(settings.database_path)
        self._clock = clock or _utc_now

    def generate_report(
        self,
        snapshot_id: int,
        *,
        model_override: str | None = None,
        regenerate: bool = False,
    ) -> MarketRoleFamilyIntelligenceReport:
        """Return exact reusable report or generate/persist a new immutable artifact."""

        prepared = prepare_market_candidate_report(
            self._settings,
            snapshot_id,
            model_override=model_override,
        )
        if not regenerate:
            reusable = self._find_reusable(prepared)
            if reusable is not None:
                self._record_attempt(
                    prepared,
                    outcome="reused",
                    artifact_id=reusable.id,
                )
                return reusable

        attempted_at = self._clock()
        try:
            generated = generate_market_candidate_report(
                self._settings,
                prepared,
            )
            self._validate_generated_report(prepared, generated.report)
        except Exception as exc:
            self._record_attempt(
                prepared,
                outcome="failed",
                attempted_at=attempted_at,
                error=exc,
            )
            raise

        artifact = self._store.record_report(
            snapshot_id=prepared.snapshot_id,
            candidate_contract_version=REPORT_CONTRACT,
            prompt_version=PROMPT_VERSION,
            model=prepared.model,
            generation_identity=prepared.generation_identity,
            candidate_input=prepared.candidate_input,
            report=generated.report,
            request_body=generated.request_body,
            raw_response=generated.raw_response,
            created_at=self._clock(),
        )
        self._record_attempt(
            prepared,
            outcome="completed",
            attempted_at=attempted_at,
            artifact_id=artifact.id,
        )
        return artifact

    def review_report(
        self,
        report_artifact_id: int,
        *,
        disposition: MarketRoleFamilyReportReviewDisposition | str,
        note: str | None = None,
        reviewed_at: datetime | None = None,
    ) -> MarketRoleFamilyReportReview:
        return self._store.record_review(
            report_artifact_id=report_artifact_id,
            disposition=disposition,
            note=note,
            reviewed_at=reviewed_at or self._clock(),
        )

    def effective_review_state(self, report_artifact_id: int) -> str:
        return self._store.effective_review_state(report_artifact_id)

    def latest_accepted_report(
        self,
        snapshot_id: int,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        return self._store.latest_accepted_for_snapshot(snapshot_id)

    def get_report(
        self,
        report_artifact_id: int,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        return self._store.get_report(report_artifact_id)

    def list_reports(
        self,
        snapshot_id: int,
    ) -> tuple[MarketRoleFamilyIntelligenceReport, ...]:
        return self._store.list_reports(snapshot_id)

    def list_attempts(
        self,
        snapshot_id: int,
    ) -> tuple[MarketRoleFamilyReportAttempt, ...]:
        return self._store.list_attempts(snapshot_id)

    def list_reviews(
        self,
        report_artifact_id: int,
    ) -> tuple[MarketRoleFamilyReportReview, ...]:
        return self._store.list_reviews(report_artifact_id)

    @staticmethod
    def _validate_generated_report(
        prepared: PreparedMarketCandidateReport,
        report: dict,
    ) -> None:
        expected = {
            "contract": REPORT_CONTRACT,
            "prompt_version": PROMPT_VERSION,
            "snapshot_id": prepared.snapshot_id,
            "model": prepared.model,
        }
        for field, value in expected.items():
            if report.get(field) != value:
                raise ValueError(
                    f"Generated candidate report {field} does not match prepared identity"
                )

    def _find_reusable(
        self,
        prepared: PreparedMarketCandidateReport,
    ) -> MarketRoleFamilyIntelligenceReport | None:
        return self._store.find_reusable_report(
            snapshot_id=prepared.snapshot_id,
            candidate_contract_version=REPORT_CONTRACT,
            prompt_version=PROMPT_VERSION,
            model=prepared.model,
            generation_identity=prepared.generation_identity,
            candidate_input=prepared.candidate_input,
        )

    def _record_attempt(
        self,
        prepared: PreparedMarketCandidateReport,
        *,
        outcome: str,
        attempted_at: datetime | None = None,
        artifact_id: int | None = None,
        error: Exception | None = None,
    ) -> MarketRoleFamilyReportAttempt:
        return self._store.record_attempt(
            snapshot_id=prepared.snapshot_id,
            attempted_at=attempted_at or self._clock(),
            candidate_contract_version=REPORT_CONTRACT,
            prompt_version=PROMPT_VERSION,
            model=prepared.model,
            generation_identity=prepared.generation_identity,
            candidate_input=prepared.candidate_input,
            outcome=outcome,
            artifact_id=artifact_id,
            error=error,
        )


__all__ = ["MarketRoleFamilyReportService"]
