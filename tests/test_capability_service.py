from datetime import UTC, datetime
from pathlib import Path

import pytest

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference import CapabilityInferenceResult
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
    def __init__(self, *, valid: bool = True) -> None:
        self.calls: list[dict] = []
        self.valid = valid

    def complete(self, **kwargs) -> CapabilityInferenceResult:
        self.calls.append(kwargs)
        unknown_scope = (
            [
                {
                    "statement": (
                        "The exact VPN vendor, topology, and high-availability design are not "
                        "supported by the posting."
                    ),
                    "evidence_status": "unknown_or_unsupported",
                    "evidence": [],
                    "rationale": "No vendor, topology, or HA details are stated.",
                    "confidence": "high",
                }
            ]
            if self.valid
            else []
        )
        return CapabilityInferenceResult(
            model="capability-model",
            intelligence={
                "role_interpretation": (
                    "The role applies secure-network knowledge to operational troubleshooting "
                    "rather than merely recognizing VPN terminology."
                ),
                "capabilities": [
                    {
                        "capability_label": "Secure network connectivity and VPN operations",
                        "summary": (
                            "VPN/network knowledge is expected to be applied in live "
                            "connectivity diagnosis, while vendor-specific scope remains unknown."
                        ),
                        "requirement_strength": "required",
                        "employer_stated_depth": [],
                        "work_activities": [],
                        "sub_capabilities": [],
                        "underlying_knowledge": [],
                        "operational_practices": [],
                        "independence_expectation": None,
                        "operational_context": [],
                        "unknown_scope": unknown_scope,
                        "overall_confidence": "high",
                    }
                ],
                "cross_capability_observations": [],
                "uncertainties": ["Exact VPN vendor is not stated."],
            },
            request_body={"provider": "fake"},
            raw_response={"id": "fake"},
            finish_reason="stop",
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
            schema_version=ANALYSIS_SCHEMA_VERSION,
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
        provider=provider,
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
    assert len(provider.calls) == 1
    payload = provider.calls[0]["user_payload"]
    assert payload["accepted_extraction"]["requirements"][0]["concept"] == (
        "VPN and network infrastructure"
    )
    artifact = CapabilityIntelligenceStore(database_path).latest_current(
        "vpn1",
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )
    assert artifact is not None
    assert artifact.analysis_artifact_id == analysis_id
    assert artifact.intelligence["capabilities"][0]["unknown_scope"]


def test_capability_service_requires_current_accepted_english_analysis(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare(database_path, with_analysis=False)
    provider = _Provider()
    service = _service(database_path, provider)

    with pytest.raises(CapabilityIntelligenceError, match="Analyze English first"):
        service.analyze_job("vpn1")

    assert provider.calls == []


def test_capability_service_revalidates_provider_output_before_persistence(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _prepare(database_path)
    provider = _Provider(valid=False)
    service = _service(database_path, provider)

    with pytest.raises(ValueError, match="must add derived reasoning"):
        service.analyze_job("vpn1")

    assert len(provider.calls) == 1
    assert (
        CapabilityIntelligenceStore(database_path).latest_current(
            "vpn1",
            model="capability-model",
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        is None
    )
