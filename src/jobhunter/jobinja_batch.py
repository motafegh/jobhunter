"""Bounded sequential batch acquisition for discovered Jobinja jobs."""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from jobhunter.evidence import EvidenceWriteError
from jobhunter.jobinja_detail_service import (
    JobDetailFetchSummary,
    JobinjaDetailService,
    JobNotFoundError,
)
from jobhunter.sources import JobinjaAcquisitionError


@dataclass(frozen=True, slots=True)
class BatchFetchFailure:
    """One isolated job-detail acquisition failure."""

    source_job_id: str
    error: str


@dataclass(frozen=True, slots=True)
class JobinjaBatchFetchSummary:
    """Result of one bounded sequential detail-fetch batch."""

    attempted: int
    results: tuple[JobDetailFetchSummary, ...]
    failures: tuple[BatchFetchFailure, ...]

    @property
    def succeeded(self) -> int:
        return len(self.results)

    @property
    def new_versions(self) -> int:
        return sum(1 for result in self.results if result.is_new_version)

    @property
    def unchanged(self) -> int:
        return self.succeeded - self.new_versions


class JobinjaBatchFetchService:
    """Fetch several jobs sequentially while isolating per-job failures."""

    def __init__(
        self,
        *,
        detail_service: JobinjaDetailService,
        request_delay_seconds: float,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if request_delay_seconds < 0:
            raise ValueError("request_delay_seconds must not be negative")
        self._detail_service = detail_service
        self._request_delay_seconds = request_delay_seconds
        self._sleep = sleep

    def run(self, job_ids: Sequence[str]) -> JobinjaBatchFetchSummary:
        """Fetch unique job IDs in order with a delay between requests."""

        cleaned_ids = (job_id.strip() for job_id in job_ids if job_id.strip())
        unique_job_ids = tuple(dict.fromkeys(cleaned_ids))
        if not unique_job_ids:
            raise ValueError("At least one Jobinja job ID is required")
        if len(unique_job_ids) > 50:
            raise ValueError("A batch may contain at most 50 jobs")

        results: list[JobDetailFetchSummary] = []
        failures: list[BatchFetchFailure] = []
        for index, source_job_id in enumerate(unique_job_ids):
            if index and self._request_delay_seconds > 0:
                self._sleep(self._request_delay_seconds)
            try:
                results.append(self._detail_service.fetch(source_job_id))
            except (
                EvidenceWriteError,
                JobNotFoundError,
                JobinjaAcquisitionError,
                OSError,
            ) as exc:
                failures.append(
                    BatchFetchFailure(
                        source_job_id=source_job_id,
                        error=str(exc),
                    )
                )

        return JobinjaBatchFetchSummary(
            attempted=len(unique_job_ids),
            results=tuple(results),
            failures=tuple(failures),
        )


def format_batch_fetch_summary(summary: JobinjaBatchFetchSummary) -> str:
    """Format one batch result without hiding individual outcomes."""

    lines = [
        "Jobinja detail fetch batch",
        f"Attempted: {summary.attempted}",
        f"Succeeded: {summary.succeeded}",
        f"New semantic versions: {summary.new_versions}",
        f"Unchanged semantic content: {summary.unchanged}",
        f"Failures: {len(summary.failures)}",
    ]
    if summary.results:
        lines.append("Results:")
        for result in summary.results:
            state = "new version" if result.is_new_version else "unchanged"
            lines.append(
                f"- {result.source_job_id}: {state}, "
                f"version {result.version_id}, {result.parse_status}"
            )
    if summary.failures:
        lines.append("Failure details:")
        lines.extend(
            f"- {failure.source_job_id}: {failure.error}"
            for failure in summary.failures
        )
    return "\n".join(lines)
