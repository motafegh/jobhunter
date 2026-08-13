"""Mechanical audit helper for isolated English P1.6 v15 snapshots."""

from __future__ import annotations

import json
import re
from pathlib import Path

from jobhunter.analysis_service import ANALYSIS_SCHEMA_VERSION
from jobhunter.analysis_service_v14 import qualification_list_spans, residual_requirement_spans
from jobhunter.analysis_service_v15 import ENGLISH_PROMPT_VERSION


class AuditError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _norm(value: str) -> str:
    return " ".join(value.replace("\u200c", " ").split()).casefold()


def audit_snapshot(path: Path, *, job_id: str) -> dict[str, int]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    analysis = snapshot.get("english_analysis") or {}
    projection = snapshot.get("english_projection") or {}
    _require(snapshot.get("source_job_id") == job_id, "Wrong job snapshot")
    _require(
        analysis.get("prompt_version") == ENGLISH_PROMPT_VERSION,
        "Wrong P1.6 candidate contract",
    )
    _require(
        analysis.get("schema_version") == ANALYSIS_SCHEMA_VERSION,
        "Wrong analysis schema",
    )
    _require(
        analysis.get("translation_artifact_id") == projection.get("artifact_id"),
        "Wrong projection dependency",
    )

    payload = analysis.get("analysis") or {}
    requirements = payload.get("requirements") or []
    responsibilities = payload.get("responsibilities") or []
    coverage = payload.get("coverage") or []
    fields = projection.get("fields") or {}
    skills = [
        value.strip()
        for value in (fields.get("skills") or [])
        if isinstance(value, str) and value.strip()
    ]
    qualification_spans = qualification_list_spans(fields)
    residual_spans = residual_requirement_spans(fields)
    requirement_evidence = {
        _norm(str(item.get("evidence") or "")) for item in requirements
    }
    coverage_by_evidence = {
        _norm(str(item.get("evidence") or "")): item
        for item in coverage
        if isinstance(item, dict)
    }

    for expected in [*skills, *qualification_spans]:
        _require(_norm(expected) in requirement_evidence, f"Missing: {expected!r}")
        decision = coverage_by_evidence.get(_norm(expected)) or {}
        _require(
            decision.get("disposition") == "extracted_requirement",
            f"Missing extracted coverage: {expected!r}",
        )
    for residual in residual_spans:
        decision = coverage_by_evidence.get(_norm(residual)) or {}
        _require(
            decision.get("disposition")
            in {"extracted_requirement", "excluded_non_requirement"},
            f"Residual not accounted: {residual!r}",
        )

    for index, item in enumerate(requirements):
        concept = str(item.get("concept") or "")
        depth_signal = str(item.get("depth_signal") or "")
        _require(
            re.search(r"\b(?:full[ -]?time|part[ -]?time)\b", depth_signal, re.I)
            is None,
            f"requirement[{index}] depth_signal contains schedule wording",
        )
        if str(item.get("concept_type") or "") == "skill":
            _require(
                re.search(r"^ability\s+to\b", concept, re.I) is None,
                f"requirement[{index}] keeps Ability-to wrapper",
            )
            _require(
                re.search(r"\b(?:full[ -]?time|part[ -]?time)\b", concept, re.I)
                is None,
                f"requirement[{index}] contains schedule wording",
            )

    decomposed = sum(
        1
        for item in coverage
        if isinstance(item, dict)
        and item.get("disposition") == "decomposed_requirement"
    )
    _require(decomposed > 0, "No coarse coverage marked decomposed")
    return {
        "artifact_id": int(analysis.get("artifact_id") or 0),
        "requirements": len(requirements),
        "responsibilities": len(responsibilities),
        "structured_skills": len(skills),
        "qualification_spans": len(qualification_spans),
        "residual_spans": len(residual_spans),
        "decomposed": decomposed,
        "coverage": len(coverage),
    }
