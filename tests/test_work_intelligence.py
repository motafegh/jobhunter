from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore
from jobhunter.web.launcher import build_runtime_app
from jobhunter.work_intelligence_inference import WorkIntelligenceInferenceResult
from jobhunter.work_intelligence_models import (
    CandidateRoleInterpretation,
    JobWorkIntelligence,
    WorkTheme,
)
from jobhunter.work_intelligence_service import (
    DETERMINISTIC_LIMITED_MODEL,
    WORK_INTELLIGENCE_PROMPT_VERSION,
    WORK_INTELLIGENCE_SCHEMA_VERSION,
    WorkIntelligenceError,
    WorkIntelligenceService,
)
from jobhunter.work_intelligence_store import WorkIntelligenceStore

_NOW = datetime(2026, 8, 26, 18, tzinfo=UTC)


def _settings(database_path: Path) -> Settings:
    return Settings(
        data_dir=database_path.parent,
        evidence_dir=database_path.parent / "evidence",
        database_path=database_path,
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="work-model",
        translation_enabled=False,
    )


def _seed_version(
    database_path: Path,
    *,
    job_id: str,
    version: int,
    responsibilities: list[dict[str, object]],
    role_purpose: list[dict[str, object]] | None = None,
    requirements: list[dict[str, object]] | None = None,
    semantic_review_status: str = "accepted",
) -> int:
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="p22a-disposable",
            canonical_url=(
                f"https://jobinja.ir/companies/p22a-disposable/jobs/{job_id}/role"
            ),
            observed_text=f"Disposable {job_id}",
        ),
        observed_at=_NOW + timedelta(minutes=version),
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW + timedelta(minutes=version),
        requested_url=(
            f"https://jobinja.ir/companies/p22a-disposable/jobs/{job_id}/role"
        ),
        final_url=f"https://jobinja.ir/companies/p22a-disposable/jobs/{job_id}/role",
        status_code=200,
        content_sha256=f"content-{job_id}-v{version}",
        semantic_sha256=f"semantic-{job_id}-v{version}",
        evidence_path=Path(f"{job_id}-v{version}.html"),
        metadata_path=Path(f"{job_id}-v{version}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": f"Disposable {job_id}",
            "description": f"Disposable accepted source for {job_id}, version {version}.",
        },
    )
    translation = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    ).translate_job(job_id)
    return AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "requirements": requirements
            or [
                {
                    "concept": "Python",
                    "concept_type": "language",
                    "requirement_type": "required",
                    "evidence": "Python",
                    "confidence": "high",
                }
            ],
            "responsibilities": responsibilities,
            "role_purpose": role_purpose or [],
        },
        request_body={},
        raw_response={},
        created_at=_NOW + timedelta(minutes=version),
        semantic_review_status=semantic_review_status,
    )


class _FakeProvider:
    def __init__(self, document: JobWorkIntelligence) -> None:
        self.document = document
        self.calls = 0

    def complete(self, **_kwargs) -> WorkIntelligenceInferenceResult:
        self.calls += 1
        return WorkIntelligenceInferenceResult(
            model="work-model",
            intelligence=self.document.model_dump(mode="json"),
            request_body={"fake": True},
            raw_response={"fake": True},
            finish_reason="stop",
            validated_model=self.document,
        )


def _service(
    database_path: Path,
    *,
    provider: _FakeProvider | None,
    work_model: str | None,
) -> WorkIntelligenceService:
    return WorkIntelligenceService(
        source_store=TranslationStore(database_path),
        analysis_store=AnalysisStore(database_path),
        work_store=WorkIntelligenceStore(database_path),
        translation_service=TranslationService(
            store=TranslationStore(database_path),
            provider=None,
        ),
        analysis_model="analysis-model",
        work_model=work_model,
        provider=provider,
        clock=lambda: _NOW + timedelta(hours=1),
    )


def _valid_direct_document() -> JobWorkIntelligence:
    return JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary=(
            "The job combines security assessment work with repeatable audit automation and "
            "technical reporting."
        ),
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Security assessment",
                summary="Review security posture and identify configuration or control weaknesses.",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[0],
                supporting_requirement_indices=[0],
                rationale="The accepted work explicitly covers assessment and security review.",
            ),
            WorkTheme(
                theme_id="theme-2",
                label="Audit automation",
                summary="Automate recurring assessment and audit activities with scripting.",
                emphasis="supporting",
                confidence="high",
                responsibility_indices=[1],
                role_purpose_indices=[],
                supporting_requirement_indices=[0],
                rationale="The second accepted responsibility explicitly describes automation.",
            ),
        ],
        deliverables=[],
        role_interpretation=CandidateRoleInterpretation(
            label="Security assessment and automation role",
            summary=(
                "A candidate interpretation centered on security review work with a supporting "
                "automation component."
            ),
            confidence="high",
            supporting_theme_ids=["theme-1", "theme-2"],
            alternatives=[],
            limitations=["This is a job-level interpretation, not a promoted role archetype."],
        ),
        limitations=[],
    )


