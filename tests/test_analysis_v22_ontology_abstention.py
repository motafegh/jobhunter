from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT_VERSION
from jobhunter.analysis_runtime_v22 import V22CandidateAnalysisProvider
from jobhunter.analysis_service_v22 import (
    _ENGLISH_SYSTEM_PROMPT_V22,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs_v21 import (
    build_requirement_coverage_plan_v21,
    build_responsibility_coverage_plan_v21,
)
from jobhunter.inference.instructor_lm_studio_v22 import (
    AnalysisRequirementV22,
    JobAnalysisResponseV22,
    complete_analysis_partition_with_instructor_v22,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_ACCEPTED_ANCHORS = ("tG9K", "t4jp", "tmBK", "t4qV", "tmyX")


def _context(
    evidence: str,
    *,
    source_kind: str = "requirement_section",
    required_item_excerpts: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "analysis_mode": "english",
        "analysis_fields": {"description": evidence},
        "evidence_catalog": {},
        "requirement_coverage_plan": {
            "candidate": {
                "text": evidence,
                "source_kind": source_kind,
                "obligation_hint": "required",
                "allow_exclusion": False,
                "required_item_excerpts": required_item_excerpts or [],
            }
        },
        "responsibility_coverage_plan": {},
    }


def _requirement(
    *,
    concept: str,
    evidence: str,
    item_excerpt: str,
    concept_type: str,
) -> dict[str, object]:
    return {
        "concept": concept,
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": concept_type,
        "evidence": evidence,
        "item_excerpt": item_excerpt,
        "confidence": "high",
        "rationale": "Direct employer qualification.",
    }


def test_v22_abstains_from_unproven_experience_without_dropping_fact() -> None:
    evidence = (
        "This is why we need someone who can move beyond the idea and prototype stage "
        "and turn an Agent into a reliable system in a real product."
    )
    item = "turn an Agent into a reliable system in a real product"

    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Agent reliability in real product deployment",
            evidence=evidence,
            item_excerpt=item,
            concept_type="experience",
        ),
        context=_context(evidence),
    )

    assert result.concept == "Agent reliability in real product deployment"
    assert result.concept_type == "other"
    assert result.requirement_type == "required"
    assert result.depth_signal is None
    assert result.evidence == evidence
    assert result.item_excerpt == item


def test_v22_preserves_explicit_prior_experience() -> None:
    evidence = "We need someone with practical experience building production AI Agents."
    item = "practical experience building production AI Agents"

    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Production AI Agent building",
            evidence=evidence,
            item_excerpt=item,
            concept_type="experience",
        ),
        context=_context(evidence),
    )

    assert result.concept_type == "experience"


@pytest.mark.parametrize(
    ("concept", "use_reference"),
    [
        ("Reliable service operation experience", True),
        ("Experience operating reliable services", False),
        ("Experienced service operator", True),
    ],
)
def test_v22_rejects_type_only_abstention_that_retains_experience_claim(
    concept: str, use_reference: bool
) -> None:
    evidence = "We need someone who can operate reliable services."
    reference = "field:description:requirement:0"
    context = _context(evidence)
    context["evidence_catalog"] = {reference: evidence}

    with pytest.raises(ValidationError, match="unsupported experience wording in concept"):
        JobAnalysisResponseV22.model_validate(
            {
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [
                    _requirement(
                        concept=concept,
                        evidence=reference if use_reference else evidence,
                        item_excerpt="operate reliable services",
                        concept_type="experience",
                    )
                ],
                "coverage_exclusions": [],
            },
            context=context,
        )


def test_v22_preserves_source_backed_experience_wording_in_concept() -> None:
    evidence = "We require experience operating reliable services."
    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Experience operating reliable services",
            evidence=evidence,
            item_excerpt="experience operating reliable services",
            concept_type="experience",
        ),
        context=_context(evidence),
    )

    assert result.concept == "Experience operating reliable services"
    assert result.concept_type == "experience"


def test_v22_rejects_retained_live_capability_as_experience_concept() -> None:
    evidence = (
        "This is why we need someone who can move beyond the idea and prototype stage "
        "and turn an Agent into a reliable system in a real product."
    )
    reference = "field:description:segment:2:clause:1:sentence:5"
    context = _context(evidence)
    context["evidence_catalog"] = {reference: evidence}

    with pytest.raises(ValidationError, match="unsupported experience wording in concept"):
        AnalysisRequirementV22.model_validate(
            _requirement(
                concept="Agent reliability in real product experience",
                evidence=reference,
                item_excerpt="turn an Agent into a reliable system in a real product",
                concept_type="experience",
            ),
            context=context,
        )


