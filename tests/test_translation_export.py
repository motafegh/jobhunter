import json
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_export import export_english_corpus
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def test_export_contains_latest_current_english_artifacts(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
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
    source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
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
            "title": "Security Engineer",
            "description": "Build detection automation.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
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
