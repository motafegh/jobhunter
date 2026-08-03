import json
import sqlite3
from pathlib import Path

from jobhunter.analysis_store import AnalysisStore
from jobhunter.translation_store import TranslationStore


def _create_legacy_source_database(database_path: Path) -> None:
    fields_json = json.dumps(
        {
            "title": "Legacy Python role",
            "description": "Build APIs",
            "language": "en",
            "parser_version": "jobinja-detail-v1",
        },
        sort_keys=True,
    )
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
            INSERT INTO job_postings(
                source, source_job_id, company_slug, canonical_url, title_observed,
                first_seen_at, last_seen_at
            ) VALUES (
                'jobinja', 'legacy1', 'acme',
                'https://jobinja.ir/companies/acme/jobs/legacy1/example',
                'Legacy Python role',
                '2026-07-31T12:00:00+00:00',
                '2026-07-31T12:00:00+00:00'
            );
            """
        )
        connection.execute(
            """
            INSERT INTO job_detail_versions(
                job_posting_id, fetched_at, requested_url, final_url, status_code,
                content_sha256, evidence_path, metadata_path, parser_version,
                parse_status, fields_json
            ) VALUES (1, ?, ?, ?, 200, ?, ?, ?, ?, 'parsed', ?)
            """,
            (
                "2026-07-31T12:00:00+00:00",
                "https://example",
                "https://example",
                "raw-legacy",
                "page.html",
                "page.json",
                "jobinja-detail-v1",
                fields_json,
            ),
        )


def _table_names(database_path: Path) -> set[str]:
    with sqlite3.connect(database_path) as connection:
        return {
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }


def test_translation_store_initialization_migrates_legacy_source_schema_first(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    _create_legacy_source_database(database_path)

    TranslationStore(database_path).initialize()

    tables = _table_names(database_path)
    assert "job_translation_artifacts" in tables
    assert "job_translation_attempts" in tables
    with sqlite3.connect(database_path) as connection:
        columns = {
            str(row[1])
            for row in connection.execute("PRAGMA table_info(job_detail_versions)")
        }
        row = connection.execute(
            "SELECT source_job_id FROM job_postings WHERE id = 1"
        ).fetchone()
        semantic = connection.execute(
            "SELECT semantic_sha256 FROM job_detail_versions WHERE id = 1"
        ).fetchone()

    assert "semantic_sha256" in columns
    assert row == ("legacy1",)
    assert semantic is not None and semantic[0]


def test_analysis_store_initialization_builds_full_dependency_chain_on_legacy_db(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    _create_legacy_source_database(database_path)

    AnalysisStore(database_path).initialize()

    tables = _table_names(database_path)
    assert {
        "job_translation_artifacts",
        "job_translation_attempts",
        "job_analysis_artifacts",
        "job_analysis_attempts",
    } <= tables
    with sqlite3.connect(database_path) as connection:
        legacy_count = connection.execute(
            "SELECT COUNT(*) FROM job_detail_versions"
        ).fetchone()[0]
        semantic = connection.execute(
            "SELECT semantic_sha256 FROM job_detail_versions WHERE id = 1"
        ).fetchone()[0]

    assert legacy_count == 1
    assert semantic
