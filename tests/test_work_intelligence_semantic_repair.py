from __future__ import annotations

import pytest

from jobhunter.work_intelligence_inference import WorkIntelligenceInferenceResult
from jobhunter.work_intelligence_models import JobWorkIntelligence, WorkTheme
from jobhunter.work_intelligence_service import WorkIntelligenceError, WorkIntelligenceService


class _SequenceProvider:
    def __init__(self, documents: list[JobWorkIntelligence]) -> None:
        self._documents = iter(documents)
        self.calls = 0
        self.prompts: list[str] = []

    def complete(self, **kwargs) -> WorkIntelligenceInferenceResult:
        self.calls += 1
        self.prompts.append(kwargs["system_prompt"])
        document = next(self._documents)
        return WorkIntelligenceInferenceResult(
            model="work-model",
            intelligence=document.model_dump(mode="json"),
            request_body={"candidate_call": self.calls},
            raw_response={"candidate_call": self.calls},
            finish_reason="stop",
            validated_model=document,
        )


def _document(summary: str) -> JobWorkIntelligence:
    return JobWorkIntelligence(
        evidence_status="sufficient",
        work_summary=summary,
        work_themes=[
            WorkTheme(
                theme_id="theme-1",
                label="Model development and production readiness",
                summary=(
                    "Build and validate industrial models and collaborate to move them toward "
                    "production."
                ),
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale="The accepted responsibility directly supports the grouped work.",
            )
        ],
        deliverables=[],
        role_interpretation=None,
        limitations=[],
    )


def _service(provider: _SequenceProvider) -> WorkIntelligenceService:
    return WorkIntelligenceService(
        source_store=None,
        analysis_store=None,
        work_store=None,
        translation_service=None,
        analysis_model="analysis-model",
        work_model="work-model",
        provider=provider,
    )


def _generate(service: WorkIntelligenceService):
    return service._generate_with_semantic_repair(
        user_payload={"source_job_id": "tG9K"},
        responsibilities=[
            {
                "statement": (
                    "Partner with engineering to move validated models toward production"
                )
            }
        ],
        role_purpose=[],
        requirements=[],
    )


def test_service_repairs_one_post_validation_scope_failure() -> None:
    provider = _SequenceProvider(
        [
            _document("The role owns the entire lifecycle of industrial ML models."),
            _document(
                "The role builds and validates industrial ML models and partners to move them "
                "toward production."
            ),
        ]
    )
    service = _service(provider)

    document, request_body, raw_response = _generate(service)

    assert provider.calls == 2
    assert "BOUNDED SEMANTIC REPAIR" in provider.prompts[1]
    assert "entire lifecycle" in provider.prompts[1]
    assert "entire lifecycle" not in document.work_summary
    assert request_body["semantic_repair"]["attempts"] == 1
    assert "entire lifecycle" in request_body["semantic_repair"]["trigger"]
    assert raw_response["semantic_repair"]["initial_raw_response"] == {
        "candidate_call": 1
    }
    assert raw_response["semantic_repair"]["final_raw_response"] == {
        "candidate_call": 2
    }


def test_service_still_fails_after_single_semantic_repair_attempt() -> None:
    provider = _SequenceProvider(
        [
            _document("The role owns the entire lifecycle of industrial ML models."),
            _document("The role manages the entire lifecycle of industrial ML models."),
        ]
    )
    service = _service(provider)

    with pytest.raises(WorkIntelligenceError, match="entire lifecycle"):
        _generate(service)

    assert provider.calls == 2
