from datetime import UTC, datetime
from pathlib import Path

from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


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
