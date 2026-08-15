from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference_v8 import CapabilityV8InferenceResult
from jobhunter.capability_service import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    CapabilityIntelligenceService,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


class _Provider:
    """Deterministic staged provider for the promoted public Capability v9 service."""

    def __init__(self, *, valid: bool = True) -> None:
        self.calls: list[dict] = []
        self.valid = valid

    def complete(self, **kwargs) -> CapabilityV8InferenceResult:
        self.calls.append(kwargs)
        response_model = kwargs["response_model"]
        model_name = response_model.__name__
        context = kwargs.get("validation_context") or {}
        user_payload = kwargs["user_payload"]

        if "GroupPlan" in model_name:
            payload = {
                "role_interpretation": "The role combines Secure Network Connectivity.",
                "groups": [
                    {
                        "group_id": 0,
                        "capability_label": "Secure Network Connectivity",
                        "summary": "This capability area covers secure network connectivity.",
                    }
                ],
                "uncertainties": [],
            }
        elif "AssignmentPartition" in model_name:
            payload = {
                "requirement_assignments": [
                    {"index": index, "group_ids": [0]}
                    for index in context.get("owned_requirement_indices", [])
                ],
                "responsibility_assignments": [
                    {"index": index, "group_ids": [0]}
                    for index in context.get("owned_responsibility_indices", [])
                ],
            }
        elif "ProfileReasoning" in model_name:
            group = user_payload.get("group") or {}
            payload = {
                "summary": group.get("summary")
                or "This capability area covers secure network connectivity.",
                "depth_signals": [],
                "work_activities": [],
                "sub_capabilities": [],
                "underlying_knowledge": [],
                "operational_practices": [],
                "operational_context": [],
                "unknown_scope": [],
                "overall_confidence": "high" if self.valid else "certain",
                "uncertainties": [],
            }
        else:  # pragma: no cover - protects the fixture from silent contract expansion
            raise AssertionError(f"Unexpected Capability stage model: {model_name}")

        validated = response_model.model_validate(payload, context=context)
        return CapabilityV8InferenceResult(
            model="capability-model",
            intelligence=validated.model_dump(mode="json"),
            request_body={"provider": "fake", "stage": model_name},
            raw_response={"id": "fake", "stage": model_name},
            finish_reason="stop",
            validated_model=validated,
        )