def test_v22_preserves_exact_checklist_experience_type() -> None:
    evidence = "If you have built an Agent, you may be a fit."
    item = "built an Agent"

    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Agent building",
            evidence=evidence,
            item_excerpt=item,
            concept_type="experience",
        ),
        context=_context(
            evidence,
            source_kind="candidate_experience",
            required_item_excerpts=[
                {"text": item, "required_concept_type": "experience"}
            ],
        ),
    )

    assert result.concept_type == "experience"


def test_v22_preserves_checklist_experience_when_model_cites_reference_id() -> None:
    evidence = (
        "if you have built an Agent yourself to date and worked with LLMs, "
        "Tool Calling, memory, workflows, RAG, and Orchestration"
    )
    item = "built an Agent yourself to date"
    reference = "field:description:v21:candidate:1"
    context = _context(
        evidence,
        source_kind="candidate_experience",
        required_item_excerpts=[
            {"text": item, "required_concept_type": "experience"}
        ],
    )
    context["evidence_catalog"] = {reference: evidence}

    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Agent building",
            evidence=reference,
            item_excerpt=item,
            concept_type="experience",
        ),
        context=context,
    )

    assert result.concept_type == "experience"
    assert result.evidence == evidence
    assert result.item_excerpt == item


def test_v22_response_resolves_reference_before_experience_decision() -> None:
    reference = "field:description:v21:candidate:1"
    evidence = (
        "if you have built an Agent yourself to date and can turn an Agent "
        "into a reliable system in a real product"
    )
    experience_item = "built an Agent yourself to date"
    capability_item = "turn an Agent into a reliable system in a real product"
    context = _context(
        evidence,
        source_kind="candidate_experience",
        required_item_excerpts=[
            {"text": experience_item, "required_concept_type": "experience"},
            {"text": capability_item, "required_concept_type": None},
        ],
    )
    context["evidence_catalog"] = {reference: evidence}

    response = JobAnalysisResponseV22.model_validate(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                _requirement(
                    concept="Agent building",
                    evidence=reference,
                    item_excerpt=experience_item,
                    concept_type="experience",
                ),
                _requirement(
                    concept="Reliable Agent product delivery",
                    evidence=reference,
                    item_excerpt=capability_item,
                    concept_type="experience",
                ),
            ],
            "coverage_exclusions": [],
        },
        context=context,
    )

    by_excerpt = {item.item_excerpt: item for item in response.requirements}
    assert by_excerpt[experience_item].concept_type == "experience"
    assert by_excerpt[capability_item].concept_type == "other"
    assert all(item.evidence == evidence for item in response.requirements)


def test_v22_preserves_non_experience_ontology() -> None:
    evidence = "We need someone who can explain distributed system tradeoffs."
    item = "explain distributed system tradeoffs"

    result = AnalysisRequirementV22.model_validate(
        _requirement(
            concept="Distributed system tradeoffs",
            evidence=evidence,
            item_excerpt=item,
            concept_type="knowledge",
        ),
        context=_context(evidence),
    )

    assert result.concept_type == "knowledge"


def test_v22_response_accepts_tvmm_shape_with_ontology_abstention() -> None:
    evidence = (
        "This is why we need someone who can move beyond the idea and prototype stage "
        "and turn an Agent into a reliable system in a real product."
    )
    item = "turn an Agent into a reliable system in a real product"

    response = JobAnalysisResponseV22.model_validate(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                _requirement(
                    concept="Agent reliability in real product deployment",
                    evidence=evidence,
                    item_excerpt=item,
                    concept_type="experience",
                )
            ],
            "coverage_exclusions": [],
        },
        context=_context(evidence),
    )

    assert len(response.requirements) == 1
    assert response.requirements[0].concept_type == "other"


def test_v22_persisted_shape_still_uses_v5_without_item_excerpt() -> None:
    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            _requirement(
                concept="Reliable Agent delivery",
                evidence="turn an Agent into a reliable system",
                item_excerpt="turn an Agent into a reliable system",
                concept_type="other",
            )
        ],
        "coverage_exclusions": [],
    }

    persisted = persisted_v20_shape(structured)

    assert persisted["requirements"][0]["concept_type"] == "other"
    assert "item_excerpt" not in persisted["requirements"][0]


def test_v22_has_distinct_identity_without_changing_current_routing() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v22"
    assert CURRENT_PROMPT_VERSION == "job-analysis-english-v23"
    assert "ONTOLOGY ABSTENTION" in _ENGLISH_SYSTEM_PROMPT_V22
    assert "use concept_type=other" in _ENGLISH_SYSTEM_PROMPT_V22


