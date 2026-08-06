import json
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from jobhunter.analysis_service import (
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
    ORIGINAL_PROMPT_VERSION,
    AnalysisValidationError,
    JobAnalysisService,
)
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


def _provider(payload: dict, requests: list[dict] | None = None) -> LMStudioProvider:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.read())
        assert body["model"] == "analysis-model"
        assert body["response_format"]["type"] == "json_schema"
        system_prompt = " ".join(body["messages"][0]["content"].casefold().split())
        user_payload = json.loads(body["messages"][1]["content"])
        if requests is not None:
            requests.append(user_payload)
        analysis_fields = user_payload["analysis_fields"]
        assert "language" not in analysis_fields
        assert "parser_version" not in analysis_fields
        assert "english_comprehension_aid" not in user_payload
        assert "authoritative_source_fields" not in user_payload
        assert "untrusted external data" in system_prompt
        assert "familiarity does not mean preferred" in system_prompt
        assert "never invent evidence-reference ids" in system_prompt
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


def _service(
    database_path: Path,
    translation: TranslationService,
    payload: dict,
    requests: list[dict] | None = None,
) -> JobAnalysisService:
    return JobAnalysisService(
        source_store=TranslationStore(database_path),
        translation_service=translation,
        analysis_store=AnalysisStore(database_path),
        provider=_provider(payload, requests),
        model="analysis-model",
    )


def test_english_analysis_persists_and_reuses_independent_artifact(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    requests: list[dict] = []
    service = _service(database_path, translation, _analysis_payload(), requests)

    first = service.analyze_english_job("eng1")
    second = service.analyze_english_job("eng1")

    assert first.outcome == "completed"
    assert first.analysis_mode == "english"
    assert second.outcome == "reused"
    assert second.artifact_id == first.artifact_id
    assert len(requests) == 1
    assert requests[0]["analysis_mode"] == "english"
    artifact = AnalysisStore(database_path).latest_current(
        "eng1",
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
    )
    assert artifact is not None
    assert artifact.analysis["requirements"][0]["concept"] == "Python"
    assert artifact.translation_artifact_id is not None
    assert artifact.prompt_version == "job-analysis-english-v3"


def test_original_analysis_is_separate_and_does_not_reuse_english(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    requests: list[dict] = []
    service = _service(database_path, translation, _analysis_payload(), requests)

    english = service.analyze_english_job("eng1")
    original = service.analyze_original_job("eng1")
    original_again = service.analyze_original_job("eng1")

    assert english.artifact_id != original.artifact_id
    assert original.analysis_mode == "original"
    assert original_again.outcome == "reused"
    assert original_again.artifact_id == original.artifact_id
    assert [request["analysis_mode"] for request in requests] == ["english", "original"]
    store = AnalysisStore(database_path)
    english_artifact = store.latest_current(
        "eng1",
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
    )
    original_artifact = store.latest_current(
        "eng1",
        model="analysis-model",
        prompt_version=ORIGINAL_PROMPT_VERSION,
        schema_version=ANALYSIS_SCHEMA_VERSION,
    )
    assert english_artifact is not None
    assert original_artifact is not None
    assert english_artifact.translation_artifact_id is not None
    assert original_artifact.translation_artifact_id is None
    assert original_artifact.prompt_version == "job-analysis-original-v3"


def test_english_and_original_requests_never_mix_text_representations(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    requests: list[dict] = []
    service = _service(database_path, translation, _analysis_payload(), requests)

    service.analyze_english_job("eng1")
    service.analyze_original_job("eng1")

    english_request, original_request = requests
    assert set(english_request) == {"source_job_id", "analysis_mode", "analysis_fields"}
    assert set(original_request) == {"source_job_id", "analysis_mode", "analysis_fields"}
    assert english_request["analysis_mode"] == "english"
    assert original_request["analysis_mode"] == "original"


def test_analysis_fails_closed_on_invalid_evidence_without_outer_repair(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    calls = 0
    invalid = _analysis_payload("Kubernetes is mandatory.")

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {"finish_reason": "stop", "message": {"content": json.dumps(invalid)}}
                ]
            },
        )

    provider = LMStudioProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="analysis-model",
        max_retries=0,
        transport=httpx.MockTransport(handler),
    )
    service = JobAnalysisService(
        source_store=TranslationStore(database_path),
        translation_service=translation,
        analysis_store=AnalysisStore(database_path),
        provider=provider,
        model="analysis-model",
    )

    with pytest.raises(AnalysisValidationError, match="not an exact excerpt"):
        service.analyze_english_job("eng1")

    assert calls == 1
    assert (
        AnalysisStore(database_path).latest_current(
            "eng1",
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ANALYSIS_SCHEMA_VERSION,
        )
        is None
    )


def test_analysis_rejects_parser_metadata_as_evidence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload("jobinja-detail-v2")
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="not an exact excerpt"):
        service.analyze_english_job("eng1")


def test_analysis_rejects_duplicate_requirement_claims_on_raw_provider_seam(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload()
    payload["requirements"].append(dict(payload["requirements"][0]))
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="duplicates an earlier requirement"):
        service.analyze_english_job("eng1")


def test_analysis_rejects_duplicate_responsibility_claims_on_raw_provider_seam(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload()
    payload["responsibilities"].append(dict(payload["responsibilities"][0]))
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="duplicates an earlier responsibility"):
        service.analyze_english_job("eng1")


def test_analysis_rejects_inferred_requirement_without_rationale(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload()
    payload["requirements"] = [
        {
            "concept": "Detection engineering",
            "requirement_type": "inferred",
            "concept_type": "practice",
            "evidence": "Build and maintain detection rules.",
            "confidence": "medium",
            "rationale": "",
        }
    ]
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="lacks rationale"):
        service.analyze_english_job("eng1")
