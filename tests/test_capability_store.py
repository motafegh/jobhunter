from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_service import CAPABILITY_PROMPT_VERSION, CAPABILITY_SCHEMA_VERSION
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


def _dependencies(database_path: Path) -> tuple[int, int, int]:
    now = datetime(2026, 8, 4, tzinfo=UTC)
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="cap1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/cap1/example",
            observed_text="Security Engineer",
        ),
        observed_at=now,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/acme/jobs/cap1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/cap1/example",
        status_code=200,
        content_sha256="raw-cap1",
        semantic_sha256="semantic-cap1",
        evidence_path=Path("cap1.html"),
        metadata_path=Path("cap1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Security Engineer",
            "description": "Troubleshoot VPN incidents.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    translation_store = TranslationStore(database_path)
    source = translation_store.latest_source_version("cap1")
    assert source is not None
    translation_id = translation_store.record_artifact(
        source=source,
        target_language="en",
        provider_name="source-identity",
        provider_model="native-english",
        translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        fields={
            "title": "Security Engineer",
            "description": "Troubleshoot VPN incidents.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
        english_document="Security Engineer\nTroubleshoot VPN incidents.",
        segment_provenance={"title": "native", "description": "native"},
        translated_segment_count=0,
        native_segment_count=2,
        translation_sha256="translation-cap1",
        created_at=now,
    )
    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
        analysis={"role_purpose": [], "responsibilities": [], "requirements": []},
        request_body={},
        raw_response={},
        created_at=now,
    )
    return detail.version_id, translation_id, analysis_id


def test_capability_store_initializes_repeat_safely_and_preserves_analysis(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    detail_id, translation_id, analysis_id = _dependencies(database_path)
    store = CapabilityIntelligenceStore(database_path)

    store.initialize()
    store.initialize()

    assert (
        AnalysisStore(database_path).latest_current(
            "cap1",
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        ).id
        == analysis_id
    )

    artifact_id = store.record_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
        intelligence={
            "role_interpretation": "The role applies VPN knowledge to operational incidents.",
            "capabilities": [],
            "cross_capability_observations": [],
            "uncertainties": [],
        },
        request_body={},
        raw_response={},
        created_at=datetime(2026, 8, 4, tzinfo=UTC),
    )
    current = store.find_artifact(
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        analysis_artifact_id=analysis_id,
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )

    assert current is not None
    assert current.id == artifact_id
    assert current.analysis_artifact_id == analysis_id