def test_requirement_only_job_produces_limited_artifact_without_model_call(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    analysis_id = _seed_version(
        database_path,
        job_id="tmBK",
        version=1,
        responsibilities=[],
    )
    service = _service(database_path, provider=None, work_model=None)

    first = service.analyze_job("tmBK")
    second = service.analyze_job("tmBK")
    artifact = service.current_artifact("tmBK")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert first.artifact_id == second.artifact_id
    assert first.model == DETERMINISTIC_LIMITED_MODEL
    assert artifact is not None
    assert artifact.analysis_artifact_id == analysis_id
    assert artifact.semantic_state == "candidate"
    assert artifact.intelligence["evidence_status"] == "limited"
    assert artifact.intelligence["work_themes"] == []
    assert artifact.intelligence["deliverables"] == []
    assert artifact.intelligence["role_interpretation"] is None


def test_direct_work_is_persisted_as_candidate_and_reused(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    analysis_id = _seed_version(
        database_path,
        job_id="tmyX",
        version=1,
        responsibilities=[
            {
                "statement": "Assess vulnerabilities and security configurations",
                "evidence": "Assess vulnerabilities and security configurations",
                "confidence": "high",
            },
            {
                "statement": "Automate assessment and audit processes",
                "evidence": "Automate assessment and audit processes",
                "confidence": "high",
            },
        ],
        role_purpose=[
            {
                "statement": "Strengthen infrastructure security",
                "evidence": "Strengthen infrastructure security",
                "confidence": "high",
            }
        ],
    )
    provider = _FakeProvider(_valid_direct_document())
    service = _service(database_path, provider=provider, work_model="work-model")

    first = service.analyze_job("tmyX")
    second = service.analyze_job("tmyX")
    artifact = service.current_artifact("tmyX")

    assert provider.calls == 2
    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert first.artifact_id == second.artifact_id
    assert artifact is not None
    assert artifact.analysis_artifact_id == analysis_id
    assert artifact.model == "work-model"
    assert artifact.semantic_state == "candidate"
    assert artifact.prompt_version == WORK_INTELLIGENCE_PROMPT_VERSION
    assert artifact.schema_version == WORK_INTELLIGENCE_SCHEMA_VERSION
    assert artifact.intelligence["role_interpretation"]["label"] == (
        "Security assessment and automation role"
    )


def test_direct_work_rejects_out_of_range_source_reference(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_version(
        database_path,
        job_id="bad-ref",
        version=1,
        responsibilities=[
            {
                "statement": "Review security controls",
                "evidence": "Review security controls",
                "confidence": "high",
            }
        ],
    )
    document = JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary="The role contains direct security control review responsibilities.",
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Security review",
                summary="Review technical security controls and their configuration.",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[2],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale="The model attempted to reference a missing responsibility.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )
    service = _service(
        database_path,
        provider=_FakeProvider(document),
        work_model="work-model",
    )

    with pytest.raises(WorkIntelligenceError, match="missing responsibility indices"):
        service.analyze_job("bad-ref")
    assert WorkIntelligenceStore(database_path).latest_for_job("bad-ref") is None


def test_direct_work_rejects_omitted_accepted_responsibility(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_version(
        database_path,
        job_id="omit-work",
        version=1,
        responsibilities=[
            {
                "statement": "Review security controls",
                "evidence": "Review security controls",
                "confidence": "high",
            },
            {
                "statement": "Automate recurring audits",
                "evidence": "Automate recurring audits",
                "confidence": "high",
            },
        ],
    )
    document = JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary="The role includes security review work with an incomplete model grouping.",
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Security review",
                summary="Review technical security controls and their configuration.",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale="Only the first responsibility was grouped by the candidate model.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )
    service = _service(
        database_path,
        provider=_FakeProvider(document),
        work_model="work-model",
    )

    with pytest.raises(WorkIntelligenceError, match="omitted accepted direct work evidence"):
        service.analyze_job("omit-work")
    assert WorkIntelligenceStore(database_path).latest_for_job("omit-work") is None


def test_historical_artifact_stops_being_current_after_new_accepted_p16_dependency(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    first_analysis_id = _seed_version(
        database_path,
        job_id="stale-work",
        version=1,
        responsibilities=[],
    )
    service = _service(database_path, provider=None, work_model=None)
    first = service.analyze_job("stale-work")
    historical = WorkIntelligenceStore(database_path).artifact_by_id(first.artifact_id)
    assert historical is not None
    assert historical.analysis_artifact_id == first_analysis_id

    second_analysis_id = _seed_version(
        database_path,
        job_id="stale-work",
        version=2,
        responsibilities=[],
    )

    assert second_analysis_id != first_analysis_id
    assert service.current_artifact("stale-work") is None
    preserved = WorkIntelligenceStore(database_path).artifact_by_id(first.artifact_id)
    assert preserved is not None
    assert preserved.analysis_artifact_id == first_analysis_id


def test_pending_p16_cannot_generate_work_intelligence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_version(
        database_path,
        job_id="pending-work",
        version=1,
        responsibilities=[],
        semantic_review_status="pending",
    )
    service = _service(database_path, provider=None, work_model=None)

    with pytest.raises(WorkIntelligenceError, match="semantically accepted current English P1.6"):
        service.analyze_job("pending-work")


def test_browser_limited_work_flow_is_candidate_and_does_not_publish(
    tmp_path: Path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _seed_version(
        database_path,
        job_id="tmBK-web",
        version=1,
        responsibilities=[],
    )
    settings = _settings(database_path)
    publication_calls: list[str] = []
    monkeypatch.setattr(
        "jobhunter.web.launcher._synchronize_public_corpus",
        lambda _settings: publication_calls.append("published"),
    )
    app = build_runtime_app(settings)

    with TestClient(app) as client:
        empty = client.get("/jobs/tmBK-web/work-intelligence")
        assert empty.status_code == 200
        assert "Generate Work Intelligence" in empty.text
        assert "candidate interpretation" in empty.text

        generated = client.post(
            "/jobs/tmBK-web/work-intelligence",
            data={"csrf_token": app.state.csrf_token},
            follow_redirects=True,
        )
        assert generated.status_code == 200
        assert "candidate · limited" in generated.text
        assert "will not invent duties from qualifications alone" in generated.text
        assert "JobHunter interpretation" in generated.text
        assert "Employer / accepted P1.6 facts" in generated.text

    assert publication_calls == []
