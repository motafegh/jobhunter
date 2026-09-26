"""Persist v23 exact source coverage from the same planner used by inference."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.evidence_refs_v21 import build_responsibility_coverage_plan_v21
from jobhunter.evidence_refs_v23 import build_requirement_coverage_plan_v23


def _key(text: str) -> str:
    return " ".join(text.replace("\u200c", " ").split()).casefold()


def persisted_analysis_v23(
    structured: dict[str, Any], analysis_fields: dict[str, Any]
) -> dict[str, Any]:
    """Resolve v23 references without silently reverting to an older coverage plan."""

    requirement_plan = build_requirement_coverage_plan_v23(analysis_fields)
    responsibility_plan = build_responsibility_coverage_plan_v21(analysis_fields)
    requirements = structured.get("requirements") or []
    responsibilities = structured.get("responsibilities") or []
    role_purpose = structured.get("role_purpose") or []
    requirement_evidence = {_key(str(item.get("evidence") or "")) for item in requirements}
    responsibility_evidence = {
        _key(str(item.get("evidence") or "")) for item in responsibilities
    }
    purpose_evidence = {_key(str(item.get("evidence") or "")) for item in role_purpose}

    exclusions: dict[str, dict[str, Any]] = {}
    for item in structured.get("coverage_exclusions") or []:
        reference = str(item.get("evidence_reference") or "")
        candidate = requirement_plan.get(reference)
        if candidate is None or not candidate.get("allow_exclusion", False):
            raise AnalysisValidationError(
                f"V23 exclusion is unknown or prohibited: {reference!r}"
            )
        if reference in exclusions:
            raise AnalysisValidationError(f"V23 exclusion repeats: {reference!r}")
        exclusions[reference] = item

    coverage: list[dict[str, str]] = []
    for reference, candidate in requirement_plan.items():
        evidence = str(candidate["text"])
        cited = _key(evidence) in requirement_evidence
        excluded = exclusions.get(reference)
        if cited and excluded is not None:
            raise AnalysisValidationError(
                f"V23 requirement is both cited and excluded: {reference!r}"
            )
        if candidate.get("obligation_hint") == "context_only":
            if cited or excluded is not None:
                raise AnalysisValidationError(
                    f"V23 context-only reference has a claim or exclusion: {reference!r}"
                )
            disposition = "context_modifier"
            rationale = "Deterministic source context for obligation strength."
        elif cited:
            disposition = "extracted_requirement"
            rationale = "A persisted requirement cites this exact v23 coverage input."
        elif excluded is not None:
            disposition = "excluded_non_requirement"
            rationale = str(excluded.get("rationale") or "")
        else:
            raise AnalysisValidationError(
                f"Unaccounted v23 requirement coverage reference: {reference!r}"
            )
        coverage.append(
            {"evidence": evidence, "disposition": disposition, "rationale": rationale}
        )

    seen = {_key(item["evidence"]) for item in coverage}
    for skill in analysis_fields.get("skills") or []:
        if not isinstance(skill, str) or not skill.strip():
            continue
        evidence = skill.strip()
        normalized = _key(evidence)
        if normalized not in requirement_evidence:
            raise AnalysisValidationError(f"Structured skill disappeared: {evidence!r}")
        if normalized not in seen:
            coverage.append({
                "evidence": evidence,
                "disposition": "extracted_requirement",
                "rationale": "Deterministic structured source skill coverage.",
            })
            seen.add(normalized)

    responsibility_coverage: list[dict[str, str]] = []
    for reference, evidence in responsibility_plan.items():
        normalized = _key(evidence)
        if normalized in purpose_evidence and normalized in responsibility_evidence:
            raise AnalysisValidationError(
                f"V23 work is both purpose and responsibility: {reference!r}"
            )
        if normalized in purpose_evidence:
            disposition = "role_purpose"
        elif normalized in responsibility_evidence:
            disposition = "responsibility"
        else:
            raise AnalysisValidationError(
                f"Unaccounted v23 responsibility coverage reference: {reference!r}"
            )
        responsibility_coverage.append(
            {"evidence": evidence, "disposition": disposition}
        )

    return {
        "role_purpose": role_purpose,
        "responsibilities": responsibilities,
        "requirements": requirements,
        "coverage": coverage,
        "responsibility_coverage": responsibility_coverage,
    }


__all__ = ["persisted_analysis_v23"]
