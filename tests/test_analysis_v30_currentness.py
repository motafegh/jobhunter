"""Only reviewed English v5 evidence can cross the v30 model boundary."""

from datetime import UTC, datetime

from test_analysis_item_review import _candidate

from jobhunter.analysis_store import AnalysisStore


def test_reviewed_v28_reuses_across_model_with_exact_translation(tmp_path):
    database, artifact_id, translation_id = _candidate(
        tmp_path, prompt_version="job-analysis-english-v28"
    )
    store = AnalysisStore(database)
    store.review_current(
        "review-b", model="model", prompt_version="job-analysis-english-v28",
        schema_version="job-analysis-v5", disposition="accepted",
        reviewed_at=datetime(2026, 9, 28, tzinfo=UTC),
        note="Exact source evidence and all claims reviewed",
        translation_artifact_id=translation_id, require_translation_dependency=True,
    )

    current = store.latest_current(
        "review-b", model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5", accepted_only=True,
        translation_artifact_id=translation_id, require_translation_dependency=True,
    )
    assert current is not None and current.id == artifact_id
    assert current.model == "model" and current.prompt_version == "job-analysis-english-v28"
    assert store.find_artifact(
        job_detail_version_id=current.job_detail_version_id,
        translation_artifact_id=translation_id, require_translation_dependency=True,
        model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5",
    ).id == artifact_id
    assert store.list_current(
        model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5", accepted_only=True,
    )[0].id == artifact_id
    assert store.latest_current(
        "review-b", model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5", translation_artifact_id=translation_id + 1,
        require_translation_dependency=True,
    ) is None


def test_pending_prior_contract_is_not_v30_compatible(tmp_path):
    database, artifact_id, translation_id = _candidate(
        tmp_path, prompt_version="job-analysis-english-v28"
    )
    store = AnalysisStore(database)
    assert store.artifact_by_id(artifact_id).semantic_review_status == "pending"
    assert store.latest_current(
        "review-b", model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5", accepted_only=True,
        translation_artifact_id=translation_id, require_translation_dependency=True,
    ) is None
    assert store.list_current(
        model="another-model", prompt_version="job-analysis-english-v30",
        schema_version="job-analysis-v5", accepted_only=True,
    ) == ()
