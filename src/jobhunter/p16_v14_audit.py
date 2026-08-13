"""Mechanical audit helper for isolated English P1.6 v14 snapshots."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION
from jobhunter.analysis_service_v14 import ENGLISH_PROMPT_VERSION, qualification_list_spans, residual_requirement_spans


class AuditError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _normalize(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def audit_snapshot(path: Path, *, job_id: str) -> dict[str, int]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    _require(snapshot.get("source_job_id") == job_id, f"Snapshot is not for {job_id!r}")
    status = snapshot.get("status") or {}
    _require(status.get("english_projection_present") is True, "English projection is missing")
    _require(status.get("english_analysis_present") is True, "English P1.6 candidate is missing")
    _require(status.get("translation_matches_english_analysis") is True, "Projection/analysis mismatch")
    projection = snapshot.get("english_projection")
    analysis = snapshot.get("english_analysis")
    _require(isinstance(projection, dict), "English projection payload is missing")
    _require(isinstance(analysis, dict), "English analysis payload is missing")
    _require(analysis.get("prompt_version") == ENGLISH_PROMPT_VERSION, "Wrong P1.6 candidate contract")
    _require(analysis.get("schema_version") == ANALYSIS_SCHEMA_VERSION, "Wrong analysis schema")
    _require(analysis.get("translation_artifact_id") == projection.get("artifact_id"), "Wrong projection dependency")

    payload = analysis.get("analysis") or {}
    requirements = payload.get("requirements") or []
    responsibilities = payload.get("responsibilities") or []
    coverage = payload.get("coverage") or []
    fields = projection.get("fields") or {}
    skills = fields.get("skills") or []
    structured_skills = [item.strip() for item in skills if isinstance(item, str) and item.strip()]
    qualification_spans = qualification_list_spans(fields)
    residual_spans = residual_requirement_spans(fields)

    requirements_by_evidence: dict[str, list[dict[str, Any]]] = {}
    for index, item in enumerate(requirements):
        _require(isinstance(item, dict), f"requirement[{index}] is malformed")
        evidence = str(item.get("evidence") or "")
        requirements_by_evidence.setdefault(_normalize(evidence), []).append(item)
        concept = str(item.get("concept") or "")
        if str(item.get("concept_type") or "") in {"skill", "knowledge", "practice", "domain", "experience", "tool"}:
            _require(re.search(r"^ability\s+to\b", concept, re.I) is None, f"requirement[{index}] keeps Ability-to wrapper")
            _require(re.search(r"\b(?:full[ -]?time|part[ -]?time)\b", concept, re.I) is None, f"requirement[{index}] mixes schedule wording into capability concept")

    for skill in structured_skills:
        matches = requirements_by_evidence.get(_normalize(skill), [])
        _require(bool(matches), f"Structured skill missing: {skill!r}")
        _require(any(item.get("requirement_type") == "required" for item in matches), f"Structured skill strength changed: {skill!r}")
    for span in qualification_spans:
        _require(_normalize(span) in requirements_by_evidence, f"Qualification item missing: {span!r}")

    coverage_by_evidence = {
        _normalize(str(item.get("evidence") or "")): item
        for item in coverage if isinstance(item, dict)
    }
    for expected in [*structured_skills, *qualification_spans]:
        decision = coverage_by_evidence.get(_normalize(expected))
        _require(bool(decision and decision.get("disposition") == "extracted_requirement"), f"Extracted coverage missing: {expected!r}")
    for residual in residual_spans:
        decision = coverage_by_evidence.get(_normalize(residual))
        _require(bool(decision), f"Residual coverage missing: {residual!r}")
        _require(decision.get("disposition") in {"extracted_requirement", "excluded_non_requirement"}, f"Residual coverage invalid: {residual!r}")

    requirement_evidence = set(requirements_by_evidence)
    qualification_evidence = {_normalize(item) for item in qualification_spans}
    for index, item in enumerate(responsibilities):
        _require(isinstance(item, dict), f"responsibility[{index}] is malformed")
        statement = _normalize(str(item.get("statement") or ""))
        evidence = _normalize(str(item.get("evidence") or ""))
        _require(evidence not in requirement_evidence, f"responsibility[{index}] reuses requirement evidence")
        _require(evidence not in qualification_evidence, f"responsibility[{index}] uses qualification evidence")
        _require(not (statement and f"ability to {statement}" in evidence), f"responsibility[{index}] paraphrases ability-to qualification")

    decomposed = [item for item in coverage if isinstance(item, dict) and item.get("disposition") == "decomposed_requirement"]
    _require(bool(decomposed), "No coarse coverage marked decomposed")
    return {
        "artifact_id": int(analysis.get("artifact_id") or 0),
        "requirements": len(requirements),
        "responsibilities": len(responsibilities),
        "structured_skills": len(structured_skills),
        "qualification_spans": len(qualification_spans),
        "residual_spans": len(residual_spans),
        "decomposed": len(decomposed),
        "coverage": len(coverage),
    }
