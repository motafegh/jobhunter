"""Isolated, versioned P1.6 source-fidelity candidate behavioral checks."""
from __future__ import annotations

from jobhunter.analysis_runtime_v30 import V30CandidateAnalysisProvider
from jobhunter.analysis_runtime_v31 import V31CandidateAnalysisProvider
from jobhunter.analysis_service_v31 import JobAnalysisServiceV31
from jobhunter.evidence_refs_v31 import (
    exact_scoped_sections,
    v31_requirement_plan,
    v31_responsibility_plan,
    v31_scoped_additional_plan,
)
from jobhunter.source_section_spine import source_sections


def _provider(cls=V31CandidateAnalysisProvider):
    return cls(
        base_url="http://127.0.0.1:18080/v1",
        configured_model="test-model",
        api_token=None,
        timeout_seconds=2,
        max_retries=0,
    )


def test_edr_flattened_duties_and_qualifications_are_separate() -> None:
    description = (
        "Company background. Job Description • Deploy and configure EDR tools "
        "• Troubleshoot customers' security infrastructure "
        "• Prepare technical reports "
        "• Minimum 3 years of security experience "
        "• Mastery of network security concepts "
        "Advantages • Vendor certificates • Public sector experience "
        "Benefits • Health insurance"
    )
    sections = source_sections(description)
    assert [x.kind for x in sections] == (
        ["responsibilities"] * 3 + ["requirements"] * 2
        + ["preferred"] * 2 + ["arrangement"]
    )
    assert [x.inferred_boundary for x in sections] == (
        [False] * 3 + [True] * 2 + [False] * 3
    )
    assert all(description[x.start:x.end] == x.text for x in sections)
    assert not any("Health insurance" in s.text for s in sections if s.kind == "requirements")


def test_tiered_requirements_not_absorbed_by_preferred_section() -> None:
    description = (
        "Main Responsibilities: Build AI services. "
        "Required Skills: Familiarity with vector search. "
        "What are considered advantages: Familiarity with monitoring tools. "
        "Eligibility Criteria: Level Middle: 2 to 4 years and one practical AI project. "
        "Level Senior: 4 to 7 years and a deployed system. "
        "Working Conditions: Full time, hybrid."
    )
    sections = exact_scoped_sections(description)
    assert [x.kind for x in sections] == [
        "responsibilities", "requirements", "preferred",
        "eligibility_middle", "eligibility_senior", "arrangement",
    ]
    plan = _provider()._requirement_coverage_plan({"description": description})
    tags = {x.get("v31_source_section_kind") for x in plan.values()}
    assert {"requirements", "preferred", "eligibility_middle", "eligibility_senior"} <= tags
    tiers = [
        x for x in plan.values()
        if x.get("v31_source_section_kind", "").startswith("eligibility_")
    ]
    assert len(tiers) == 2
    assert all(x["obligation_hint"] == "required" for x in tiers)
    assert all(x["text"] in description for x in tiers)
    assert not any("4 to 7" in x["text"] for x in plan.values()
                   if x.get("v31_source_section_kind") == "preferred")


def test_preferred_heading_preserves_source_exact_boundary() -> None:
    description = (
        "Responsibilities: Write Python services. "
        "Required skills: Strong Python, practical backend experience, teamwork "
        "are scored based on: LLM framework experience, async programming"
    )
    plan = _provider()._requirement_coverage_plan({"description": description})
    required = [x for x in plan.values() if x.get("v31_source_section_kind") == "requirements"]
    preferred = [x for x in plan.values() if x.get("v31_source_section_kind") == "preferred"]
    assert len(required) == len(preferred) == 1
    assert "teamwork" in required[0]["text"]
    assert "LLM framework" not in required[0]["text"]
    assert "LLM framework" in preferred[0]["text"]
    assert "Strong Python" not in preferred[0]["text"]
    assert preferred[0]["obligation_context"].endswith(preferred[0]["text"])


