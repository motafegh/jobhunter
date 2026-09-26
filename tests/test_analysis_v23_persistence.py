"""The persisted v23 ledger must match the model-facing versioned source plan."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_service import AnalysisValidationError, _analysis_fields_for_english
from jobhunter.analysis_service_v23 import JobAnalysisServiceV23
from jobhunter.evidence_refs_v21 import build_responsibility_coverage_plan_v21
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23

_ROOT = Path(__file__).resolve().parents[1]


def _source_plan():
    projection = json.loads(
        (_ROOT / "corpus/jobs/tvMm/english-projection.json").read_text()
    )
    fields = _analysis_fields_for_english(projection["fields"])
    return (
        fields,
        build_requirement_coverage_plan_v23(fields),
        build_responsibility_coverage_plan_v21(fields),
    )


def _complete_structured(fields, requirements, responsibilities):
    return {
        "role_purpose": [],
        "requirements": [
            {"concept": "Source item", "evidence": candidate["text"]}
            for candidate in requirements.values()
            if candidate.get("obligation_hint") != "context_only"
        ] + [
            {"concept": skill, "evidence": skill}
            for skill in fields["skills"]
        ],
        "responsibilities": [
            {"statement": evidence, "evidence": evidence}
            for evidence in responsibilities.values()
        ],
        "coverage_exclusions": [],
    }


def test_v23_persistence_accounts_for_the_exact_generation_ledger() -> None:
    fields, requirement_plan, responsibility_plan = _source_plan()
    structured = _complete_structured(fields, requirement_plan, responsibility_plan)

    analysis = JobAnalysisServiceV23._persist_analysis(
        object.__new__(JobAnalysisServiceV23), structured, fields
    )

    expected = {item["text"] for item in requirement_plan.values()}
    expected.update(fields["skills"])
    assert {item["evidence"] for item in analysis["coverage"]} == expected
    assert len(analysis["responsibility_coverage"]) == len(responsibility_plan) == 11
    assert all(item["disposition"] == "extracted_requirement"
               for item in analysis["coverage"])
    assert all(item["disposition"] == "responsibility"
               for item in analysis["responsibility_coverage"])


def test_v23_persistence_fails_closed_on_missing_or_excluded_proof() -> None:
    fields, requirement_plan, responsibility_plan = _source_plan()
    structured = _complete_structured(fields, requirement_plan, responsibility_plan)
    proof_ref, proof = next(
        (reference, item) for reference, item in requirement_plan.items()
        if item.get("source_kind") == "candidate_proof"
    )
    structured["requirements"] = [
        item for item in structured["requirements"] if item["evidence"] != proof["text"]
    ]

    with pytest.raises(AnalysisValidationError, match="Unaccounted v23 requirement"):
        persisted_analysis_v23(structured, fields)

    structured["coverage_exclusions"] = [
        {"evidence_reference": proof_ref, "rationale": "Do not bypass proof"}
    ]
    with pytest.raises(AnalysisValidationError, match="unknown or prohibited"):
        persisted_analysis_v23(structured, fields)
