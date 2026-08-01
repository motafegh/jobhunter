import json
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from jobhunter.analysis_service import AnalysisValidationError, JobAnalysisService
from jobhunter.analysis_store import AnalysisStore
from jobhunter.inference import LMStudioProvider
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore


def _prepare_native_job(database_path: Path) -> TranslationService:
    source = JobHunterStore(database_path)
    source.initialize()
    posting = source.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="eng1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/eng1/example",
            observed_text="Detection Engineer",
        ),
        observed_at=datetime(2026, 8, 1, tzinfo=UTC),
    )
    source.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=datetime(2026, 8, 1, tzinfo=UTC),
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
            "title": "Detection Engineer",
            "company": "Acme",
            "description": (
                "Build and maintain detection rules. Python experience is required. "
                "Docker familiarity is preferred."
            ),
            "skills": ["Python"],
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    translation = TranslationService(store=TranslationStore(database_path), provider=None)
    translation.translate_job("eng1")
    return translation


def _analysis_payload(evidence: str = "Python experience is required.") -> dict:
    return {
        "role_purpose": [
            {
                "statement": "Improve threat detection capability",
                "evidence": "Build and maintain detection rules.",
                "confidence": "high",
            }
        ],
        "responsibilities": [
            {
                "statement": "Build and maintain detection rules",
                "evidence": "Build and maintain detection rules.",
                "confidence": "high",
            }
        ],
        "requirements": [
            {
                "concept": "Python",
                "requirement_type": "required",
                "concept_type": "skill",
                "evidence": evidence,
                "confidence": "high",
                "rationale": "",
            },
            {
                "concept": "Docker",
                "requirement_type": "preferred",
                "concept_type": "tool",
                "evidence": "Docker familiarity is preferred.",
                "confidence": "high",
                "rationale": "",
            },
        ],
    }


def _provider(payload: dict) -> LMStudioProvider:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.read())
        assert body["model"] == "analysis-model"
        assert body["response_format"]["type"] == "json_schema"
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": json.dumps(payload)},
                    }
                ]
            },
        )

    return LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="analysis-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )


def test_analysis_persists_evidence_validated_artifact_and_reuses(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    service = JobAnalysisService(
        source_store=TranslationStore(database_path),
        translation_service=translation,
        analysis_store=AnalysisStore(database_path),
        provider=_provider(_analysis_payload()),
        model="analysis-model",
    )

    first = service.analyze_job("eng1")
    second = service.analyze_job("eng1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert second.artifact_id == first.artifact_id
    artifact = AnalysisStore(database_path).latest_current("eng1")
    assert artifact is not None
    assert artifact.analysis["requirements"][0]["concept"] == "Python"
    assert artifact.translation_artifact_id is not None
    assert artifact.request_body["model"] == "analysis-model"


def test_analysis_rejects_evidence_not_present_in_authoritative_source(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    service = JobAnalysisService(
        source_store=TranslationStore(database_path),
        translation_service=translation,
        analysis_store=AnalysisStore(database_path),
        provider=_provider(_analysis_payload("Kubernetes is mandatory.")),
        model="analysis-model",
    )

    with pytest.raises(AnalysisValidationError, match="not an exact excerpt"):
        service.analyze_job("eng1")
    assert AnalysisStore(database_path).latest_current("eng1") is None