def test_v22_transport_selects_v22_response_model(monkeypatch) -> None:
    captured = {}
    expected = StructuredInferenceResult(
        model="offline-v22",
        structured={},
        request_body={},
        raw_response={},
        finish_reason="stop",
    )

    def shared_transport(**kwargs):
        captured.update(kwargs)
        return expected

    monkeypatch.setattr(
        "jobhunter.inference.instructor_lm_studio_v20."
        "_complete_analysis_partition_with_instructor",
        shared_transport,
    )
    result = complete_analysis_partition_with_instructor_v22(
        base_url="http://127.0.0.1:1234/v1/",
        api_token=None,
        timeout_seconds=10,
        network_retries=0,
        selected_model="offline-v22",
        system_prompt=_ENGLISH_SYSTEM_PROMPT_V22,
        user_payload={"analysis_fields": {"description": "Requirements: Python"}},
        max_tokens=1024,
        seed=0,
        requirement_coverage_plan={
            "field:description:segment:0:sentence:0": {
                "text": "Python",
                "source_kind": "requirement_section",
                "obligation_hint": "required",
                "allow_exclusion": False,
            }
        },
        responsibility_coverage_plan={},
    )

    assert result.model == expected.model
    assert result.structured == expected.structured
    assert result.raw_response == expected.raw_response
    assert result.finish_reason == expected.finish_reason
    assert result.request_body["runtime"] == {
        "p16_v21_item_scoped_evidence": True,
        "p16_v22_ontology_abstention": True,
    }
    assert captured["response_model"] is JobAnalysisResponseV22
    assert captured["contract_version"] == "v22"


def test_v22_preserves_accepted_anchor_experience_types() -> None:
    validated = 0
    for source_job_id in _ACCEPTED_ANCHORS:
        job_dir = _REPOSITORY_ROOT / "corpus" / "jobs" / source_job_id
        fields = json.loads(
            (job_dir / "english-projection.json").read_text(encoding="utf-8")
        )["fields"]
        requirements = json.loads(
            (job_dir / "p16-english.json").read_text(encoding="utf-8")
        )["analysis"]["requirements"]
        for persisted in requirements:
            if persisted["concept_type"] != "experience":
                continue
            result = AnalysisRequirementV22.model_validate(
                {**persisted, "item_excerpt": persisted["evidence"]},
                context={
                    "analysis_mode": "english",
                    "analysis_fields": fields,
                    "evidence_catalog": {},
                    "requirement_coverage_plan": {},
                },
            )
            assert result.concept_type == "experience"
            validated += 1

    assert validated == 6


def test_v22_preserves_v21_ledgers_across_all_public_projections() -> None:
    provider = V22CandidateAnalysisProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="offline-v22",
        api_token=None,
        timeout_seconds=10,
        max_retries=0,
    )
    projection_paths = sorted(
        (_REPOSITORY_ROOT / "corpus" / "jobs").glob("*/english-projection.json")
    )
    assert len(projection_paths) == 27

    for projection_path in projection_paths:
        fields = json.loads(projection_path.read_text(encoding="utf-8"))["fields"]
        assert provider._requirement_coverage_plan(fields) == (
            build_requirement_coverage_plan_v21(fields)
        )
        assert provider._responsibility_coverage_plan(fields) == (
            build_responsibility_coverage_plan_v21(fields)
        )


def test_v22_provider_keeps_v21_planning_and_v5_persistence(monkeypatch) -> None:
    evidence = "Requirements: We need someone who can ship a reliable Agent."
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v20.ensure_lm_studio_model_context",
        lambda **kwargs: SimpleNamespace(
            context_length=32768,
            action="reused",
            instance_id="offline-v22",
        ),
    )

    def complete_partition(**kwargs):
        calls.append(kwargs)
        parent = next(iter(kwargs["requirement_coverage_plan"].values()))["text"]
        return StructuredInferenceResult(
            model="offline-v22",
            structured={
                "role_purpose": [],
                "responsibilities": [],
                "requirements": [
                    _requirement(
                        concept="Reliable Agent delivery",
                        evidence=parent,
                        item_excerpt="ship a reliable Agent",
                        concept_type="other",
                    )
                ],
                "coverage_exclusions": [],
            },
            request_body={"runtime": {"p16_v22_ontology_abstention": True}},
            raw_response={"offline": True},
            finish_reason="stop",
        )

    monkeypatch.setattr(
        "jobhunter.analysis_runtime_v22.complete_analysis_partition_with_instructor_v22",
        complete_partition,
    )
    provider = V22CandidateAnalysisProvider(
        base_url="http://127.0.0.1:1234/v1",
        configured_model="offline-v22",
        api_token=None,
        timeout_seconds=10,
        max_retries=0,
    )
    result = provider._run_once(
        kwargs={"user_payload": {"analysis_fields": {"description": evidence}}},
        system_prompt=_ENGLISH_SYSTEM_PROMPT_V22,
        original_fields={"description": evidence},
        effective_fields={"description": evidence},
        qualification_refs=[],
        residual_refs=[],
        additional_plan={},
        decomposed_refs=[],
    )

    assert calls
    assert all("item_excerpt" not in item for item in result.structured["requirements"])
