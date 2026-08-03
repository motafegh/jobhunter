"""Application service for one-job Jobinja detail acquisition and inspection."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from jobhunter.evidence import EvidenceStore, EvidenceWriteError
from jobhunter.job_detail_observations import JobDetailObservationStore
from jobhunter.jobinja_details import PARSER_VERSION, ParsedJobDetail, parse_jobinja_detail
from jobhunter.lifecycle import LifecycleStore
from jobhunter.sources import JobinjaAcquisitionError, JobinjaClient
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
    observation_id: int
    checked_at: str


class JobinjaDetailService:
    """Fetch, preserve, parse, and persist one discovered Jobinja job page."""

    def __init__(
        self,
        *,
        client: JobinjaClient,
        evidence_store: EvidenceStore,
        store: JobHunterStore,
        observation_store: JobDetailObservationStore,
        lifecycle_store: LifecycleStore | None = None,
    ) -> None:
        self._client = client
        self._evidence_store = evidence_store
        self._store = store
        self._observation_store = observation_store
        self._lifecycle_store = lifecycle_store

    def _record_lifecycle(
        self,
        source_job_id: str,
        *,
        classification: str,
        checked_at: datetime,
        status_code: int | None = None,
        retryable: bool = False,
        detail: str | None = None,
    ) -> None:
        if self._lifecycle_store is None:
            return
        self._lifecycle_store.record(
            source_job_id,
            classification=classification,
            status_code=status_code,
            retryable=retryable,
            detail=detail,
            checked_at=checked_at,
        )

    def fetch(self, source_job_id: str) -> JobDetailFetchSummary:
        self._store.initialize()
        self._observation_store.initialize()
        if self._lifecycle_store is not None:
            self._lifecycle_store.initialize()
        job = self._store.get_job(source_job_id)
        if job is None:
            raise JobNotFoundError(
                f"Job {source_job_id!r} is not in the local database. Run discovery first."
            )

        checked_at = datetime.now(UTC)
        try:
            page = self._client.fetch_job_page(job.canonical_url)
            snapshot = self._evidence_store.write_jobinja_job_page(
                source_job_id=source_job_id,
                fetched_page=page,
                captured_at=checked_at,
            )
        except (EvidenceWriteError, JobinjaAcquisitionError, OSError) as exc:
            self._observation_store.record_failure(
                job_posting_id=job.id,
                checked_at=checked_at,
                requested_url=job.canonical_url,
                error=exc,
            )
            if isinstance(exc, JobinjaAcquisitionError):
                self._record_lifecycle(
                    source_job_id,
                    classification=exc.classification,
                    checked_at=checked_at,
                    status_code=exc.status_code,
                    retryable=exc.retryable,
                    detail=str(exc),
                )
            else:
                self._record_lifecycle(
                    source_job_id,
                    classification="unknown_error",
                    checked_at=checked_at,
                    detail=str(exc),
                )
            raise

        if page.classification != "active":
            error = JobinjaAcquisitionError(
                f"Jobinja page classified as {page.classification}",
                classification=page.classification,
                status_code=page.status_code,
                retryable=False,
            )
            self._observation_store.record_failure(
                job_posting_id=job.id,
                checked_at=checked_at,
                requested_url=page.requested_url,
                error=error,
            )
            self._record_lifecycle(
                source_job_id,
                classification=page.classification,
                checked_at=checked_at,
                status_code=page.status_code,
                detail=f"Raw evidence: {snapshot.content_path}",
            )
            raise error

        parsed = parse_jobinja_detail(page.text)
        fields = parsed.to_dict()
        semantic_sha256 = _semantic_sha256(fields)
        parse_status = _parse_status(parsed)
        result = self._store.record_job_detail(
            job_posting_id=job.id,
            fetched_at=checked_at,
            requested_url=page.requested_url,
            final_url=page.final_url,
            status_code=page.status_code,
            content_sha256=snapshot.content_sha256,
            semantic_sha256=semantic_sha256,
            evidence_path=snapshot.content_path,
            metadata_path=snapshot.metadata_path,
            parser_version=PARSER_VERSION,
            parse_status=parse_status,
            fields=fields,
        )
        observation_id = self._observation_store.record_success(
            job_posting_id=job.id,
            checked_at=checked_at,
            requested_url=page.requested_url,
            final_url=page.final_url,
            status_code=page.status_code,
            content_sha256=snapshot.content_sha256,
            semantic_sha256=semantic_sha256,
            evidence_path=snapshot.content_path,
            metadata_path=snapshot.metadata_path,
            parser_version=PARSER_VERSION,
            parse_status=parse_status,
            job_detail_version_id=result.version_id,
            is_new_version=result.is_new_version,
        )
        self._record_lifecycle(
            source_job_id,
            classification="active",
            checked_at=checked_at,
            status_code=page.status_code,
            detail=f"Parsed status: {parse_status}",
        )
        return JobDetailFetchSummary(
            source_job_id=source_job_id,
            title=parsed.title or job.title_observed,
            version_id=result.version_id,
            is_new_version=result.is_new_version,
            parse_status=parse_status,
            evidence_path=str(snapshot.content_path),
            observation_id=observation_id,
            checked_at=checked_at.isoformat(),
        )

    def show(self, source_job_id: str) -> JobDetailView:
        self._store.initialize()
        detail = self._store.get_latest_job_detail(source_job_id)
        if detail is None:
            job = self._store.get_job(source_job_id)
            if job is None:
                raise JobNotFoundError(f"Job {source_job_id!r} is not in the local database.")
            raise JobNotFoundError(
                f"Job {source_job_id!r} has no local detail page. "
                f"Run: jobhunter jobinja fetch {source_job_id}"
            )
        return detail


def _semantic_sha256(fields: dict[str, Any]) -> str:
    semantic_fields = {
        key: value
        for key, value in fields.items()
        if key not in {"language", "parser_version"}
    }
    canonical = json.dumps(
        semantic_fields,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


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
        else "unchanged semantic content"
    )
    return "\n".join(
        [
            f"Jobinja job fetched: {summary.source_job_id}",
            f"Title: {summary.title or '(not extracted)'}",
            f"Result: {version_state}",
            f"Parse status: {summary.parse_status}",
            f"Version ID: {summary.version_id}",
            f"Fetch observation ID: {summary.observation_id}",
            f"Checked at: {summary.checked_at}",
            f"Raw evidence: {summary.evidence_path}",
        ]
    )


def format_job_detail(detail: JobDetailView) -> str:
    fields = detail.fields
    lines = [
        f"Job: {detail.source_job_id}",
        f"Title: {fields.get('title') or detail.title_observed or '(not available)'}",
        f"Company: {fields.get('company') or '(not available)'}",
        f"Category: {fields.get('job_category') or '(not available)'}",
        f"Location: {fields.get('location') or '(not available)'}",
        f"Employment type: {fields.get('employment_type') or '(not available)'}",
        f"Minimum experience: {fields.get('minimum_experience') or '(not available)'}",
        f"Education: {fields.get('education') or '(not available)'}",
        f"Salary: {fields.get('salary') or '(not available)'}",
        f"Gender: {fields.get('gender') or '(not available)'}",
        f"Military service: {fields.get('military_service') or '(not available)'}",
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

    lines.extend(["", "Job description:", fields.get("description") or "(not available)"])
    if fields.get("company_description"):
        lines.extend(["", "Company description:", str(fields["company_description"])])
    lines.extend(
        [
            "",
            f"Source URL: {detail.final_url}",
            f"Semantic version first recorded at: {detail.fetched_at}",
            f"Semantic SHA-256: {detail.semantic_sha256}",
            f"Version evidence raw HTML SHA-256: {detail.content_sha256}",
            f"Version-defining raw evidence: {detail.evidence_path}",
            f"Version-defining metadata: {detail.metadata_path}",
        ]
    )
    return "\n".join(lines)
