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
    AcceptedWorkItem,
    CandidateJobWorkIntelligence,
    CandidateRoleInterpretation,
    CandidateWorkTheme,
    JobWorkIntelligence,
    WorkTheme,
)
from jobhunter.work_intelligence_service import (
    DETERMINISTIC_LIMITED_MODEL,
    WORK_INTELLIGENCE_PROMPT_VERSION,
    WORK_INTELLIGENCE_SCHEMA_VERSION,
    WorkIntelligenceError,
    WorkIntelligenceService,
    format_work_intelligence,
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
    def __init__(self, candidate: CandidateJobWorkIntelligence) -> None:
        self.candidate = candidate
        self.calls = 0
        self.response_models: list[type] = []

    def complete(self, **kwargs) -> WorkIntelligenceInferenceResult:
        self.calls += 1
        self.response_models.append(kwargs["response_model"])
        return WorkIntelligenceInferenceResult(
            model="work-model",
            intelligence=self.candidate.model_dump(mode="json"),
            request_body={"fake": True},
            raw_response={"fake": True},
            finish_reason="stop",
            validated_model=self.candidate,
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


def _valid_direct_candidate() -> CandidateJobWorkIntelligence:
    return CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Security assessment",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[0],
                supporting_requirement_indices=[0],
                rationale="This groups the accepted assessment and security-review work.",
            ),
            CandidateWorkTheme(
                theme_id="theme-2",
                label="Audit automation",
                emphasis="supporting",
                confidence="high",
                responsibility_indices=[1],
                role_purpose_indices=[],
                supporting_requirement_indices=[0],
                rationale="This groups the accepted recurring audit-automation work.",
            ),
        ],
        deliverables=[],
        role_interpretation=CandidateRoleInterpretation(
            label="Security assessment and automation role",
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
    assert "work_summary" not in artifact.intelligence


def test_direct_work_is_assembled_with_exact_p16_facts_and_reused(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    responsibility_0 = "Assess vulnerabilities and security configurations"
    responsibility_1 = "Automate assessment and audit processes"
    role_purpose_0 = "Strengthen infrastructure security"
    analysis_id = _seed_version(
        database_path,
        job_id="tmyX",
        version=1,
        responsibilities=[
            {
                "statement": responsibility_0,
                "evidence": responsibility_0,
                "confidence": "high",
            },
            {
                "statement": responsibility_1,
                "evidence": responsibility_1,
                "confidence": "high",
            },
        ],
        role_purpose=[
            {
                "statement": role_purpose_0,
                "evidence": role_purpose_0,
                "confidence": "high",
            }
        ],
    )
    provider = _FakeProvider(_valid_direct_candidate())
    service = _service(database_path, provider=provider, work_model="work-model")

    first = service.analyze_job("tmyX")
    second = service.analyze_job("tmyX")
    artifact = service.current_artifact("tmyX")

    assert provider.calls == 1
    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert first.artifact_id == second.artifact_id
    assert artifact is not None
    assert artifact.analysis_artifact_id == analysis_id
    assert artifact.model == "work-model"
    assert artifact.semantic_state == "candidate"
    assert artifact.prompt_version == WORK_INTELLIGENCE_PROMPT_VERSION
    assert artifact.schema_version == WORK_INTELLIGENCE_SCHEMA_VERSION

    document = JobWorkIntelligence.model_validate(artifact.intelligence)
    assert document.work_themes[0].accepted_work_items == [
        AcceptedWorkItem(
            kind="responsibility",
            index=0,
            statement=responsibility_0,
            confidence="high",
        ),
        AcceptedWorkItem(
            kind="role_purpose",
            index=0,
            statement=role_purpose_0,
            confidence="high",
        ),
    ]
    assert document.work_themes[1].accepted_work_items[0].statement == responsibility_1
    assert artifact.intelligence["role_interpretation"]["label"] == (
        "Security assessment and automation role"
    )
    assert "work_summary" not in artifact.intelligence
    assert "summary" not in artifact.intelligence["work_themes"][0]
    assert "responsibility_indices" not in artifact.intelligence["work_themes"][0]


def test_candidate_interpretation_cannot_replace_exact_tg9k_factual_statement(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    exact_statement = (
        "Partner with the semiconductor technical lead and engineering to move models toward "
        "production."
    )
    _seed_version(
        database_path,
        job_id="tG9K",
        version=1,
        responsibilities=[
            {
                "statement": exact_statement,
                "evidence": exact_statement,
                "confidence": "high",
            }
        ],
    )
    candidate = CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Production deployment",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale="Candidate grouping around production-readiness activity.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )
    service = _service(
        database_path,
        provider=_FakeProvider(candidate),
        work_model="work-model",
    )

    result = service.analyze_job("tG9K")
    artifact = WorkIntelligenceStore(database_path).artifact_by_id(result.artifact_id)

    assert artifact is not None
    persisted = artifact.intelligence["work_themes"][0]
    assert persisted["label"] == "Production deployment"
    assert persisted["accepted_work_items"] == [
        {
            "kind": "responsibility",
            "index": 0,
            "statement": exact_statement,
            "confidence": "high",
        }
    ]


def test_role_purpose_hardening_wording_is_preserved_exactly(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    exact_role_purpose = (
        "Assess security posture of servers and Microsoft services and to develop and provide "
        "security requirements, Best Practices, and hardening solutions."
    )
    _seed_version(
        database_path,
        job_id="tmyX-role-purpose",
        version=1,
        responsibilities=[],
        role_purpose=[
            {
                "statement": exact_role_purpose,
                "evidence": exact_role_purpose,
                "confidence": "high",
            }
        ],
    )
    candidate = CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Security hardening",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[],
                role_purpose_indices=[0],
                supporting_requirement_indices=[],
                rationale="Candidate grouping of the accepted security-posture work.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )
    service = _service(
        database_path,
        provider=_FakeProvider(candidate),
        work_model="work-model",
    )

    result = service.analyze_job("tmyX-role-purpose")
    artifact = WorkIntelligenceStore(database_path).artifact_by_id(result.artifact_id)

    assert artifact is not None
    work = artifact.intelligence["work_themes"][0]["accepted_work_items"][0]
    assert work["kind"] == "role_purpose"
    assert work["index"] == 0
    assert work["statement"] == exact_role_purpose


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
    candidate = CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Security review",
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
        provider=_FakeProvider(candidate),
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
    candidate = CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Security review",
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
        provider=_FakeProvider(candidate),
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


def test_historical_v1_artifact_remains_readable_but_is_not_reused_as_v2(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    analysis_id = _seed_version(
        database_path,
        job_id="historical-v1",
        version=1,
        responsibilities=[
            {
                "statement": "Review security controls",
                "evidence": "Review security controls",
                "confidence": "high",
            }
        ],
    )
    store = WorkIntelligenceStore(database_path)
    historical_id = store.record_artifact(
        analysis_artifact_id=analysis_id,
        model="work-model",
        prompt_version="job-work-intelligence-v1.3",
        schema_version="job-work-intelligence-v1",
        intelligence={
            "evidence_status": "sufficient",
            "work_summary": "Historical v1 candidate.",
            "work_themes": [],
            "deliverables": [],
            "role_interpretation": None,
            "limitations": [],
        },
        request_body={"historical": True},
        raw_response={"historical": True},
        created_at=_NOW,
    )
    service = _service(
        database_path,
        provider=_FakeProvider(
            CandidateJobWorkIntelligence(
                evidence_status="sufficient",
                work_themes=[
                    CandidateWorkTheme(
                        theme_id="theme-1",
                        label="Security review",
                        emphasis="primary",
                        confidence="high",
                        responsibility_indices=[0],
                        role_purpose_indices=[],
                        supporting_requirement_indices=[],
                        rationale="Candidate grouping of accepted review work.",
                    )
                ],
                deliverables=[],
                role_interpretation=None,
                limitations=[],
            )
        ),
        work_model="work-model",
    )

    historical = store.artifact_by_id(historical_id)

    assert historical is not None
    assert historical.prompt_version == "job-work-intelligence-v1.3"
    assert historical.intelligence["work_summary"] == "Historical v1 candidate."
    assert service.current_artifact("historical-v1") is None


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
        assert "Accepted P1.6 facts" in generated.text
        assert "JobHunter interpretation" in generated.text
        assert "job-work-intelligence-v2" in generated.text

    assert publication_calls == []


def test_browser_and_cli_show_exact_work_separately_from_interpretation(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    exact_statement = "Partner with engineering to move models toward production."
    analysis_id = _seed_version(
        database_path,
        job_id="v2-view",
        version=1,
        responsibilities=[
            {
                "statement": exact_statement,
                "evidence": exact_statement,
                "confidence": "high",
            }
        ],
    )
    document = JobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Production readiness",
                emphasis="primary",
                confidence="high",
                accepted_work_items=[
                    AcceptedWorkItem(
                        kind="responsibility",
                        index=0,
                        statement=exact_statement,
                        confidence="high",
                    )
                ],
                supporting_requirement_indices=[],
                rationale="This groups the accepted collaboration around production readiness.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )
    artifact_id = WorkIntelligenceStore(database_path).record_artifact(
        analysis_artifact_id=analysis_id,
        model="analysis-model",
        prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
        schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
        intelligence=document.model_dump(mode="json"),
        request_body={"manual_fixture": True},
        raw_response={"manual_fixture": True},
        created_at=_NOW,
    )
    settings = _settings(database_path)
    app = build_runtime_app(settings)

    with TestClient(app) as client:
        response = client.get("/jobs/v2-view/work-intelligence")

    assert response.status_code == 200
    assert "JobHunter candidate theme" in response.text
    assert "Accepted P1.6 work" in response.text
    assert exact_statement in response.text
    assert "JobHunter interpretation" in response.text

    artifact = WorkIntelligenceStore(database_path).artifact_by_id(artifact_id)
    assert artifact is not None
    rendered = format_work_intelligence(artifact)
    assert "JobHunter candidate theme" in rendered
    assert "Accepted P1.6 work:" in rendered
    assert exact_statement in rendered
    assert "JobHunter interpretation:" in rendered


def test_current_v2_artifact_rejects_kind_index_statement_mismatch(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    analysis_id = _seed_version(
        database_path,
        job_id="mismatched-fact",
        version=1,
        responsibilities=[
            {
                "statement": "Partner with engineering to move models toward production.",
                "evidence": "Partner with engineering to move models toward production.",
                "confidence": "high",
            }
        ],
    )
    WorkIntelligenceStore(database_path).record_artifact(
        analysis_artifact_id=analysis_id,
        model="work-model",
        prompt_version=WORK_INTELLIGENCE_PROMPT_VERSION,
        schema_version=WORK_INTELLIGENCE_SCHEMA_VERSION,
        intelligence={
            "evidence_status": "sufficient",
            "work_themes": [
                {
                    "theme_id": "theme-1",
                    "label": "Production readiness",
                    "emphasis": "primary",
                    "confidence": "high",
                    "accepted_work_items": [
                        {
                            "kind": "responsibility",
                            "index": 0,
                            "statement": "Deploy models to production.",
                            "confidence": "high",
                        }
                    ],
                    "supporting_requirement_indices": [],
                    "rationale": "Candidate grouping.",
                }
            ],
            "deliverables": [],
            "role_interpretation": None,
            "limitations": [],
        },
        request_body={"manual_fixture": True},
        raw_response={"manual_fixture": True},
        created_at=_NOW,
    )
    service = _service(
        database_path,
        provider=_FakeProvider(_valid_direct_candidate()),
        work_model="work-model",
    )

    with pytest.raises(
        WorkIntelligenceError,
        match="does not exactly match P1.6 responsibility\\[0\\]",
    ):
        service.current_artifact("mismatched-fact")
