from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.queries import WebRepository


def _add_job(
    store: JobHunterStore,
    *,
    job_id: str,
    parse_status: str | None,
) -> int | None:
    observed_at = datetime(2026, 8, 3, tzinfo=UTC)
    posting = store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="acme",
            canonical_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
            observed_text=f"Role {job_id}",
        ),
        observed_at=observed_at,
    )
    if parse_status is None:
        return None
    version = store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=observed_at,
        requested_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        final_url=f"https://jobinja.ir/companies/acme/jobs/{job_id}/example",
        status_code=200,
        content_sha256=f"raw-{job_id}",
        semantic_sha256=f"semantic-{job_id}",
        evidence_path=Path(f"{job_id}.html"),
        metadata_path=Path(f"{job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status=parse_status,
        fields={
            "title": f"Role {job_id}",
            "company": "Acme",
            "description": "Build reliable systems.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    return version.version_id


def test_dashboard_stats_keep_each_current_pipeline_stage_distinct(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    store = JobHunterStore(database_path)
    store.initialize()

    _add_job(store, job_id="discovered", parse_status=None)
    _add_job(store, job_id="partial", parse_status="partial")
    _add_job(store, job_id="parsed-only", parse_status="parsed")
    analyzed_version = _add_job(store, job_id="analyzed", parse_status="parsed")
    _add_job(store, job_id="translated-only", parse_status="parsed")

    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    )
    analyzed_english = translation.translate_job("analyzed")
    translated_english = translation.translate_job("translated-only")
    assert analyzed_english.artifact_id != translated_english.artifact_id
    assert analyzed_version is not None

    AnalysisStore(database_path).record_artifact(
        job_detail_version_id=analyzed_version,
        translation_artifact_id=analyzed_english.artifact_id,
        model="analysis-model",
        prompt_version=PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
        analysis={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [],
        },
        request_body={},
        raw_response={},
        created_at=datetime(2026, 8, 3, tzinfo=UTC),
    )

    stats = WebRepository(
        database_path,
        analysis_model="analysis-model",
    ).dashboard_stats()

    assert stats.discovered_jobs == 5
    assert stats.detailed_jobs == 4
    assert stats.parsed_jobs == 3
    assert stats.translated_jobs == 2
    assert stats.analyzed_jobs == 1
    assert stats.missing_details == 1
    assert stats.missing_translations == 1
    assert stats.missing_analyses == 1
