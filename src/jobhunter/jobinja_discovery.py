"""Phase 1 Jobinja search discovery orchestration."""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime

from jobhunter.evidence import EvidenceStore, EvidenceWriteError
from jobhunter.sources import (
    DiscoveredJobLink,
    JobinjaAcquisitionError,
    JobinjaClient,
    JobinjaUrlError,
    canonicalize_search_url,
    extract_job_links,
)
from jobhunter.storage import JobHunterStore


@dataclass(frozen=True, slots=True)
class DiscoverySearch:
    """One enabled Jobinja search executed by a discovery run."""

    name: str
    url: str
    max_pages: int = 1


@dataclass(frozen=True, slots=True)
class DiscoverySummary:
    """User-facing result of one bounded Jobinja discovery run."""

    run_id: int
    searches_attempted: int
    pages_fetched: int
    unique_jobs: int
    new_jobs: int
    known_jobs: int
    failures: tuple[str, ...]
    newly_discovered: tuple[DiscoveredJobLink, ...]

    @property
    def succeeded(self) -> bool:
        return not self.failures


def _utc_now() -> datetime:
    return datetime.now(UTC)


class JobinjaDiscoveryService:
    """Acquire search pages, preserve evidence, and persist discovered jobs."""

    def __init__(
        self,
        *,
        client: JobinjaClient,
        evidence_store: EvidenceStore,
        store: JobHunterStore,
        request_delay_seconds: float,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._client = client
        self._evidence_store = evidence_store
        self._store = store
        self._request_delay_seconds = request_delay_seconds
        self._sleep = sleep
        self._clock = clock

    def run(self, searches: Sequence[DiscoverySearch]) -> DiscoverySummary:
        """Run enabled searches without requiring LM Studio."""

        if not searches:
            raise ValueError("At least one Jobinja search is required")

        self._store.initialize()
        started_at = self._clock()
        run_id = self._store.start_run(source="jobinja", started_at=started_at)

        pages_fetched = 0
        failures: list[str] = []
        run_jobs: dict[str, bool] = {}
        newly_discovered: list[DiscoveredJobLink] = []

        for search_index, search in enumerate(searches):
            try:
                canonical_search_url = canonicalize_search_url(search.url)
            except JobinjaUrlError as exc:
                failures.append(f"{search.name}: {exc}")
                continue

            self._store.upsert_search(
                source="jobinja",
                name=search.name,
                canonical_url=canonical_search_url,
                enabled=True,
                max_pages=search.max_pages,
                observed_at=started_at,
            )

            for page_number in range(1, search.max_pages + 1):
                if (search_index > 0 or page_number > 1) and self._request_delay_seconds > 0:
                    self._sleep(self._request_delay_seconds)

                try:
                    fetched_page = self._client.fetch_search_page(
                        canonical_search_url,
                        page_number,
                    )
                    captured_at = self._clock()
                    snapshot = self._evidence_store.write_jobinja_search_page(
                        search_name=search.name,
                        page_number=page_number,
                        fetched_page=fetched_page,
                        captured_at=captured_at,
                    )
                    links = extract_job_links(
                        fetched_page.text,
                        base_url=fetched_page.final_url,
                    )
                    self._store.record_search_page(
                        run_id=run_id,
                        search_name=search.name,
                        page_number=page_number,
                        requested_url=fetched_page.requested_url,
                        final_url=fetched_page.final_url,
                        fetched_at=captured_at,
                        status_code=fetched_page.status_code,
                        content_sha256=snapshot.content_sha256,
                        evidence_path=snapshot.content_path,
                        metadata_path=snapshot.metadata_path,
                        discovered_count=len(links),
                    )
                except (JobinjaAcquisitionError, JobinjaUrlError, EvidenceWriteError) as exc:
                    failures.append(f"{search.name} page {page_number}: {exc}")
                    break

                pages_fetched += 1
                for link in links:
                    upserted = self._store.upsert_job(job=link, observed_at=captured_at)
                    self._store.record_discovery(
                        run_id=run_id,
                        job_posting_id=upserted.job_posting_id,
                        search_name=search.name,
                        page_number=page_number,
                        discovered_at=captured_at,
                    )
                    if link.source_job_id in run_jobs:
                        continue
                    run_jobs[link.source_job_id] = upserted.is_new
                    if upserted.is_new:
                        newly_discovered.append(link)

                if not links:
                    break

        new_jobs = sum(1 for is_new in run_jobs.values() if is_new)
        known_jobs = len(run_jobs) - new_jobs
        completed_at = self._clock()
        status = "completed" if not failures else "completed_with_errors"
        self._store.complete_run(
            run_id=run_id,
            completed_at=completed_at,
            status=status,
            searches_attempted=len(searches),
            pages_fetched=pages_fetched,
            jobs_discovered=len(run_jobs),
            new_jobs=new_jobs,
            known_jobs=known_jobs,
            failures=len(failures),
            error_summary="\n".join(failures) if failures else None,
        )

        return DiscoverySummary(
            run_id=run_id,
            searches_attempted=len(searches),
            pages_fetched=pages_fetched,
            unique_jobs=len(run_jobs),
            new_jobs=new_jobs,
            known_jobs=known_jobs,
            failures=tuple(failures),
            newly_discovered=tuple(newly_discovered),
        )


def format_discovery_summary(
    summary: DiscoverySummary,
    *,
    show_jobs: bool = False,
) -> str:
    """Format a concise terminal report for one discovery run."""

    lines = [
        f"Jobinja discovery run: {summary.run_id}",
        f"Searches attempted: {summary.searches_attempted}",
        f"Pages fetched: {summary.pages_fetched}",
        f"Unique jobs discovered: {summary.unique_jobs}",
        f"New jobs: {summary.new_jobs}",
        f"Known jobs: {summary.known_jobs}",
        f"Failures: {len(summary.failures)}",
    ]

    if show_jobs and summary.newly_discovered:
        lines.append("Newly discovered jobs:")
        lines.extend(
            f"- {job.source_job_id}: {job.canonical_url}"
            for job in summary.newly_discovered
        )

    if summary.failures:
        lines.append("Failure details:")
        lines.extend(f"- {failure}" for failure in summary.failures)

    return "\n".join(lines)
