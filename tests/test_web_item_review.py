"""Browser review stays separate from original claims and whole-artifact acceptance."""

from __future__ import annotations

from fastapi.testclient import TestClient
from test_analysis_item_review import _candidate

from jobhunter.analysis_item_review import AnalysisItemReviewStore
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.web.launcher import build_runtime_app


def test_browser_item_review_end_to_end_with_csrf(tmp_path):
    database, artifact_id, projection_id = _candidate(tmp_path)
    settings = Settings(
        data_dir=tmp_path, database_path=database,
        evidence_dir=tmp_path / "evidence",
        analysis_lm_studio_model="model", translation_enabled=False,
    )
    app = build_runtime_app(settings)
    target = "/jobs/review-b/item-review"
    with TestClient(app) as client:
        page = client.get(target)
        assert page.status_code == 200
        assert "Python" in page.text
        assert "Not reviewed" in page.text
        assert "item review" in page.text.casefold()
        token = app.state.csrf_token
        denied = client.post(
            target, data={"csrf_token": "bad", "artifact_id": artifact_id, "intent": "begin"},
            follow_redirects=False,
        )
        assert denied.status_code == 403
        stale = client.post(
            target, data={"csrf_token": token, "artifact_id": artifact_id + 1,
                          "intent": "begin"}, follow_redirects=False,
        )
        assert stale.status_code == 409
        started = client.post(
            target, data={"csrf_token": token, "artifact_id": artifact_id,
                          "intent": "begin"}, follow_redirects=False,
        )
        assert started.status_code == 303
        assert not AnalysisItemReviewStore(database).is_complete(artifact_id)
        finding = client.post(
            target, data={
                "csrf_token": token, "artifact_id": artifact_id, "intent": "item",
                "kind": "requirements", "item_index": 0, "finding": "supported",
                "note": "Exact Python evidence was checked against the job",
            }, follow_redirects=False,
        )
        assert finding.status_code == 303
        assert "Source supported" in client.get(target).text
        done = client.post(
            target, data={
                "csrf_token": token, "artifact_id": artifact_id, "intent": "finish",
                "note": "Each original item and source omission was checked",
            }, follow_redirects=False,
        )
        assert done.status_code == 303
        assert AnalysisItemReviewStore(database).is_complete(artifact_id)
        artifact = AnalysisStore(database).artifact_by_id(artifact_id)
        assert artifact is not None
        assert artifact.semantic_review_status == "pending"
        assert artifact.translation_artifact_id == projection_id
