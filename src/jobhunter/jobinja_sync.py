"""Acquisition-only Jobinja synchronization workflow.

This service composes already accepted discovery, detail acquisition, refresh
selection, and deterministic parser audit. It deliberately stops before local
LLM analysis so acquisition remains independently operable.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from jobhunter.job_audit import JobAuditReport, JobDetailAuditor
from jobhunter.job_catalog import JobCatalog
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_batch import JobinjaBatchFetchService, JobinjaBatchFetchSummary
from jobhunter.jobinja_discovery import (
    DiscoverySearch,
    DiscoverySummary,
    JobinjaDiscoveryService,
    format_discovery_summary,
)


@dataclass(frozen=True, slots=True)
class JobinjaSyncSummary:
    """Combined result of one bounded acquisition-only synchronization."""

    discovery: DiscoverySummary
    missing_selected: tuple[str, ...]
    refresh_selected: tuple[str, ...]
    detail_fetch: JobinjaBatchFetchSummary | None
    audit: JobAuditReport

    @property
    def succeeded(self) -> bool:
        detail_failures = self.detail_fetch.failures if self.detail_fetch else ()
        return not self.discovery.failures and not detail_failures and not self.audit.needs_review


def _utc_now() -> datetime:
    return datetime.now(UTC)


class JobinjaSyncService:
    """Run bounded discovery, detail acquisition, and local structural audit."""

    def __init__(
        self,
        *,
        discovery_service: JobinjaDiscoveryService,
        batch_service: JobinjaBatchFetchService,
        catalog: JobCatalog,
        observations: JobDetailObservationStore,
        auditor: JobDetailAuditor,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._discovery_service = discovery_service
        self._batch_service = batch_service
        self._catalog = catalog
        self._observations = observations
        self._auditor = auditor
        self._clock = clock

    def run(
        self,
        searches: Sequence[DiscoverySearch],
        *,
        missing_limit: int,
        refresh_limit: int,
        refresh_after_hours: float,
    ) -> JobinjaSyncSummary:
        """Execute one acquisition-only sync with a maximum of 50 detail checks."""

        if not 0 <= missing_limit <= 50:
            raise ValueError("missing_limit must be between 0 and 50")
        if not 0 <= refresh_limit <= 50:
            raise ValueError("refresh_limit must be between 0 and 50")
        if missing_limit + refresh_limit > 50:
            raise ValueError("combined missing and refresh limits may not exceed 50")
        if refresh_after_hours <= 0:
            raise ValueError("refresh_after_hours must be greater than zero")

        discovery = self._discovery_service.run(searches)
        missing_selected = (
            self._catalog.missing_job_ids(limit=missing_limit)
            if missing_limit
            else ()
        )
        refresh_candidates = (
            self._observations.refresh_due_job_ids(
                as_of=self._clock(),
                older_than_hours=refresh_after_hours,
                limit=refresh_limit + len(missing_selected),
            )
            if refresh_limit
            else ()
        )
        missing_set = set(missing_selected)
        refresh_selected = tuple(
            job_id
            for job_id in refresh_candidates
            if job_id not in missing_set
        )[:refresh_limit]

        selected = (*missing_selected, *refresh_selected)
        detail_fetch = self._batch_service.run(selected) if selected else None
        audit = self._auditor.audit(limit=500)
        return JobinjaSyncSummary(
            discovery=discovery,
            missing_selected=missing_selected,
            refresh_selected=refresh_selected,
            detail_fetch=detail_fetch,
            audit=audit,
        )


def format_sync_summary(summary: JobinjaSyncSummary) -> str:
    """Format one acquisition sync without dumping every parsed description."""

    lines = [
        "JobHunter acquisition sync",
        "",
        format_discovery_summary(summary.discovery),
        "",
        "Detail selection:",
        f"Missing selected: {len(summary.missing_selected)}",
        f"Refresh-due selected: {len(summary.refresh_selected)}",
    ]

    if summary.detail_fetch is None:
        lines.append("No detail pages selected.")
    else:
        detail = summary.detail_fetch
        lines.extend(
            [
                f"Detail checks attempted: {detail.attempted}",
                f"Detail checks succeeded: {detail.succeeded}",
                f"New semantic versions: {detail.new_versions}",
                f"Unchanged semantic content: {detail.unchanged}",
                f"Detail failures: {len(detail.failures)}",
            ]
        )
        if detail.failures:
            lines.append("Detail failure summary:")
            lines.extend(
                f"- {failure.source_job_id}: {failure.error}"
                for failure in detail.failures
            )

    lines.extend(
        [
            "",
            "Parser audit:",
            f"Jobs audited: {summary.audit.jobs_audited}",
            f"No structural findings: {summary.audit.clean}",
            f"Needs review: {summary.audit.needs_review}",
            "",
            f"Sync status: {'ok' if summary.succeeded else 'attention required'}",
        ]
    )
    return "\n".join(lines)
