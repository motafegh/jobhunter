from jobhunter.job_audit import JobAuditReport
from jobhunter.jobinja_discovery import DiscoverySummary
from jobhunter.jobinja_sync import JobinjaSyncSummary
from jobhunter.web.presentation import format_web_sync_summary


def test_web_sync_summary_explains_overlap_without_per_search_dump() -> None:
    discovery = DiscoverySummary(
        run_id=6,
        searches_attempted=40,
        pages_fetched=40,
        unique_jobs=273,
        new_jobs=241,
        known_jobs=32,
        cross_search_overlaps=468,
        request_budget=40,
        requests_attempted=40,
        discovered_job_ids=(),
        search_summaries=(),
        failures=(),
        newly_discovered=(),
    )
    summary = JobinjaSyncSummary(
        discovery=discovery,
        missing_selected=(),
        refresh_selected=(),
        detail_fetch=None,
        audit=JobAuditReport(entries=()),
    )

    output = format_web_sync_summary(summary)

    assert "Unique postings found this run: 273" in output
    assert "New to your local catalog: 241" in output
    assert "Cross-search matches: 468" in output
    assert "same posting matched more than one search term" in output
    assert "Search summaries:" not in output
