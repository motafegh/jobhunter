from datetime import UTC, datetime
from pathlib import Path

from jobhunter.analysis_current import ENGLISH_ANALYSIS_SCHEMA_VERSION, ENGLISH_PROMPT_VERSION
from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference_v8 import CapabilityV8InferenceResult
from jobhunter.capability_service_v8 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceServiceV8,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.capability_v8_models import (
    CapabilityAssignmentPartitionV8,
    CapabilityGroupPlanV8,
    CapabilityProfileReasoningV8,
)
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation.projection import TRANSLATION_SCHEMA_VERSION
from jobhunter.translation_store import TranslationStore


class _Provider:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def complete(self, **kwargs) -> CapabilityV8InferenceResult:
        self.calls.append(kwargs)
        response_model = kwargs["response_model"]
        payload = kwargs["user_payload"]
        assert "rationale" not in repr(payload)

        if response_model is CapabilityGroupPlanV8:
            intelligence = {
                "role_interpretation": (
                    "The role combines applied machine learning with production data operations."
                ),
                "groups": [
                    {
                        "group_id": 0,
                        "capability_label": "Applied machine learning",
                        "summary": "Build and validate models using the stated analytical stack.",
                    },
                    {
                        "group_id": 1,
                        "capability_label": "Data and operational engineering",
                        "summary": "Work with production data pipelines and operational practices.",
                    },
                ],
                "uncertainties": [],
            }
        elif response_model is CapabilityAssignmentPartitionV8:
            intelligence = {
                "requirement_assignments": [
                    {
                        "index": item["index"],
                        "group_ids": [item["index"] % 2],
                    }
                    for item in payload["owned_requirements"]
                ],
                "responsibility_assignments": [
                    {
                        "index": item["index"],
                        "group_ids": [item["index"] % 2],
                    }
                    for item in payload["owned_responsibilities"]
                ],
            }
        elif response_model is CapabilityProfileReasoningV8:
            evidence_ref = payload["evidence_reference_ids"][0]
            intelligence = {
                "summary": payload["group"]["summary"],
                "depth_signals": [],
                "work_activities": [],
                "sub_capabilities": [
                    {
                        "statement": "Apply the linked source facts together in this capability area.",
                        "evidence_status": "strongly_implied_by_work",
                        "evidence": [evidence_ref],
                        "rationale": "The linked work directly supports this bounded capability.",
                        "confidence": "high",
                    }
                ],
                "underlying_knowledge": [],
                "operational_practices": [],
                "operational_context": [],
                "unknown_scope": [],
                "overall_confidence": "high",
                "uncertainties": [],
            }
        else:  # pragma: no cover - test guard
            raise AssertionError(response_model)

        return CapabilityV8InferenceResult(
            model="capability-model",
            intelligence=intelligence,
            request_body={"response_model": response_model.__name__},
            raw_response={"response_model": response_model.__name__},
            finish_reason="stop",
        )


