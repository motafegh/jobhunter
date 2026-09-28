"""Required residual ownership and exact source degree in isolated v27."""

import json
from pathlib import Path

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_service_v27 import ENGLISH_PROMPT_VERSION
from jobhunter.evidence_refs_v27 import persisted_qualification_plan_v27
from jobhunter.inference.instructor_lm_studio_v27 import AnalysisRequirementV27

_ROOT = Path(__file__).resolve().parents[1]


def _fields(job: str) -> dict:
    return json.loads(
        (_ROOT / f"corpus/jobs/{job}/english-projection.json").read_text(
            encoding="utf-8"
        )
    )["fields"]


def test_required_decomposed_residual_cannot_be_excluded() -> None:
    plan = persisted_qualification_plan_v27(_fields("t7Ay"))
    residual = plan["field:__candidate_residual_requirement_evidence:0"]
    assert "Model Context Protocol" in residual["text"]
    assert residual["obligation_hint"] == "required"
    assert residual["allow_exclusion"] is False
    assert CURRENT_PROMPT == "job-analysis-english-v30"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v27"


def test_qualified_degree_retains_source_modifier() -> None:
    evidence = "Relative mastery of Prompt Engineering and Workflow design."
    claim = {
        "concept": "Prompt Engineering and Workflow design",
        "depth_signal": "mastery",
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Source proficiency wording.",
        "item_excerpt": evidence,
    }
    parsed = AnalysisRequirementV27.model_validate(
        claim,
        context={"analysis_mode": "english", "analysis_fields": {"description": evidence}},
    )
    assert parsed.depth_signal == "Relative mastery"


def test_explicit_n8n_prior_work_is_experience() -> None:
    evidence = "Experience working with n8n or similar tools."
    claim = {
        "concept": "Experience working with n8n or similar tools",
        "depth_signal": None,
        "requirement_type": "required",
        "concept_type": "tool",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Source prior work.",
        "item_excerpt": evidence,
    }
    parsed = AnalysisRequirementV27.model_validate(
        claim,
        context={"analysis_mode": "english", "analysis_fields": {"description": evidence}},
    )
    assert parsed.concept_type == "experience"
