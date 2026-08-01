"""Human-facing summaries for the local JobHunter browser application."""

from __future__ import annotations

from jobhunter.jobinja_sync import JobinjaSyncSummary


def format_web_sync_summary(summary: JobinjaSyncSummary) -> str:
    """Format a market sync for normal app use without per-search debug noise."""

    discovery = summary.discovery
    detail = summary.detail_fetch
    lines = [
        "Market sync completed",
        f"Status: {'OK' if summary.succeeded else 'Attention required'}",
        "",
        "Search coverage",
        f"- Search terms tried: {discovery.searches_attempted}",
        (
            f"- Search-page requests: {discovery.requests_attempted} "
            f"/ budget {discovery.request_budget}"
        ),
        f"- Unique postings found this run: {discovery.unique_jobs}",
        f"- New to your local catalog: {discovery.new_jobs}",
        f"- Already known locally: {discovery.known_jobs}",
        (
            f"- Cross-search matches: {discovery.cross_search_overlaps} "
            "(the same posting matched more than one search term)"
        ),
        f"- Search failures: {len(discovery.failures)}",
        "",
        "Source details",
        f"- New postings selected for full fetch: {len(summary.missing_selected)}",
        f"- Existing postings selected for recheck: {len(summary.refresh_selected)}",
    ]

    if detail is None:
        lines.append("- No full job pages were selected in this run")
    else:
        lines.extend(
            [
                f"- Detail checks succeeded: {detail.succeeded} / {detail.attempted}",
                f"- New semantic content versions: {detail.new_versions}",
                f"- Unchanged semantic content: {detail.unchanged}",
                f"- Detail failures: {len(detail.failures)}",
            ]
        )
        if detail.failures:
            lines.append("- Failed Jobinja references:")
            lines.extend(
                f"  - {failure.source_job_id}: {failure.error}"
                for failure in detail.failures
            )

    lines.extend(
        [
            "",
            "Parser health",
            f"- Current jobs audited: {summary.audit.jobs_audited}",
            f"- Structurally clean: {summary.audit.clean}",
            f"- Need review: {summary.audit.needs_review}",
            "",
            "What this means",
            (
                "- Cross-search matches are expected: one useful posting can match several "
                "Persian/English search phrases without becoming duplicate database rows."
            ),
            (
                "- Discovery adds logical postings cheaply; only the bounded detail selection "
                "downloads and parses complete job pages."
            ),
        ]
    )
    return "\n".join(lines)