def _prepare(database_path: Path, *, with_analysis: bool = True):
    now = datetime(2026, 8, 4, tzinfo=UTC)
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="vpn1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/vpn1/example",
            observed_text="Infrastructure Security Specialist",
        ),
        observed_at=now,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/acme/jobs/vpn1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/vpn1/example",
        status_code=200,
        content_sha256="raw-vpn1",
        semantic_sha256="semantic-vpn1",
        evidence_path=Path("vpn1.html"),
        metadata_path=Path("vpn1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "Infrastructure Security Specialist",
            "company": "Acme",
            "description": (
                "Mastery of VPN and network infrastructure. "
                "Troubleshoot connectivity and security incidents."
            ),
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )
    detail_id = detail.version_id

    translation_store = TranslationStore(database_path)
    source = translation_store.latest_source_version("vpn1")
    assert source is not None
    translation_id = translation_store.record_artifact(
        source=source,
        target_language="en",
        provider_name="source-identity",
        provider_model="native-english",
        translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        fields={
            "title": "Infrastructure Security Specialist",
            "company": "Acme",
            "description": (
                "Mastery of VPN and network infrastructure. "
                "Troubleshoot connectivity and security incidents."
            ),
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
        english_document=(
            "Infrastructure Security Specialist\nAcme\n"
            "Mastery of VPN and network infrastructure."
        ),
        segment_provenance={
            "title": "native",
            "company": "native",
            "description": "native",
        },
        translated_segment_count=0,
        native_segment_count=3,
        translation_sha256="translation-vpn1",
        created_at=now,
    )

    analysis_id = None
    if with_analysis:
        analysis_store = AnalysisStore(database_path)
        analysis_id = analysis_store.record_artifact(
            job_detail_version_id=detail_id,
            translation_artifact_id=translation_id,
            model="analysis-model",
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            analysis={
                "role_purpose": [],
                "responsibilities": [
                    {
                        "statement": "Troubleshoot connectivity and security incidents",
                        "evidence": "Troubleshoot connectivity and security incidents",
                        "confidence": "high",
                    }
                ],
                "requirements": [
                    {
                        "concept": "VPN and network infrastructure",
                        "depth_signal": "Mastery of VPN and network infrastructure",
                        "requirement_type": "required",
                        "concept_type": "knowledge",
                        "evidence": "Mastery of VPN and network infrastructure",
                        "confidence": "high",
                        "rationale": "",
                    }
                ],
            },
            request_body={"analysis": "request"},
            raw_response={"analysis": "response"},
            created_at=now,
        )
    return detail_id, translation_id, analysis_id


def _service(database_path: Path, provider: _Provider) -> CapabilityIntelligenceService:
    return CapabilityIntelligenceService(
        source_store=TranslationStore(database_path),
        analysis_store=AnalysisStore(database_path),
        capability_store=CapabilityIntelligenceStore(database_path),
        provider=provider,  # type: ignore[arg-type]
        analysis_model="analysis-model",
        capability_model="capability-model",
    )


def test_capability_service_persists_and_reuses_exact_dependency_artifact(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _, translation_id, analysis_id = _prepare(database_path)
    assert analysis_id is not None
    provider = _Provider()
    service = _service(database_path, provider)

    first = service.analyze_job("vpn1")
    second = service.analyze_job("vpn1")

    assert first.outcome == "completed"
    assert second.outcome == "reused"
    assert second.artifact_id == first.artifact_id
    assert first.translation_artifact_id == translation_id
    assert first.analysis_artifact_id == analysis_id
    assert len(provider.calls) == 3

    plan_payload = provider.calls[0]["user_payload"]
    assert plan_payload["capability_requirements"][0]["concept"] == (
        "VPN and network infrastructure"
    )
    assert plan_payload["responsibilities"][0]["statement"] == (
        "Troubleshoot connectivity and security incidents"
    )

    profile_payload = provider.calls[2]["user_payload"]
    assert "p1:requirements:0" in profile_payload["evidence_reference_ids"]
    assert "p1:responsibilities:0" in profile_payload["evidence_reference_ids"]

    artifact = CapabilityIntelligenceStore(database_path).latest_current(
        "vpn1",
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )
    assert artifact is not None
    assert artifact.analysis_artifact_id == analysis_id
    profile = artifact.intelligence["capabilities"][0]
    assert profile["source_requirement_indices"] == [0]
    assert profile["source_responsibility_indices"] == [0]
    assert profile["requirement_strength"] == "required"
    assert profile["depth_signals"] == [
        {
            "statement": (
                "VPN and network infrastructure — employer-stated depth: "
                "Mastery of VPN and network infrastructure"
            ),
            "evidence_status": "source_explicit",
            "evidence": ["Mastery of VPN and network infrastructure"],
            "rationale": (
                "Deterministically propagated from accepted P1.6 requirement 0; "
                "not model-inferred."
            ),
            "confidence": "high",
        }
    ]
    assert profile["unknown_scope"] == []
    source_truth = artifact.intelligence["source_truth"]
    assert source_truth["unlinked_capability_requirement_indices"] == []
    assert source_truth["unlinked_responsibility_indices"] == []


def test_capability_service_requires_current_accepted_english_analysis(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare(database_path, with_analysis=False)
    provider = _Provider()
    service = _service(database_path, provider)

    with pytest.raises(CapabilityIntelligenceError, match="Analyze English first"):
        service.analyze_job("vpn1")

    assert provider.calls == []


def test_capability_service_uses_exact_p1_6_translation_amid_alternate_artifacts(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _, original_translation_id, _ = _prepare(database_path)
    store = TranslationStore(database_path)
    source = store.latest_source_version("vpn1")
    assert source is not None
    alternate_translation_id = store.record_artifact(
        source=source,
        target_language="en",
        provider_name="experimental",
        provider_model="alternate-english",
        translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        fields={
            "title": "Alternate Infrastructure Security Specialist",
            "company": "Acme",
            "description": "Alternate experimental projection text.",
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
        english_document="Alternate experimental projection text.",
        segment_provenance={"description": "translated"},
        translated_segment_count=1,
        native_segment_count=0,
        translation_sha256="translation-vpn1-alternate",
        created_at=datetime(2026, 8, 4, 1, tzinfo=UTC),
    )
    assert alternate_translation_id != original_translation_id
    provider = _Provider()
    service = _service(database_path, provider)

    result = service.analyze_job("vpn1")

    assert result.outcome == "completed"
    assert result.translation_artifact_id == original_translation_id
    assert len(provider.calls) == 3
    plan_payload = provider.calls[0]["user_payload"]
    assert plan_payload["title"] == "Infrastructure Security Specialist"
    assert plan_payload["capability_requirements"][0]["evidence"] == [
        "Mastery of VPN and network infrastructure"
    ]


def test_capability_service_revalidates_provider_output_before_persistence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare(database_path)
    provider = _Provider(valid=False)
    service = _service(database_path, provider)

    with pytest.raises(ValueError, match="overall_confidence"):
        service.analyze_job("vpn1")

    assert len(provider.calls) == 3
    assert (
        CapabilityIntelligenceStore(database_path).latest_current(
            "vpn1",
            model="capability-model",
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        is None
    )
