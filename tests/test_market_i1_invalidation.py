import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_store import AnalysisStore
from jobhunter.market_models import MarketDefinitionSpec
from jobhunter.market_store import MarketStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 9, 16, 13, tzinfo=UTC)


def test_target_definition_version_does_not_invalidate_upstream_artifacts(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="stable-upstream",
            company_slug="example",
            canonical_url=(
                "https://jobinja.ir/companies/example/jobs/stable-upstream/role"
            ),
            observed_text="Applied AI Engineer",
        ),
        observed_at=_NOW,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW,
        requested_url="https://jobinja.ir/companies/example/jobs/stable-upstream/role",
        final_url="https://jobinja.ir/companies/example/jobs/stable-upstream/role",
        status_code=200,
        content_sha256="raw-stable-upstream",
        semantic_sha256="semantic-stable-upstream",
        evidence_path=Path("stable-upstream.html"),
        metadata_path=Path("stable-upstream.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": "Applied AI Engineer",
            "description": "Build production AI systems.",
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job("stable-upstream")
    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version="job-analysis-english-v20",
        schema_version="job-analysis-v5",
        analysis={"role_purpose": [], "responsibilities": [], "requirements": []},
        request_body={},
        raw_response={},
        created_at=_NOW,
    )

    market = MarketStore(database_path)
    target = market.create_target(
        slug="applied-ai",
        name="Applied AI",
        description=None,
        created_at=_NOW,
    )
    first = market.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI engineering work",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused",),
        ),
        created_at=_NOW,
    )
    second = market.create_definition_version(
        target.id,
        spec=MarketDefinitionSpec(
            membership_intent="Applied AI engineering work in Tehran",
            search_catalog_version="2026-08-01",
            search_profiles=("ai-focused",),
            geography_scope="Tehran",
        ),
        created_at=_NOW,
    )

    assert second.id != first.id
    with sqlite3.connect(database_path) as connection:
        source_count = connection.execute(
            "SELECT COUNT(*) FROM job_detail_versions WHERE id = ?",
            (detail.version_id,),
        ).fetchone()[0]
        translation_count = connection.execute(
            "SELECT COUNT(*) FROM job_translation_artifacts WHERE id = ?",
            (translation.artifact_id,),
        ).fetchone()[0]
        analysis_count = connection.execute(
            "SELECT COUNT(*) FROM job_analysis_artifacts WHERE id = ?",
            (analysis_id,),
        ).fetchone()[0]

    assert source_count == 1
    assert translation_count == 1
    assert analysis_count == 1
