"""Deterministic quality audit for locally parsed Jobinja details."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jobhunter.jobinja_details import PARSER_VERSION
from jobhunter.storage import JobHunterStore

_REQUIRED_FIELDS = ("title", "description")
_COVERAGE_FIELDS = (
    "company",
    "job_category",
    "location",
    "employment_type",
    "minimum_experience",
    "education",
    "salary",
    "gender",
    "military_service",
    "skills",
)
_SCALAR_FIELDS = (
    "title",
    "company",
    "job_category",
    "location",
    "employment_type",
    "minimum_experience",
    "education",
    "salary",
    "gender",
    "military_service",
    "date_posted",
    "valid_through",
)
_UI_CONTAMINATION_MARKERS = (
    "مشاغل مشابه",
    "اطلاع‌رسانی از طریق ایمیل",
    "پشتیبان سایت",
    "ارسال رزومه",
    "ورود / ثبت‌نام",
    "فرصت‌های شغلی",
)


@dataclass(frozen=True, slots=True)
class AuditFinding:
    """One deterministic reason a parsed job should be reviewed."""

    code: str
    message: str


@dataclass(frozen=True, slots=True)
class JobAuditEntry:
    """Compact parser-quality result for one local semantic version."""

    source_job_id: str
    title: str | None
    parse_status: str
    parser_version: str
    description_characters: int
    skill_count: int
    covered_fields: int
    total_coverage_fields: int
    missing_coverage_fields: tuple[str, ...]
    findings: tuple[AuditFinding, ...]

    @property
    def needs_review(self) -> bool:
        return bool(self.findings)


@dataclass(frozen=True, slots=True)
class JobAuditReport:
    """Audit results across a bounded set of locally available jobs."""

    entries: tuple[JobAuditEntry, ...]

    @property
    def jobs_audited(self) -> int:
        return len(self.entries)

    @property
    def clean(self) -> int:
        return sum(1 for entry in self.entries if not entry.needs_review)

    @property
    def needs_review(self) -> int:
        return self.jobs_audited - self.clean


class JobDetailAuditor:
    """Inspect latest local semantic versions without network or model calls."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def audit(
        self,
        *,
        source_job_ids: tuple[str, ...] = (),
        limit: int = 50,
    ) -> JobAuditReport:
        """Audit latest details for explicit IDs or all locally available jobs."""

        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")

        JobHunterStore(self._database_path).initialize()
        requested = tuple(dict.fromkeys(job_id.strip() for job_id in source_job_ids if job_id.strip()))
        requested_set = set(requested)

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    p.source_job_id,
                    p.title_observed,
                    v.parse_status,
                    v.parser_version,
                    v.fields_json
                FROM job_postings AS p
                JOIN job_detail_versions AS v
                  ON v.id = (
                      SELECT latest.id
                      FROM job_detail_versions AS latest
                      WHERE latest.job_posting_id = p.id
                      ORDER BY latest.id DESC
                      LIMIT 1
                  )
                WHERE p.source = 'jobinja'
                ORDER BY p.id ASC
                """
            ).fetchall()

        by_id = {str(row["source_job_id"]): row for row in rows}
        if requested:
            selected_rows = [by_id[job_id] for job_id in requested if job_id in by_id]
        else:
            selected_rows = list(rows)

        entries = tuple(_audit_row(row) for row in selected_rows[:limit])
        return JobAuditReport(entries=entries)


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return bool(value)
    return True


def _audit_row(row: sqlite3.Row) -> JobAuditEntry:
    fields = json.loads(str(row["fields_json"]))
    findings: list[AuditFinding] = []

    parse_status = str(row["parse_status"])
    parser_version = str(row["parser_version"])
    if parse_status != "parsed":
        findings.append(
            AuditFinding(
                code="parse-status",
                message=f"parse status is {parse_status!r}, not 'parsed'",
            )
        )
    if parser_version != PARSER_VERSION:
        findings.append(
            AuditFinding(
                code="parser-version",
                message=f"stored parser {parser_version!r} differs from current {PARSER_VERSION!r}",
            )
        )

    for field in _REQUIRED_FIELDS:
        if not _present(fields.get(field)):
            findings.append(
                AuditFinding(
                    code=f"missing-{field}",
                    message=f"required field {field!r} is missing",
                )
            )

    description = fields.get("description")
    description_text = description if isinstance(description, str) else ""
    if description_text and len(description_text.strip()) < 40:
        findings.append(
            AuditFinding(
                code="short-description",
                message="description is shorter than 40 characters",
            )
        )

    for field in _SCALAR_FIELDS:
        value = fields.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            findings.append(
                AuditFinding(
                    code=f"non-scalar-{field}",
                    message=f"field {field!r} contains {type(value).__name__}, expected text",
                )
            )
            continue
        stripped = value.strip()
        if len(stripped) > 240 and field not in {"title", "company"}:
            findings.append(
                AuditFinding(
                    code=f"long-scalar-{field}",
                    message=f"field {field!r} is implausibly long ({len(stripped)} characters)",
                )
            )
        if any(marker in stripped for marker in _UI_CONTAMINATION_MARKERS):
            findings.append(
                AuditFinding(
                    code=f"ui-contamination-{field}",
                    message=f"field {field!r} contains unrelated page-interface text",
                )
            )
        if stripped.startswith(("{'", '[{"')):
            findings.append(
                AuditFinding(
                    code=f"mapping-repr-{field}",
                    message=f"field {field!r} looks like a serialized Python mapping",
                )
            )

    skills = fields.get("skills") or []
    if not isinstance(skills, list):
        findings.append(
            AuditFinding(
                code="non-list-skills",
                message="skills must be a list of source tags",
            )
        )
        skills = []
    else:
        for skill in skills:
            if not isinstance(skill, str):
                findings.append(
                    AuditFinding(
                        code="non-text-skill",
                        message="skills contains a non-text value",
                    )
                )
                break
            if len(skill.strip()) > 120:
                findings.append(
                    AuditFinding(
                        code="long-skill",
                        message="a skill tag is implausibly long",
                    )
                )
                break

    missing_coverage_fields = tuple(
        field for field in _COVERAGE_FIELDS if not _present(fields.get(field))
    )
    covered_fields = len(_COVERAGE_FIELDS) - len(missing_coverage_fields)

    return JobAuditEntry(
        source_job_id=str(row["source_job_id"]),
        title=fields.get("title") or row["title_observed"],
        parse_status=parse_status,
        parser_version=parser_version,
        description_characters=len(description_text.strip()),
        skill_count=len(skills),
        covered_fields=covered_fields,
        total_coverage_fields=len(_COVERAGE_FIELDS),
        missing_coverage_fields=missing_coverage_fields,
        findings=tuple(findings),
    )


def format_job_audit(report: JobAuditReport, *, only_issues: bool = False) -> str:
    """Format a compact audit suitable for terminal review."""

    visible_entries = tuple(
        entry for entry in report.entries if not only_issues or entry.needs_review
    )
    lines = [
        "Local Jobinja detail parser audit",
        f"Jobs audited: {report.jobs_audited}",
        f"No structural findings: {report.clean}",
        f"Needs review: {report.needs_review}",
    ]
    if only_issues:
        lines.append(f"Entries shown: {len(visible_entries)}")
    if not visible_entries:
        lines.append("No matching audit entries.")
        return "\n".join(lines)

    lines.append("Jobs:")
    for entry in visible_entries:
        state = "review" if entry.needs_review else "ok"
        title = entry.title or "(title unavailable)"
        lines.append(
            f"- {entry.source_job_id} [{state}] {title}"
        )
        lines.append(
            "  "
            f"parser={entry.parser_version}; description={entry.description_characters} chars; "
            f"skills={entry.skill_count}; coverage={entry.covered_fields}/"
            f"{entry.total_coverage_fields}"
        )
        if entry.missing_coverage_fields:
            lines.append(
                "  coverage gaps: " + ", ".join(entry.missing_coverage_fields)
            )
        for finding in entry.findings:
            lines.append(f"  review: {finding.message}")
    return "\n".join(lines)