def test_application_instructions_not_required_portfolio_skills() -> None:
    description = (
        "What do you do in this role? Build backend services. "
        "What is important to us? Strong Python and teamwork. "
        "Working conditions: Part time or full time. "
        "Please send us your resume. If you have a GitHub or portfolio "
        "that demonstrates skills, we would be happy to see it."
    )
    extra = {
        "field:__candidate_residual_requirement_evidence:0": {
            "text": ("If you have a GitHub or portfolio that demonstrates skills, "
                     "we would be happy to see it."),
            "source_kind": "candidate_residual_sentence",
            "obligation_hint": None,
            "allow_exclusion": True,
        }
    }
    adjusted = v31_scoped_additional_plan({"description": description}, extra)
    assert next(iter(adjusted.values()))["source_kind"] == "v31_nonqualification_context"
    assert next(iter(adjusted.values()))["obligation_hint"] == "context_only"
    out, excluded = _provider()._source_context_exclusions(adjusted)
    assert out == list(extra)
    assert excluded[0]["evidence_reference"] == list(extra)[0]


def test_optional_group_is_preferred_not_required() -> None:
    description = (
        "What is important to us? Strong Python knowledge and teamwork. "
        "Familiarity with financial markets, simulations, or LLMs "
        "is an advantage, but not a requirement. "
        "Why collaborate with us? Build useful products."
    )
    sections = exact_scoped_sections(description)
    assert [s.kind for s in sections] == [
        "requirements", "preferred", "context",
    ]
    assert sections[1].text.endswith("but not a requirement.")
    assert all(description[s.start:s.end] == s.text for s in sections)


def test_no_implicit_section_assignment_without_heading() -> None:
    description = (
        "We collaborate with partners and require professional standards. "
        "Experience in this industry may be useful for customers."
    )
    assert source_sections(description) == ()
    fields = {"description": description, "education": "Bachelor's degree"}
    inherited = {
        "field:education": {
            "text": "Bachelor's degree", "source_kind": "structured_field",
            "obligation_hint": "required", "allow_exclusion": False,
        }
    }
    assert v31_requirement_plan(fields, inherited) == inherited
    assert v31_responsibility_plan(fields, {}) == {}


def test_structured_fields_are_not_removed_by_overlays() -> None:
    fields = {
        "description": "Responsibilities: Write Python APIs. Required Skills: SQL experience.",
        "education": "Bachelor's degree",
        "minimum_experience": "3 to 6 years",
    }
    base = _provider(V30CandidateAnalysisProvider)._requirement_coverage_plan(fields)
    adjusted = v31_requirement_plan(fields, base)
    assert adjusted["field:education"]["text"] == "Bachelor's degree"
    assert adjusted["field:minimum_experience"]["text"] == "3 to 6 years"
    work = v31_responsibility_plan(fields, {})
    assert len(work) == 1
    assert "Write Python APIs" in next(iter(work.values()))


def test_existing_public_v30_contract_not_modified() -> None:
    assert JobAnalysisServiceV31.prompt_version == "job-analysis-english-v31"
    assert V30CandidateAnalysisProvider is not V31CandidateAnalysisProvider


def test_retains_existing_granular_qualification_references() -> None:
    """The new heading reader cannot replace a dense accepted ledger wholesale."""
    description = (
        "Requirements: Strong Python; Practical backend experience; "
        "Knowledge of SQL"
    )
    exact = [
        "Strong Python", "Practical backend experience", "Knowledge of SQL"
    ]
    inherited = {
        f"field:description:segment:0:clause:{i}": {
            "text": text,
            "source_kind": "requirement_section",
            "obligation_hint": "required",
            "allow_exclusion": False,
        } for i, text in enumerate(exact)
    }
    result = v31_requirement_plan({"description": description}, inherited)
    assert set(result) == set(inherited)
    assert all(result[k]["text"] == v["text"] for k, v in inherited.items())
    assert all(v["v31_source_section_kind"] == "requirements" for v in result.values())


