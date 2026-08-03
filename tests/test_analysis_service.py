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


def _assert_no_evidence_values(value) -> None:
    if isinstance(value, dict):
        assert "evidence" not in value
        for nested in value.values():
            _assert_no_evidence_values(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_no_evidence_values(nested)


def _provider(payload: dict) -> LMStudioProvider:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.read())
        assert body["model"] == "analysis-model"
        assert body["response_format"]["type"] == "json_schema"
        system_prompt = " ".join(body["messages"][0]["content"].casefold().split())
        user_payload = json.loads(body["messages"][1]["content"])
        authoritative = user_payload["authoritative_source_fields"]
        assert "language" not in authoritative
        assert "parser_version" not in authoritative

        schema_name = body["response_format"]["json_schema"]["name"]
        if schema_name.endswith("_repair"):
            assert "authoritative_source_fields is the only payload field" in system_prompt
            assert "familiarity alone does not mean preferred" in system_prompt
            assert "english_comprehension_aid" not in user_payload
            rejected = user_payload["rejected_analysis_without_evidence"]
            _assert_no_evidence_values(rejected)
        else:
            assert "untrusted external data" in system_prompt
            assert "ignore previous instructions" in system_prompt
            assert "candidate qualification statements" in system_prompt
            assert "familiarity does not mean preferred" in system_prompt
            assert "english_comprehension_aid" in user_payload

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
) -> JobAnalysisService:
    return JobAnalysisService(
        source_store=TranslationStore(database_path),
        translation_service=translation,
        analysis_store=AnalysisStore(database_path),
        provider=_provider(payload),
        model="analysis-model",
    )


def test_analysis_persists_evidence_validated_artifact_and_reuses(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    service = _service(database_path, translation, _analysis_payload())

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
    assert artifact.prompt_version == "job-analysis-prompt-v4"
    assert artifact.schema_version == "job-analysis-v2"


def test_analysis_repairs_one_synthesized_evidence_claim_then_persists(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    rejected = _analysis_payload()
    rejected["role_purpose"][0]["evidence"] = (
        "Build detection capability across the company."
    )
    repaired = _analysis_payload()
    repaired["role_purpose"] = []
    requests: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.read())
        user_payload = json.loads(body["messages"][1]["content"])
        requests.append(user_payload)
        payload = rejected if len(requests) == 1 else repaired
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

    result = service.analyze_job("eng1")

    assert result.outcome == "completed"
    assert len(requests) == 2
    assert "validation_error" not in requests[0]
    assert "english_comprehension_aid" in requests[0]
    repair_request = requests[1]
    assert "not an exact excerpt" in repair_request["validation_error"]
    assert "english_comprehension_aid" not in repair_request
    assert "rejected_analysis" not in repair_request
    rejected_without_evidence = repair_request["rejected_analysis_without_evidence"]
    _assert_no_evidence_values(rejected_without_evidence)
    assert rejected_without_evidence["role_purpose"][0]["statement"] == (
        rejected["role_purpose"][0]["statement"]
    )
    assert rejected_without_evidence["requirements"][0]["concept"] == "Python"

    artifact = AnalysisStore(database_path).latest_current(
        "eng1",
        model="analysis-model",
        prompt_version="job-analysis-prompt-v4",
        schema_version="job-analysis-v2",
    )
    assert artifact is not None
    assert artifact.analysis["role_purpose"] == []
    assert len(artifact.analysis["responsibilities"]) == 1
    assert len(artifact.analysis["requirements"]) == 2
    repair_payload = json.loads(artifact.request_body["messages"][1]["content"])
    assert "not an exact excerpt" in repair_payload["validation_error"]
    assert "english_comprehension_aid" not in repair_payload
    _assert_no_evidence_values(repair_payload["rejected_analysis_without_evidence"])


def test_analysis_rejects_evidence_not_present_after_one_bounded_repair(
    tmp_path: Path,
) -> None:
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
                    {
                        "finish_reason": "stop",
                        "message": {"content": json.dumps(invalid)},
                    }
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

    with pytest.raises(AnalysisValidationError, match="one bounded repair attempt"):
        service.analyze_job("eng1")

    assert calls == 2
    assert AnalysisStore(database_path).latest_current("eng1") is None


def test_analysis_rejects_parser_metadata_as_employer_evidence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload("jobinja-detail-v2")
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="not an exact excerpt"):
        service.analyze_job("eng1")
    assert AnalysisStore(database_path).latest_current("eng1") is None


def test_analysis_rejects_duplicate_requirement_claims(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload()
    payload["requirements"].append(dict(payload["requirements"][0]))
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="duplicates an earlier requirement"):
        service.analyze_job("eng1")

    assert AnalysisStore(database_path).latest_current("eng1") is None


def test_analysis_rejects_duplicate_responsibility_claims(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation = _prepare_native_job(database_path)
    payload = _analysis_payload()
    payload["responsibilities"].append(dict(payload["responsibilities"][0]))
    service = _service(database_path, translation, payload)

    with pytest.raises(AnalysisValidationError, match="duplicates an earlier responsibility"):
        service.analyze_job("eng1")

    assert AnalysisStore(database_path).latest_current("eng1") is None


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
        service.analyze_job("eng1")

    assert AnalysisStore(database_path).latest_current("eng1") is None