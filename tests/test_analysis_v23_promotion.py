"""V23 currentness preserves historical accepted identity without promoting pending work."""

from __future__ import annotations

from pathlib import Path

import pytest
from test_analysis_v21_promotion import _prepare_job, _record_analysis

from jobhunter.analysis_service_v23 import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    JobAnalysisServiceV23,
)
from jobhunter.analysis_store import (
    SEMANTIC_REVIEW_ACCEPTED,
    SEMANTIC_REVIEW_PENDING,
    AnalysisStore,
)
from jobhunter.translation_store import TranslationStore


class _NeverProvider:
    def complete_structured(self, **_kwargs):
        raise AssertionError("Accepted prior artifact must be reused without inference")


@pytest.mark.parametrize("prior", [
    "job-analysis-english-v20", "job-analysis-english-v21",
])
def test_v23_reuses_only_accepted_prior_artifact_with_exact_identity(
    tmp_path: Path, prior: str,
) -> None:
    database = tmp_path / "jobhunter.sqlite3"
    translation_service, detail_id, translation_id = _prepare_job(database, prior[-3:])
    analyses = AnalysisStore(database)
    prior_id = _record_analysis(
        analyses,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        prompt_version=prior,
        review_status=SEMANTIC_REVIEW_ACCEPTED,
    )
    service = JobAnalysisServiceV23(
        source_store=TranslationStore(database),
        translation_service=translation_service,
        analysis_store=analyses,
        provider=_NeverProvider(),
        model="analysis-model",
    )

    result = service.analyze_english_job(prior[-3:])

    assert result.outcome == "reused"
    assert result.artifact_id == prior_id
    assert result.prompt_version == prior
    assert result.schema_version == ANALYSIS_SCHEMA_VERSION
    current = analyses.latest_current(
        prior[-3:], model="analysis-model", prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION, accepted_only=True,
        translation_artifact_id=translation_id,
        require_translation_dependency=True,
    )
    assert current is not None
    assert (current.id, current.prompt_version) == (prior_id, prior)


@pytest.mark.parametrize("prior", [
    "job-analysis-english-v20", "job-analysis-english-v21",
])
def test_v23_does_not_promote_pending_prior_candidate(tmp_path: Path, prior: str) -> None:
    database = tmp_path / "jobhunter.sqlite3"
    _translations, detail_id, translation_id = _prepare_job(database, prior[-3:])
    analyses = AnalysisStore(database)
    _record_analysis(
        analyses,
        job_detail_version_id=detail_id,
        translation_artifact_id=translation_id,
        prompt_version=prior,
        review_status=SEMANTIC_REVIEW_PENDING,
    )

    assert analyses.find_artifact(
        job_detail_version_id=detail_id, translation_artifact_id=translation_id,
        require_translation_dependency=True, model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION, schema_version=ANALYSIS_SCHEMA_VERSION,
    ) is None
    assert analyses.latest_current(
        prior[-3:], model="analysis-model", prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION, accepted_only=False,
        translation_artifact_id=translation_id,
        require_translation_dependency=True,
    ) is None
