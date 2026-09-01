from __future__ import annotations

import pytest

from jobhunter.work_intelligence_inference import WorkIntelligenceInferenceResult
from jobhunter.work_intelligence_models import CandidateJobWorkIntelligence, CandidateWorkTheme
from jobhunter.work_intelligence_service import WorkIntelligenceError, WorkIntelligenceService


class _SequenceProvider:
    def __init__(self, candidates: list[CandidateJobWorkIntelligence]) -> None:
        self._candidates = iter(candidates)
        self.calls = 0
        self.prompts: list[str] = []

    def complete(self, **kwargs) -> WorkIntelligenceInferenceResult:
        self.calls += 1
        self.prompts.append(kwargs["system_prompt"])
        candidate = next(self._candidates)
        return WorkIntelligenceInferenceResult(
            model="work-model",
            intelligence=candidate.model_dump(mode="json"),
            request_body={"candidate_call": self.calls},
            raw_response={"candidate_call": self.calls},
            finish_reason="stop",
            validated_model=candidate,
        )


def _candidate(rationale: str) -> CandidateJobWorkIntelligence:
    return CandidateJobWorkIntelligence(
        evidence_status="sufficient",
        work_themes=[
            CandidateWorkTheme(
                theme_id="theme-1",
                label="Model development and production readiness",
                emphasis="primary",
                confidence="high",
                responsibility_indices=[0],
                role_purpose_indices=[],
                supporting_requirement_indices=[],
                rationale=rationale,
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
        user_payload={
            "source_job_id": "tG9K",
            "analysis_artifact_id": 36,
            "responsibilities": [
                {
                    "index": 0,
                    "statement": (
                        "Partner with engineering to move validated models toward production"
                    ),
                }
            ],
            "role_purpose": [],
            "supporting_requirements": [],
        },
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


def test_service_repairs_one_post_validation_scope_failure_without_second_review() -> None:
    provider = _SequenceProvider(
        [
            _candidate("This theme owns the entire lifecycle of industrial ML models."),
            _candidate(
                "This theme groups model work with engineering collaboration toward production."
            ),
        ]
    )
    service = _service(provider)

    candidate, request_body, raw_response = _generate(service)

    assert provider.calls == 2
    assert "BOUNDED SEMANTIC REPAIR" in provider.prompts[1]
    assert "entire lifecycle" in provider.prompts[1]
    assert "entire lifecycle" not in (candidate.work_themes[0].rationale or "")
    assert request_body["semantic_repair"]["attempts"] == 1
    assert "entire lifecycle" in request_body["semantic_repair"]["trigger"]
    assert raw_response["semantic_repair"]["initial_raw_response"] == {
        "candidate_call": 1
    }
    assert raw_response["semantic_repair"]["final_raw_response"] == {
        "candidate_call": 2
    }


def test_valid_direct_work_candidate_uses_one_model_call() -> None:
    provider = _SequenceProvider(
        [
            _candidate(
                "This theme groups model development with production-readiness collaboration."
            )
        ]
    )
    service = _service(provider)

    candidate, request_body, raw_response = _generate(service)

    assert provider.calls == 1
    assert "final semantic authority reviewer" not in provider.prompts[0]
    assert candidate.work_themes[0].theme_id == "theme-1"
    assert request_body == {"candidate_call": 1}
    assert raw_response == {"candidate_call": 1}


def test_service_still_fails_after_single_semantic_repair_attempt() -> None:
    provider = _SequenceProvider(
        [
            _candidate("This theme owns the entire lifecycle of industrial ML models."),
            _candidate("This theme manages the entire lifecycle of industrial ML models."),
        ]
    )
    service = _service(provider)

    with pytest.raises(WorkIntelligenceError, match="entire lifecycle"):
        _generate(service)

    assert provider.calls == 2