def _prepare(database_path: Path) -> tuple[int, int, int]:
    now = datetime(2026, 8, 15, tzinfo=UTC)
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id="dense1",
            company_slug="acme",
            canonical_url="https://jobinja.ir/companies/acme/jobs/dense1/example",
            observed_text="ML Engineer",
        ),
        observed_at=now,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=now,
        requested_url="https://jobinja.ir/companies/acme/jobs/dense1/example",
        final_url="https://jobinja.ir/companies/acme/jobs/dense1/example",
        status_code=200,
        content_sha256="raw-dense1",
        semantic_sha256="semantic-dense1",
        evidence_path=Path("dense1.html"),
        metadata_path=Path("dense1.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "title": "ML Engineer",
            "company": "Acme",
            "description": (
                "Python expert. Solid statistics. Build data pipelines. "
                "Build ML models. Operate production pipelines. Master's degree."
            ),
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
    )

    translation_store = TranslationStore(database_path)
    source = translation_store.latest_source_version("dense1")
    assert source is not None
    translation_id = translation_store.record_artifact(
        source=source,
        target_language="en",
        provider_name="source-identity",
        provider_model="native-english",
        translation_schema_version=TRANSLATION_SCHEMA_VERSION,
        fields={
            "title": "ML Engineer",
            "company": "Acme",
            "description": (
                "Python expert. Solid statistics. Build data pipelines. "
                "Build ML models. Operate production pipelines. Master's degree."
            ),
            "language": "en",
            "parser_version": "jobinja-detail-v2",
        },
        english_document=(
            "ML Engineer\nAcme\nPython expert. Solid statistics. Build data pipelines. "
            "Build ML models. Operate production pipelines. Master's degree."
        ),
        segment_provenance={
            "title": "native",
            "company": "native",
            "description": "native",
        },
        translated_segment_count=0,
        native_segment_count=3,
        translation_sha256="translation-dense1",
        created_at=now,
    )

    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "role_purpose": [],
            "responsibilities": [
                {
                    "statement": "Build ML models",
                    "evidence": "Build ML models",
                    "confidence": "high",
                },
                {
                    "statement": "Operate production pipelines",
                    "evidence": "Operate production pipelines",
                    "confidence": "high",
                },
            ],
            "requirements": [
                {
                    "concept": "Python",
                    "concept_type": "tool",
                    "requirement_type": "required",
                    "depth_signal": "expert",
                    "evidence": "Python expert",
                    "confidence": "high",
                    "rationale": "DO NOT LEAK",
                },
                {
                    "concept": "Statistics",
                    "concept_type": "knowledge",
                    "requirement_type": "required",
                    "depth_signal": "Solid",
                    "evidence": "Solid statistics",
                    "confidence": "high",
                    "rationale": "DO NOT LEAK",
                },
                {
                    "concept": "Data pipelines",
                    "concept_type": "skill",
                    "requirement_type": "required",
                    "depth_signal": None,
                    "evidence": "Build data pipelines",
                    "confidence": "high",
                    "rationale": "DO NOT LEAK",
                },
                {
                    "concept": "Master's degree",
                    "concept_type": "education",
                    "requirement_type": "required",
                    "depth_signal": None,
                    "evidence": "Master's degree",
                    "confidence": "high",
                    "rationale": "DO NOT LEAK",
                },
            ],
        },
        request_body={"analysis": "request"},
        raw_response={"analysis": "response"},
        created_at=now,
    )
    return detail.version_id, translation_id, analysis_id


def test_v8_stages_cover_source_then_reconcile_and_persist(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    _, translation_id, analysis_id = _prepare(database_path)
    provider = _Provider()
    service = CapabilityIntelligenceServiceV8(
        source_store=TranslationStore(database_path),
        analysis_store=AnalysisStore(database_path),
        capability_store=CapabilityIntelligenceStore(database_path),
        provider=provider,
        analysis_model="analysis-model",
        capability_model="capability-model",
    )

    result = service.analyze_job("dense1")

    assert result.outcome == "completed"
    assert result.analysis_artifact_id == analysis_id
    assert result.translation_artifact_id == translation_id
    assert [call["response_model"] for call in provider.calls] == [
        CapabilityGroupPlanV8,
        CapabilityAssignmentPartitionV8,
        CapabilityProfileReasoningV8,
        CapabilityProfileReasoningV8,
    ]

    artifact = CapabilityIntelligenceStore(database_path).latest_current(
        "dense1",
        model="capability-model",
        prompt_version=CAPABILITY_PROMPT_VERSION,
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )
    assert artifact is not None
    source_truth = artifact.intelligence["source_truth"]
    assert source_truth["capability_requirement_indices"] == [0, 1, 2]
    assert source_truth["role_level_requirement_indices"] == [3]
    assert source_truth["unlinked_capability_requirement_indices"] == []
    assert source_truth["unlinked_responsibility_indices"] == []
    assert artifact.request_body["architecture"] == (
        "source-led-group-plan-assignment-profile-v8"
    )
