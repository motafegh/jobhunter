"""Isolated A1 R2/R3/R4 controls."""

from __future__ import annotations

from dataclasses import asdict, replace

import pytest
from pydantic import ValidationError

from jobhunter.analysis_runtime_v20 import _v20_deterministic_structured_skills
from jobhunter.evidence_refs_v21 import build_responsibility_coverage_plan_v21
from jobhunter.inference.instructor_lm_studio_v30 import AnalysisRequirementV30
from jobhunter.p16_lab_a1_r4 import (
    board_skill_observations,
    separate_board_skills,
    verify_board_observations,
)
from jobhunter.p16_lab_a1_r23 import AnalysisRequirementR2, corrected_duty_plan
from jobhunter.translation_store import TranslationSourceVersion

MOTIVATION = "with a strong interest in hands-on robotics development."


def raw_motivation(**changes):
    return {
        "concept": "Strong interest in hands-on robotics development",
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "other",
        "evidence": MOTIVATION,
        "confidence": "high",
        "rationale": "Source expectation.",
        "item_excerpt": MOTIVATION,
        **changes,
    }


def ctx(text=MOTIVATION, plan=None):
    return {
        "analysis_mode": "english",
        "analysis_fields": {"description": text},
        "requirement_coverage_plan": plan or {},
    }


@pytest.mark.parametrize("signal", [None, "strong", "strong interest"])
def test_motivation_remains_explicit_without_technical_depth(signal):
    raw = raw_motivation(depth_signal=signal)
    result = AnalysisRequirementR2.model_validate(raw, context=ctx())
    assert result.depth_signal is None
    assert result.concept == raw["concept"]
    assert result.evidence == result.item_excerpt == MOTIVATION
    assert result.requirement_type == "required"


@pytest.mark.parametrize(
    "changes",
    [
        {"depth_signal": "expertise"},
        {"depth_signal": "hands-on"},
        {"concept_type": "skill"},
        {"concept_type": "experience"},
        {"concept": "Robotics experience"},
        {"evidence": "invented evidence"},
        {"requirement_type": "preferred"},
        {"requirement_type": "inferred", "rationale": ""},
    ],
)
def test_motivation_does_not_authorize_other_assertions(changes):
    with pytest.raises(ValidationError):
        AnalysisRequirementR2.model_validate(raw_motivation(**changes), context=ctx())


def test_motivation_preferred_parent_still_enforced():
    plan = {"r": {"text": MOTIVATION, "obligation_hint": "preferred"}}
    with pytest.raises(ValidationError):
        AnalysisRequirementR2.model_validate(raw_motivation(), context=ctx(plan=plan))


@pytest.mark.parametrize(
    "text,concept,depth",
    [
        ("Mastery of Rust", "Rust", "Mastery"),
        ("Hands-on experience in robotics", "Robotics", "Hands-on"),
        ("3 years of software development", "Software development", "3 years"),
    ],
)
def test_r2_genuine_depth_unchanged(text, concept, depth):
    raw = raw_motivation(
        concept=concept, depth_signal=depth, item_excerpt=text, evidence=text, concept_type="skill"
    )
    old = AnalysisRequirementV30.model_validate(raw, context=ctx(text))
    new = AnalysisRequirementR2.model_validate(raw, context=ctx(text))
    assert old.model_dump() == new.model_dump()


@pytest.mark.parametrize(
    "description",
    [
        "Responsibilities: Deploy applications. Skills: Familiarity with Kubernetes.",
        "Responsibilities: Maintain infrastructure. Skills: Knowledge of Linux. "
        "You will deploy services.",
        "Responsibilities: Maintain infrastructure. Skills: Configure and operate systems.",
        "Responsibilities: Develop a Skills: dashboard. Monitor services.",
        "Responsibilities: Monitor systems. Qualifications: Knowledge of Linux.",
    ],
)
def test_r3_never_adds_duties_or_removes_unproven_items(description):
    fields = {"description": description}
    baseline = build_responsibility_coverage_plan_v21(fields)
    corrected, removed = corrected_duty_plan(fields)
    assert corrected == {k: v for k, v in baseline.items() if k not in removed}
    for key in removed:
        assert baseline[key].startswith("Skills: Familiarity")
    if "Familiarity" not in description:
        assert not removed


def test_r3_exact_transition_removes_false_duplicate():
    fields = {
        "description": "Responsibilities: Deploy applications. Skills: Familiarity with Kubernetes."
    }
    old = build_responsibility_coverage_plan_v21(fields)
    new, removed = corrected_duty_plan(fields)
    assert len(removed) == 1
    assert old[removed[0]] == "Skills: Familiarity with Kubernetes."
    assert list(new.values()) == ["Deploy applications."]


def source(skills):
    return TranslationSourceVersion(
        "synthetic", 1, "a" * 64, "en", {"skills": skills, "description": "Rust is a plus."}
    )


def test_r4_preserves_board_identity_without_upgrading_prose():
    s = source(["Rust", " Go ", "Rust"])
    old_fields, old_claims, _ = _v20_deterministic_structured_skills(s.fields)
    fields, board = separate_board_skills(s, s.fields)
    assert fields == old_fields == {"description": "Rust is a plus."}
    assert all(c["requirement_type"] == "required" for c in old_claims)
    assert [b.value for b in board] == s.fields["skills"]
    assert [b.selector for b in board] == ["/skills/0", "/skills/1", "/skills/2"]
    assert all(b.employer_obligation == "not_established" and b.depth_signal is None for b in board)
    verify_board_observations(s, [asdict(b) for b in board])


def test_r4_does_not_invent_original_translation_equivalence():
    s = source(["مهندسی"])
    fields, board = separate_board_skills(s, {"skills": ["Engineering"], "description": "Work"})
    assert fields == {"description": "Work"}
    assert board[0].value == "مهندسی"


@pytest.mark.parametrize("skills", ["Rust", [""], ["Rust", 123]])
def test_r4_malformed_source_fails(skills):
    with pytest.raises(ValueError):
        board_skill_observations(source(skills))


def test_r4_reordered_or_modified_records_rejected():
    s = source(["Rust", "Go"])
    records = [asdict(b) for b in board_skill_observations(s)]
    with pytest.raises(ValueError):
        verify_board_observations(s, records[::-1])
    with pytest.raises(ValueError):
        verify_board_observations(replace(s, job_detail_version_id=2), records)
    records[0]["employer_obligation"] = "required"
    with pytest.raises(ValueError):
        verify_board_observations(s, records)
