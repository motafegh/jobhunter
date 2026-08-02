import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def test_translation_store_migrates_legacy_source_schema_first(tmp_path: Path) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    fields = {
        "title": "Example role",
        "description": "Example description.",
        "language": "en",
        "parser_version": "jobinja-detail-v1",
    }
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
                source, source_job_id, company_slug, canonical_url, title_observed,
                first_seen_at, last_seen_at
            ) VALUES ('jobinja', 'legacy1', 'acme', 'https://example', 'Example role',
                      '2026-08-01T00:00:00+00:00', '2026-08-01T00:00:00+00:00')
            """
        )
        connection.execute(
            """
            INSERT INTO job_detail_versions(
                job_posting_id, fetched_at, requested_url, final_url, status_code,
                content_sha256, evidence_path, metadata_path, parser_version,
                parse_status, fields_json
            ) VALUES (1, '2026-08-01T00:00:00+00:00', 'https://example',
                      'https://example', 200, 'raw-legacy', 'page.html', 'page.json',
                      'jobinja-detail-v1', 'parsed', ?)
            """,
            (json.dumps(fields, ensure_ascii=False, sort_keys=True),),
        )

    source = TranslationStore(database_path).latest_source_version("legacy1")

    assert source is not None
    assert source.semantic_sha256
    with sqlite3.connect(database_path) as connection:
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(job_detail_versions)")
        }
    assert "semantic_sha256" in columns


def test_v1_artifact_stays_historical_and_v2_is_required(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    observed_at = datetime(2026, 8, 1, tzinfo=UTC)
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="eng1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
            observed_text="Example role",
        ),
        observed_at=observed_at,
    )
    source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=observed_at,
        requested_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
        status_code=200,
        content_sha256="raw-1",
        semantic_sha256="semantic-1",
        evidence_path=Path("eng1.html"),
        metadata_path=Path("eng1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Example role",
            "description": "Example description.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )

    store = TranslationStore(database_path)
    source = store.latest_source_version("eng1")
    assert source is not None
    legacy_id = store.record_artifact(
        source=source,
        target_language="en",
        provider_name="source-identity",
        provider_model="native-english",
        translation_schema_version="english-projection-v1",
        fields={"title": "Example role", "description": "Example description."},
        english_document="legacy",
        segment_provenance={"title": "native", "description": "native"},
        translated_segment_count=0,
        native_segment_count=2,
        translation_sha256="legacy-sha",
        created_at=observed_at,
    )

    service = TranslationService(store=store, provider=None)
    assert TRANSLATION_SCHEMA_VERSION == "english-projection-v2"
    assert store.latest_artifact("eng1") is not None
    assert service.current_artifact("eng1") is None
    assert [item.source_job_id for item in service.missing_source_versions(limit=10)] == ["eng1"]

    repaired = service.translate_job("eng1")

    assert repaired.outcome == "completed"
    assert repaired.artifact_id != legacy_id
    current = service.current_artifact("eng1")
    assert current is not None
    assert current.translation_schema_version == "english-projection-v2"
