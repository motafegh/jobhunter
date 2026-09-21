from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.inference.instructor_lm_studio_v21 import (
    AnalysisRequirementV21,
    JobAnalysisResponseV21,
    persisted_v20_shape,
)


def _context(evidence: str, *, obligation: str = "required") -> dict[str, object]:
    return {
        "analysis_mode": "english",
        "analysis_fields": {"description": evidence},
        "evidence_catalog": {},
        "requirement_coverage_plan": {
            "field:description:segment:0": {
                "text": evidence,
                "source_kind": "requirement_section",
                "obligation_hint": obligation,
                "allow_exclusion": True,
            }
        },
    }


def _requirement(
    *,
    concept: str,
    evidence: str,
    item_excerpt: str,
    depth_signal: str | None,
    requirement_type: str = "required",
    concept_type: str = "skill",
) -> dict[str, object]:
    return {
        "concept": concept,
        "depth_signal": depth_signal,
        "requirement_type": requirement_type,
        "concept_type": concept_type,
        "evidence": evidence,
        "item_excerpt": item_excerpt,
        "confidence": "high",
        "rationale": "Direct employer qualification.",
    }


def test_v21_distinguishes_null_experience_depth_from_neighbor_familiarity() -> None:
    evidence = (
        "practical experience with LLMs and language model APIs in Python and/or TypeScript, "
        "familiarity with Tool Calling / Function Calling, familiarity with RAG, Embedding, "
        "and Vector Databases"
    )
    context = _context(evidence)
    response = JobAnalysisResponseV21.model_validate(
        {
            "role_purpose": [],
            "responsibilities": [],
            "requirements": [
                _requirement(
                    concept="LLM and language model API experience",
                    evidence=evidence,
                    item_excerpt=(
                        "practical experience with LLMs and language model APIs in Python "
                        "and/or TypeScript"
                    ),
                    depth_signal=None,
                    concept_type="experience",
                ),
                _requirement(
                    concept="Tool Calling / Function Calling",
                    evidence=evidence,
                    item_excerpt="familiarity with Tool Calling / Function Calling",
                    depth_signal="familiarity with Tool Calling / Function Calling",
                ),
            ],
            "coverage_exclusions": [],
        },
        context=context,
    )

    assert response.requirements[0].depth_signal is None
    assert response.requirements[1].depth_signal == "familiarity"
    assert {item.evidence for item in response.requirements} == {evidence}


def test_v21_rejects_omitted_depth_within_exact_item_scope() -> None:
    evidence = "practical Python experience, familiarity with Linux and Git"
    with pytest.raises(ValidationError, match="Explicit item depth must be supplied"):
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept="Linux and Git",
                evidence=evidence,
                item_excerpt="familiarity with Linux and Git",
                depth_signal=None,
            ),
            context=_context(evidence),
        )


def test_v21_preserves_shared_preferred_parent_context() -> None:
    evidence = (
        "It is an advantage if you have experience building Production-grade Agents, "
        "familiarity with LLM system Observability and Evaluation"
    )
    context = _context(evidence, obligation="preferred")
    result = AnalysisRequirementV21.model_validate(
        _requirement(
            concept="Production-grade Agent experience",
            evidence=evidence,
            item_excerpt="experience building Production-grade Agents",
            depth_signal=None,
            requirement_type="preferred",
            concept_type="experience",
        ),
        context=context,
    )

    assert result.requirement_type == "preferred"
    assert result.item_excerpt == "experience building Production-grade Agents"
    assert result.evidence == evidence


def test_v21_rejects_item_excerpt_outside_parent_or_wrong_parent_strength() -> None:
    evidence = "It is an advantage if you have familiarity with Docker and Cloud services"
    payload = _requirement(
        concept="Docker and Cloud services",
        evidence=evidence,
        item_excerpt="familiarity with Kubernetes",
        depth_signal="familiarity",
        requirement_type="preferred",
    )
    with pytest.raises(ValidationError, match="exact contiguous source subspan"):
        AnalysisRequirementV21.model_validate(
            payload,
            context=_context(evidence, obligation="preferred"),
        )

    payload["item_excerpt"] = "familiarity with Docker and Cloud services"
    payload["requirement_type"] = "required"
    with pytest.raises(ValidationError, match="Preferred parent coverage"):
        AnalysisRequirementV21.model_validate(
            payload,
            context=_context(evidence, obligation="preferred"),
        )


def test_v21_handles_accepted_anchor_style_multi_depth_list() -> None:
    evidence = (
        "Mastery of Python/Django - Mastery of DRF, FastAPI - Familiarity with Git - "
        "Familiarity with Linux operating system - Sufficient knowledge of Object-Oriented "
        "concepts, modular design"
    )
    context = _context(evidence)
    requirements = [
        ("Python/Django", "Mastery of Python/Django", "Mastery", "tool"),
        ("DRF, FastAPI", "Mastery of DRF, FastAPI", "Mastery", "tool"),
        ("Git", "Familiarity with Git", "Familiarity", "tool"),
        (
            "Linux operating system",
            "Familiarity with Linux operating system",
            "Familiarity",
            "tool",
        ),
        (
            "Object-Oriented concepts, modular design",
            "Sufficient knowledge of Object-Oriented concepts, modular design",
            "Sufficient knowledge",
            "knowledge",
        ),
    ]

    results = [
        AnalysisRequirementV21.model_validate(
            _requirement(
                concept=concept,
                evidence=evidence,
                item_excerpt=item_excerpt,
                depth_signal=depth,
                concept_type=concept_type,
            ),
            context=context,
        )
        for concept, item_excerpt, depth, concept_type in requirements
    ]

    assert [item.depth_signal for item in results] == [
        "Mastery",
        "Mastery",
        "Familiarity",
        "Familiarity",
        "Sufficient knowledge",
    ]


def test_v21_candidate_scope_is_explicit_and_does_not_change_v5_shape() -> None:
    schema = JobAnalysisResponseV21.model_json_schema()
    requirement_ref = schema["properties"]["requirements"]["items"]["$ref"]
    requirement_name = requirement_ref.rsplit("/", 1)[1]
    assert "item_excerpt" in schema["$defs"][requirement_name]["required"]

    structured = {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [
            {
                "concept": "Git",
                "depth_signal": "Familiarity",
                "requirement_type": "required",
                "concept_type": "tool",
                "evidence": "Familiarity with Git and Linux",
                "item_excerpt": "Familiarity with Git",
                "confidence": "high",
                "rationale": "Direct employer qualification.",
            }
        ],
        "coverage_exclusions": [],
    }
    persisted = persisted_v20_shape(structured)

    assert "item_excerpt" not in persisted["requirements"][0]
    assert "item_excerpt" in structured["requirements"][0]