def test_replaces_only_cross_heading_reference_and_preserves_adjacent_clauses() -> None:
    description = (
        "Requirements: Strong Python; Practical API experience; "
        "Teamwork. General Conditions: Ability to collaborate and learn"
    )
    inherited = {
        "first": {"text": "Strong Python", "source_kind": "requirement_section",
                  "obligation_hint": "required", "allow_exclusion": False},
        "second": {"text": "Practical API experience",
                   "source_kind": "requirement_section",
                   "obligation_hint": "required", "allow_exclusion": False},
        "field:description:cross": {
            "text": "Teamwork. General Conditions: Ability to collaborate and learn",
            "source_kind": "requirement_section",
            "obligation_hint": "required", "allow_exclusion": True,
        },
    }
    # The synthetic pre-existing labels use conventional description refs,
    # not fabricated structured field keys.
    inherited["field:description:0"] = inherited.pop("first")
    inherited["field:description:1"] = inherited.pop("second")
    result = v31_requirement_plan({"description": description}, inherited)
    assert "field:description:0" in result
    assert "field:description:1" in result
    assert "field:description:cross" not in result
    assert any("Teamwork." in c["text"] for c in result.values())
    assert any("Ability to collaborate" in c["text"] for c in result.values())
    for c in result.values():
        if "v31_source_offset" in c:
            assert description[c["v31_source_offset"]:c["v31_source_end"]] == c["text"]


def test_section_scope_does_not_override_unrelated_structured_requirement() -> None:
    text = (
        "Requirements: Practical Linux experience. "
        "Preferred qualifications: Experience with Linux containers."
    )
    inherited = {
        "field:education": {
            "text": "Bachelor's degree", "source_kind": "structured_field",
            "obligation_hint": "required", "allow_exclusion": False,
        },
    }
    result = v31_requirement_plan({"description": text}, inherited)
    assert result["field:education"] == inherited["field:education"]
    assert sum(v["obligation_hint"] == "preferred" for k, v in result.items()
               if k.startswith("field:description:")) == 1


def test_structured_tag_source_explicit_nonrequired_conflict_is_reported() -> None:
    from jobhunter.source_obligation_conflicts import (
        structured_skill_preference_conflicts,
    )

    description = (
        "What is important to us? Strong Python proficiency. "
        "Familiarity with trading systems or LLMs is an advantage, "
        "but not a requirement."
    )
    fields = {"description": description, "skills": ["LLM", "Python"]}
    conflicts = structured_skill_preference_conflicts(fields)
    assert [item.skill for item in conflicts] == ["LLM"]
    assert "not a requirement" in conflicts[0].source_text
    assert (
        description[
            conflicts[0].source_section_start:conflicts[0].source_section_end
        ]
        == conflicts[0].source_text
    )
    assert conflicts[0].reason.endswith("source_nonrequired")


def test_structured_skill_flags_are_advisory_not_automatic_demotions() -> None:
    from jobhunter.source_obligation_conflicts import (
        structured_skill_preference_conflicts,
    )

    fields = {
        "description": (
            "Required Skills: Deep experience with Python and SQL. "
            "Advantages: Familiarity with RAG."
        ),
        "skills": ["Python", "SQL", "RAG"],
    }
    assert structured_skill_preference_conflicts(fields) == ()
    assert structured_skill_preference_conflicts({
        "description": "General work on LLMAgents is optional.",
        "skills": ["LLM"],
    }) == ()


def test_conflict_detection_never_invents_unknown_metadata() -> None:
    from jobhunter.source_obligation_conflicts import (
        structured_skill_preference_conflicts,
    )

    assert structured_skill_preference_conflicts({
        "description": "Optional LLM awareness.",
    }) == ()
    assert structured_skill_preference_conflicts({
        "skills": ["LLM"],
    }) == ()
