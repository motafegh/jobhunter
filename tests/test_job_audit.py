from datetime import UTC, datetime
from pathlib import Path

from jobhunter.job_audit import JobDetailAuditor, format_job_audit
from jobhunter.jobinja_details import PARSER_VERSION
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def _store_detail(
    database_path: Path,
    *,
    source_job_id: str,
    fields: dict,
    parse_status: str = "parsed",
    parser_version: str = PARSER_VERSION,
) -> None:
    store = JobHunterStore(database_path)
    store.initialize()
    job = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=source_job_id,
            company_slug="acme",
            canonical_url=(
                f"https://jobinja.ir/companies/acme/jobs/{source_job_id}/example"
            ),
            observed_text=fields.get("title"),
        ),
        observed_at=datetime(2026, 7, 31, 12, 0, tzinfo=UTC),
    )
    store.record_job_detail(
        job_posting_id=job.job_posting_id,
        fetched_at=datetime(2026, 7, 31, 12, 5, tzinfo=UTC),
        requested_url="https://jobinja.ir/example",
        final_url="https://jobinja.ir/example",
        status_code=200,
        content_sha256=f"raw-{source_job_id}",
        semantic_sha256=f"semantic-{source_job_id}",
        evidence_path=Path(f"{source_job_id}.html"),
        metadata_path=Path(f"{source_job_id}.json"),
        parser_version=parser_version,
        parse_status=parse_status,
        fields=fields,
    )


def test_audits_clean_latest_detail(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _store_detail(
        database_path,
        source_job_id="abc1",
        fields={
            "title": "AI Engineer",
            "company": "Acme",
            "job_category": "Software",
            "location": "Tehran",
            "employment_type": "Full time",
            "minimum_experience": "Three years",
            "education": "Bachelor",
            "salary": "Negotiable",
            "gender": "Any",
            "military_service": "Not specified",
            "skills": ["Python", "Linux"],
            "description": (
                "Design, build, test, and maintain reliable artificial intelligence services."
            ),
        },
    )

    report = JobDetailAuditor(database_path).audit()

    assert report.jobs_audited == 1
    assert report.clean == 1
    assert report.needs_review == 0
    assert report.entries[0].covered_fields == 10
    assert report.entries[0].findings == ()
    assert "abc1 [ok] AI Engineer" in format_job_audit(report)


def test_flags_structural_contamination_and_parser_drift(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _store_detail(
        database_path,
        source_job_id="xyz2",
        fields={
            "title": "Security Engineer",
            "location": {"@type": "Country", "name": "IR"},
            "education": "کارشناسی | مشاغل مشابه | اطلاع‌رسانی از طریق ایمیل",
            "skills": "Python",
            "description": "Short text",
        },
        parse_status="partial",
        parser_version="jobinja-detail-v1",
    )

    report = JobDetailAuditor(database_path).audit(source_job_ids=("xyz2",))
    codes = {finding.code for finding in report.entries[0].findings}

    assert report.needs_review == 1
    assert "parse-status" in codes
    assert "parser-version" in codes
    assert "short-description" in codes
    assert "non-scalar-location" in codes
    assert "ui-contamination-education" in codes
    assert "non-list-skills" in codes


def test_preserves_explicit_audit_order(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    common_fields = {
        "title": "Example",
        "description": "A sufficiently detailed source description for deterministic audit.",
        "skills": [],
    }
    _store_detail(database_path, source_job_id="first", fields=common_fields)
    _store_detail(database_path, source_job_id="second", fields=common_fields)

    report = JobDetailAuditor(database_path).audit(
        source_job_ids=("second", "first", "second"),
    )

    assert [entry.source_job_id for entry in report.entries] == ["second", "first"]
