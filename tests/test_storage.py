import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore


def test_job_upsert_is_repeat_safe(tmp_path: Path) -> None:
    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
    store.initialize()
    observed_at = datetime(2026, 7, 31, 12, 0, tzinfo=UTC)
    job = DiscoveredJobLink(
        source_job_id="tpLF",
        company_slug="aseh-tejarat-asia",
        canonical_url=(
            "https://jobinja.ir/companies/aseh-tejarat-asia/jobs/tpLF/example-title"
        ),
        observed_text="AI Developer",
    )

    first = store.upsert_job(job=job, observed_at=observed_at)
    second = store.upsert_job(job=job, observed_at=observed_at)

    assert first.is_new is True
    assert second.is_new is False
    assert first.job_posting_id == second.job_posting_id
    assert store.count_job_postings() == 1


def test_non_latin_title_or_company_text_never_controls_logical_job_identity(
    tmp_path: Path,
) -> None:
    store = JobHunterStore(tmp_path / "jobhunter.sqlite3")
    store.initialize()
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)

    first = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="fa-1",
            company_slug="company-one",
            canonical_url="https://jobinja.ir/companies/company-one/jobs/fa-1/example",
            observed_text="مهندس امنیت هوش مصنوعی",
        ),
        observed_at=observed_at,
    )
    second = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="fa-2",
            company_slug="company-two",
            canonical_url="https://jobinja.ir/companies/company-two/jobs/fa-2/example",
            observed_text="مهندس امنیت هوش مصنوعی",
        ),
        observed_at=observed_at,
    )

    assert first.job_posting_id != second.job_posting_id
    assert store.count_job_postings() == 2
    assert store.get_job("fa-1").source_job_id == "fa-1"
    assert store.get_job("fa-2").source_job_id == "fa-2"


def test_initialize_migrates_legacy_detail_versions_to_semantic_hashes(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    fields = {
        "title": "Python Developer",
        "description": "Build APIs",
        "language": "en",
        "parser_version": "jobinja-detail-v1",
    }
    fields_json = json.dumps(fields, ensure_ascii=False, sort_keys=True)

    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE job_postings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                source_job_id TEXT NOT NULL,
                company_slug TEXT NOT NULL,
                canonical_url TEXT NOT NULL,
                title_observed TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL DEFAULT 'active',
                UNIQUE(source, source_job_id)
            );
            CREATE TABLE job_detail_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_posting_id INTEGER NOT NULL,
                fetched_at TEXT NOT NULL,
                requested_url TEXT NOT NULL,
                final_url TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                content_sha256 TEXT NOT NULL,
                evidence_path TEXT NOT NULL,
                metadata_path TEXT NOT NULL,
                parser_version TEXT NOT NULL,
                parse_status TEXT NOT NULL,
                fields_json TEXT NOT NULL,
                FOREIGN KEY(job_posting_id) REFERENCES job_postings(id),
                UNIQUE(job_posting_id, content_sha256)
            );
            """
        )
        connection.execute(
            """
            INSERT INTO job_postings(
                source,
                source_job_id,
                company_slug,
                canonical_url,
                title_observed,
                first_seen_at,
                last_seen_at
            ) VALUES (
                'jobinja',
                'abc1',
                'acme',
                'https://jobinja.ir/companies/acme/jobs/abc1/python',
                'Python Developer',
                '2026-07-31T12:00:00+00:00',
                '2026-07-31T12:00:00+00:00'
            )
            """
        )
        for raw_hash in ("raw-one", "raw-two"):
            connection.execute(
                """
                INSERT INTO job_detail_versions(
                    job_posting_id,
                    fetched_at,
                    requested_url,
                    final_url,
                    status_code,
                    content_sha256,
                    evidence_path,
                    metadata_path,
                    parser_version,
                    parse_status,
                    fields_json
                ) VALUES (
                    1,
                    '2026-07-31T12:00:00+00:00',
                    'https://example',
                    'https://example',
                    200,
                    ?,
                    'page.html',
                    'page.json',
                    'jobinja-detail-v1',
                    'parsed',
                    ?
                )
                """,
                (raw_hash, fields_json),
            )

    store = JobHunterStore(database_path)
    store.initialize()

    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(
            "SELECT id, semantic_sha256 FROM job_detail_versions ORDER BY id"
        ).fetchall()

    assert len(rows) == 2
    assert rows[0][1]
    assert rows[0][1] == rows[1][1]

    result = store.record_job_detail(
        job_posting_id=1,
        fetched_at=datetime.now(UTC),
        requested_url="https://example",
        final_url="https://example",
        status_code=200,
        content_sha256="raw-three",
        semantic_sha256=str(rows[0][1]),
        evidence_path=Path("new-page.html"),
        metadata_path=Path("new-page.json"),
        parser_version="jobinja-detail-v1",
        parse_status="parsed",
        fields=fields,
    )

    assert result.is_new_version is False
    assert result.version_id == 2
    assert store.count_job_detail_versions("abc1") == 2
