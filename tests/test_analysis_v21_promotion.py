from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_service_v21 import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    JobAnalysisServiceV21,
)
from jobhunter.analysis_store import (
    SEMANTIC_REVIEW_ACCEPTED,
    SEMANTIC_REVIEW_PENDING,
    AnalysisStore,
)
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_V20_PROMPT_VERSION = "job-analysis-english-v20"


def _prepare_job(database_path: Path, source_job_id: str) -> tuple[TranslationService, int, int]:
    source = JobHunterStore(database_path)
    source.initialize()
    posting = source.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=source_job_id,
            company_slug="compat",
            canonical_url=f"https://jobinja.ir/companies/compat/jobs/{source_job_id}/example",
            observed_text="AI Engineer",
        ),
        observed_at=datetime(2026, 9, 22, tzinfo=UTC),
    )
    source.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 9, 22, tzinfo=UTC),
        requested_url=f"https://jobinja.ir/companies/compat/jobs/{source_job_id}/example",
        final_url=f"https://jobinja.ir/companies/compat/jobs/{source_job_id}/example",
        status_code=200,
        content_sha256=f"raw-{source_job_id}",
        semantic_sha256=f"semantic-{source_job_id}",
        evidence_path=Path(f"{source_job_id}.html"),
        metadata_path=Path(f"{source_job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "AI Engineer",
            "company": "Compat",
            "description": "Build reliable AI systems. Python experience is required.",
            "skills": ["Python"],
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    translations = TranslationStore(database_path)
    translation_service = TranslationService(store=translations, provider=None)
    translation_result = translation_service.translate_job(source_job_id)
    source_version = translations.latest_source_version(source_job_id)
    assert source_version is not None
    return translation_service, source_version.job_detail_version_id, translation_result.artifact_id


def _record_analysis(
    store: AnalysisStore,
    *,
    job_detail_version_id: int,
    translation_artifact_id: int,
    prompt_version: str,
    review_status: str,
) -> int:
    return store.record_artifact(
        job_detail_version_id=job_detail_version_id,
        translation_artifact_id=translation_artifact_id,
        model="analysis-model",
        prompt_version=prompt_version,
        schema_version=ANALYSIS_SCHEMA_VERSION,
        analysis={
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [],
            "coverage": [],
            "responsibility_coverage": [],
        },
        request_body={"contract": prompt_version},
        raw_response={"offline": True},
        created_at=datetime(2026, 9, 22, tzinfo=UTC),
        semantic_review_status=review_status,
    )


class _NeverProvider:
    def complete_structured(self, **_kwargs):
        raise AssertionError(
            "accepted v20 compatibility artifact should be reused without inference"
        )


def test_v21_current_service_reuses_accepted_v20_artifact_with_exact_lineage(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation_service, detail_id, translation_id = _prepare_job(database_path, "compat1")
    analyses = AnalysisStore(database_path)
    legacy_id = _record_analysis(
        analyses,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        prompt_version=_V20_PROMPT_VERSION,
        review_status=SEMANTIC_REVIEW_ACCEPTED,
    )
    service = JobAnalysisServiceV21(
        source_store=TranslationStore(database_path),
        translation_service=translation_service,
        analysis_store=analyses,
        provider=_NeverProvider(),
        model="analysis-model",
    )

    result = service.analyze_english_job("compat1")

    assert result.outcome == "reused"
    assert result.artifact_id == legacy_id
    assert result.prompt_version == _V20_PROMPT_VERSION
    assert result.schema_version == ANALYSIS_SCHEMA_VERSION

    accepted = analyses.latest_current(
        "compat1",
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
        accepted_only=True,
        translation_artifact_id=translation_id,
        require_translation_dependency=True,
    )
    assert accepted is not None
    assert accepted.id == legacy_id
    assert accepted.prompt_version == _V20_PROMPT_VERSION


def test_v21_compatibility_does_not_promote_pending_v20_candidate(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _translation_service, detail_id, translation_id = _prepare_job(database_path, "compat2")
    analyses = AnalysisStore(database_path)
    _record_analysis(
        analyses,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        prompt_version=_V20_PROMPT_VERSION,
        review_status=SEMANTIC_REVIEW_PENDING,
    )

    assert (
        analyses.find_artifact(
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            require_translation_dependency=True,
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        is None
    )
    assert (
        analyses.latest_current(
            "compat2",
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
            accepted_only=False,
            translation_artifact_id=translation_id,
            require_translation_dependency=True,
        )
        is None
    )
