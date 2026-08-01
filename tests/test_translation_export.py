import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_export import export_english_corpus
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def _source_store_with_english_job(database_path: Path) -> tuple[JobHunterStore, int]:
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="eng1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
            observed_text="Security Engineer",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    return source_store, posting.job_posting_id


def _record_english_version(
    source_store: JobHunterStore,
    *,
    posting_id: int,
    semantic_sha256: str,
    title: str,
    fetched_at: datetime,
) -> None:
    source_store.record_job_detail(
        job_posting_id=posting_id,
        fetched_at=fetched_at,
        requested_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
        status_code=200,
        content_sha256=f"raw-{semantic_sha256}",
        semantic_sha256=semantic_sha256,
        evidence_path=Path(f"eng1-{semantic_sha256}.html"),
        metadata_path=Path(f"eng1-{semantic_sha256}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": title,
            "description": "Build detection automation.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )


def test_export_contains_latest_current_english_artifacts(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store, posting_id = _source_store_with_english_job(database_path)
    _record_english_version(
        source_store,
        posting_id=posting_id,
        semantic_sha256="semantic-1",
        title="Security Engineer",
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    translation_store = TranslationStore(database_path)
    TranslationService(store=translation_store, provider=None).translate_job("eng1")

    output = tmp_path / "exports" / "english.jsonl"
    result = export_english_corpus(
        translation_store,
        output_path=output,
        limit=50,
    )

    assert result.records == 1
    record = json.loads(output.read_text(encoding="utf-8").strip())
    assert record["source_job_id"] == "eng1"
    assert record["english_origin"] == "native"
    assert record["english_fields"]["title"] == "Security Engineer"
    assert "source_semantic_sha256" in record
    assert "english_document" in record


def test_export_excludes_old_artifact_after_new_source_version(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store, posting_id = _source_store_with_english_job(database_path)
    base_time = datetime(2026, 8, 1, tzinfo=UTC)
    _record_english_version(
        source_store,
        posting_id=posting_id,
        semantic_sha256="semantic-1",
        title="Security Engineer",
        fetched_at=base_time,
    )
    translation_store = TranslationStore(database_path)
    TranslationService(store=translation_store, provider=None).translate_job("eng1")

    _record_english_version(
        source_store,
        posting_id=posting_id,
        semantic_sha256="semantic-2",
        title="Senior Security Engineer",
        fetched_at=base_time + timedelta(hours=1),
    )
    output = tmp_path / "exports" / "english.jsonl"
    stale_result = export_english_corpus(
        translation_store,
        output_path=output,
        limit=50,
    )

    assert stale_result.records == 0
    assert output.read_text(encoding="utf-8") == ""

    TranslationService(store=translation_store, provider=None).translate_job("eng1")
    current_result = export_english_corpus(
        translation_store,
        output_path=output,
        limit=50,
    )

    assert current_result.records == 1
    record = json.loads(output.read_text(encoding="utf-8").strip())
    assert record["source_semantic_sha256"] == "semantic-2"
    assert record["english_fields"]["title"] == "Senior Security Engineer"
