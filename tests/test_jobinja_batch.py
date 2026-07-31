from jobhunter.jobinja_batch import (
    JobinjaBatchFetchService,
    format_batch_fetch_summary,
)
from jobhunter.jobinja_detail_service import JobDetailFetchSummary, JobNotFoundError


class _FakeDetailService:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def fetch(self, source_job_id: str) -> JobDetailFetchSummary:
        self.calls.append(source_job_id)
        if source_job_id == "missing":
            raise JobNotFoundError("not found")
        return JobDetailFetchSummary(
            source_job_id=source_job_id,
            title=f"Title {source_job_id}",
            version_id=1,
            is_new_version=source_job_id != "known",
            parse_status="parsed",
            evidence_path=f"{source_job_id}.html",
        )


def test_batch_deduplicates_delays_and_isolates_failures() -> None:
    detail_service = _FakeDetailService()
    sleeps: list[float] = []
    service = JobinjaBatchFetchService(
        detail_service=detail_service,  # type: ignore[arg-type]
        request_delay_seconds=1.5,
        sleep=sleeps.append,
    )

    summary = service.run(["abc1", "missing", "known", "abc1"])

    assert detail_service.calls == ["abc1", "missing", "known"]
    assert sleeps == [1.5, 1.5]
    assert summary.attempted == 3
    assert summary.succeeded == 2
    assert summary.new_versions == 1
    assert summary.unchanged == 1
    assert [failure.source_job_id for failure in summary.failures] == ["missing"]

    rendered = format_batch_fetch_summary(summary)
    assert "Attempted: 3" in rendered
    assert "New semantic versions: 1" in rendered
    assert "missing: not found" in rendered
