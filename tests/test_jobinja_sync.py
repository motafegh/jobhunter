from datetime import UTC, datetime

from jobhunter.job_audit import JobAuditReport
from jobhunter.jobinja_batch import JobinjaBatchFetchSummary
from jobhunter.jobinja_detail_service import JobDetailFetchSummary
from jobhunter.jobinja_discovery import DiscoverySummary
from jobhunter.jobinja_sync import JobinjaSyncService, format_sync_summary


class _Discovery:
    def run(self, searches):
        return DiscoverySummary(
            run_id=7,
            searches_attempted=len(searches),
            pages_fetched=2,
            unique_jobs=3,
            new_jobs=2,
            known_jobs=1,
            cross_search_overlaps=0,
            request_budget=10,
            requests_attempted=2,
            search_summaries=(),
            failures=(),
            newly_discovered=(),
        )


class _Catalog:
    def missing_job_ids(self, *, limit: int):
        return ("new1", "new2")[:limit]


class _Observations:
    def refresh_due_job_ids(self, *, as_of, older_than_hours: float, limit: int):
        assert as_of.tzinfo is not None
        assert older_than_hours == 24
        return ("old1", "old2")[:limit]


class _Batch:
    def __init__(self) -> None:
        self.selected = ()

    def run(self, job_ids):
        self.selected = tuple(job_ids)
        results = tuple(
            JobDetailFetchSummary(
                source_job_id=job_id,
                title=job_id,
                version_id=index,
                is_new_version=job_id.startswith("new"),
                parse_status="parsed",
                evidence_path=f"{job_id}.html",
                observation_id=index,
                checked_at="2026-08-01T00:00:00+00:00",
            )
            for index, job_id in enumerate(self.selected, start=1)
        )
        return JobinjaBatchFetchSummary(
            attempted=len(results),
            results=results,
            failures=(),
        )


class _Auditor:
    def audit(self, *, limit: int):
        assert limit == 500
        return JobAuditReport(entries=())


def test_sync_composes_discovery_missing_refresh_and_audit() -> None:
    batch = _Batch()
    service = JobinjaSyncService(
        discovery_service=_Discovery(),  # type: ignore[arg-type]
        batch_service=batch,  # type: ignore[arg-type]
        catalog=_Catalog(),  # type: ignore[arg-type]
        observations=_Observations(),  # type: ignore[arg-type]
        auditor=_Auditor(),  # type: ignore[arg-type]
        clock=lambda: datetime(2026, 8, 1, tzinfo=UTC),
    )

    summary = service.run(
        [object(), object()],  # type: ignore[list-item]
        missing_limit=2,
        refresh_limit=1,
        refresh_after_hours=24,
    )

    assert summary.missing_selected == ("new1", "new2")
    assert summary.refresh_selected == ("old1",)
    assert batch.selected == ("new1", "new2", "old1")
    assert summary.detail_fetch is not None
    assert summary.detail_fetch.new_versions == 2
    assert summary.detail_fetch.unchanged == 1
    assert summary.succeeded is True
    rendered = format_sync_summary(summary)
    assert "Missing selected: 2" in rendered
    assert "Refresh-due selected: 1" in rendered
    assert "Sync status: ok" in rendered


def test_sync_rejects_detail_selection_over_fifty() -> None:
    service = JobinjaSyncService(
        discovery_service=_Discovery(),  # type: ignore[arg-type]
        batch_service=_Batch(),  # type: ignore[arg-type]
        catalog=_Catalog(),  # type: ignore[arg-type]
        observations=_Observations(),  # type: ignore[arg-type]
        auditor=_Auditor(),  # type: ignore[arg-type]
    )

    try:
        service.run(
            [object()],  # type: ignore[list-item]
            missing_limit=30,
            refresh_limit=21,
            refresh_after_hours=24,
        )
    except ValueError as exc:
        assert "may not exceed 50" in str(exc)
    else:
        raise AssertionError("expected ValueError")
