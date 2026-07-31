"""Application service for one-job Jobinja detail acquisition and inspection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from jobhunter.evidence import EvidenceStore
from jobhunter.jobinja_details import (
    PARSER_VERSION,
    ParsedJobDetail,
    parse_jobinja_detail,
)
from jobhunter.sources import JobinjaClient
from jobhunter.storage import JobDetailView, JobHunterStore


class JobNotFoundError(LookupError):
    """Raised when a requested source job has not been discovered locally."""


@dataclass(frozen=True, slots=True)
class JobDetailFetchSummary:
    source_job_id: str
    title: str | None
    version_id: int
    is_new_version: bool
    parse_status: str
    evidence_path: str


class JobinjaDetailService:
    """Fetch, preserve, parse, and persist one discovered Jobinja job page."""

    def __init__(
        self,
        *,
        client: JobinjaClient,
        evidence_store: EvidenceStore,
        store: JobHunterStore,
    ) -> None:
        self._client = client
        self._evidence_store = evidence_store
        self._store = store

    def fetch(self, source_job_id: str) -> JobDetailFetchSummary:
        self._store.initialize()
        job = self._store.get_job(source_job_id)
        if job is None:
            raise JobNotFoundError(
                f"Job {source_job_id!r} is not in the local database. "
                "Run discovery first."
            )

        fetched_at = datetime.now(UTC)
        page = self._client.fetch_job_page(job.canonical_url)
        snapshot = self._evidence_store.write_jobinja_job_page(
            source_job_id=source_job_id,
            fetched_page=page,
            captured_at=fetched_at,
        )
        parsed = parse_jobinja_detail(page.text)
        parse_status = _parse_status(parsed)
        result = self._store.record_job_detail(
            job_posting_id=job.id,
            fetched_at=fetched_at,
            requested_url=page.requested_url,
            final_url=page.final_url,
            status_code=page.status_code,
            content_sha256=snapshot.content_sha256,
            evidence_path=snapshot.content_path,
            metadata_path=snapshot.metadata_path,
            parser_version=PARSER_VERSION,
            parse_status=parse_status,
            fields=parsed.to_dict(),
        )
        return JobDetailFetchSummary(
            source_job_id=source_job_id,
            title=parsed.title or job.title_observed,
            version_id=result.version_id,
            is_new_version=result.is_new_version,
            parse_status=parse_status,
            evidence_path=str(snapshot.content_path),
        )

    def show(self, source_job_id: str) -> JobDetailView:
        self._store.initialize()
        detail = self._store.get_latest_job_detail(source_job_id)
        if detail is None:
            job = self._store.get_job(source_job_id)
            if job is None:
                raise JobNotFoundError(
                    f"Job {source_job_id!r} is not in the local database."
                )
            raise JobNotFoundError(
                f"Job {source_job_id!r} has no local detail page. "
                f"Run: jobhunter jobinja fetch {source_job_id}"
            )
        return detail


def _parse_status(detail: ParsedJobDetail) -> str:
    if detail.title and detail.description:
        return "parsed"
    if detail.title or detail.description or detail.company or detail.location:
        return "partial"
    return "parse_failed"


def format_fetch_summary(summary: JobDetailFetchSummary) -> str:
    version_state = (
        "new content version"
        if summary.is_new_version
        else "unchanged content"
    )
    return "\n".join(
        [
            f"Jobinja job fetched: {summary.source_job_id}",
            f"Title: {summary.title or '(not extracted)'}",
            f"Result: {version_state}",
            f"Parse status: {summary.parse_status}",
            f"Version ID: {summary.version_id}",
            f"Raw evidence: {summary.evidence_path}",
        ]
    )


def format_job_detail(detail: JobDetailView) -> str:
    fields = detail.fields
    lines = [
        f"Job: {detail.source_job_id}",
        (
            "Title: "
            f"{fields.get('title') or detail.title_observed or '(not available)'}"
        ),
        f"Company: {fields.get('company') or '(not available)'}",
        f"Category: {fields.get('job_category') or '(not available)'}",
        f"Location: {fields.get('location') or '(not available)'}",
        (
            "Employment type: "
            f"{fields.get('employment_type') or '(not available)'}"
        ),
        (
            "Minimum experience: "
            f"{fields.get('minimum_experience') or '(not available)'}"
        ),
        f"Education: {fields.get('education') or '(not available)'}",
        f"Salary: {fields.get('salary') or '(not available)'}",
        f"Gender: {fields.get('gender') or '(not available)'}",
        (
            "Military service: "
            f"{fields.get('military_service') or '(not available)'}"
        ),
        f"Date posted: {fields.get('date_posted') or '(not available)'}",
        f"Valid through: {fields.get('valid_through') or '(not available)'}",
        f"Language: {fields.get('language') or 'unknown'}",
        f"Parse status: {detail.parse_status}",
        "",
        "Required skill tags:",
    ]
    skills = fields.get("skills") or []
    lines.extend(f"- {skill}" for skill in skills)
    if not skills:
        lines.append("(not available)")

    lines.extend(
        [
            "",
            "Job description:",
            fields.get("description") or "(not available)",
        ]
    )
    if fields.get("company_description"):
        lines.extend(
            [
                "",
                "Company description:",
                str(fields["company_description"]),
            ]
        )
    lines.extend(
        [
            "",
            f"Source URL: {detail.final_url}",
            f"Fetched at: {detail.fetched_at}",
            f"Content SHA-256: {detail.content_sha256}",
            f"Raw evidence: {detail.evidence_path}",
            f"Metadata: {detail.metadata_path}",
        ]
    )
    return "\n".join(lines)
