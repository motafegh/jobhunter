"""Candidate-only Instructor response model for P1.6 v17.

The accepted P1.6 schema historically capped ``requirements`` at 32. Later source-led coverage
rules can legitimately require more records than that on dense postings, so v17 removes that
arbitrary array bound while preserving the accepted requirement-item validators.

The first live dense v17 run exposed a second mechanical issue: the inherited response-level
coverage validator raised on the first missing requirement reference. With one bounded Instructor
retry, the model could therefore repair one omission only to discover the next omission after the
retry budget was exhausted. V17 keeps one bounded retry, but reports every requirement-coverage
and responsibility-coverage defect together so the correction receives the complete repair set.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, ValidationInfo, model_validator

from jobhunter.inference.instructor_lm_studio import (
    _normalize,
    _source_is_information_rich,
)
from jobhunter.inference.instructor_lm_studio_v14 import (
    AnalysisRequirementV14,
    JobAnalysisResponseV14,
)


class JobAnalysisResponseV17(JobAnalysisResponseV14):
    """Source-led response with aggregate dense-coverage correction feedback."""

    requirements: list[AnalysisRequirementV14] = Field()

    @model_validator(mode="after")
    def normalize_and_validate_quality(self, info: ValidationInfo) -> JobAnalysisResponseV17:
        """Preserve shared quality rules but expose all dense coverage defects at once.

        Pydantic model-validator overrides are intentional here: the accepted/public response model
        remains unchanged, while this isolated candidate replaces only the historical fail-fast
        response-level coverage loop. Requirement-item evidence/depth/optionality validators still
        come from ``AnalysisRequirementV14``.
        """

        seen_responsibilities: set[tuple[str, str]] = set()
        responsibilities = []
        for item in self.responsibilities:
            key = (_normalize(item.statement), _normalize(item.evidence))
            if key in seen_responsibilities:
                continue
            seen_responsibilities.add(key)
            responsibilities.append(item)
        self.responsibilities = responsibilities

        seen_requirements: set[tuple[str, str, str]] = set()
        requirements: list[AnalysisRequirementV14] = []
        for item in self.requirements:
            key = (
                _normalize(item.concept),
                item.requirement_type,
                _normalize(item.evidence),
            )
            if key in seen_requirements:
                continue
            seen_requirements.add(key)
            requirements.append(item)
        self.requirements = requirements

        context = info.context or {}
        fields = context.get("analysis_fields")
        if (
            isinstance(fields, dict)
            and _source_is_information_rich(fields)
            and not self.responsibilities
            and not self.requirements
        ):
            raise ValueError(
                "Information-rich job fields cannot be accepted with both responsibilities "
                "and requirements empty; extract supported career claims or explicitly narrow "
                "the source interpretation on retry."
            )

        coverage_plan = context.get("requirement_coverage_plan") or {}
        missing_non_excludable: list[str] = []
        unaccounted_excludable: list[str] = []
        obligation_mismatches: list[str] = []
        double_accounted: list[str] = []
        context_only_conflicts: list[str] = []
        illegally_excluded_required: list[str] = []

        if coverage_plan:
            exclusions = {item.evidence_reference: item for item in self.coverage_exclusions}
            if len(exclusions) != len(self.coverage_exclusions):
                raise ValueError("Requirement coverage exclusions contain duplicate references")

            requirements_by_evidence: dict[str, list[AnalysisRequirementV14]] = {}
            for item in self.requirements:
                requirements_by_evidence.setdefault(_normalize(item.evidence), []).append(item)

            for reference, candidate in coverage_plan.items():
                evidence = str(candidate["text"])
                matching = requirements_by_evidence.get(_normalize(evidence), [])
                if candidate.get("obligation_hint") == "context_only":
                    if matching or reference in exclusions:
                        context_only_conflicts.append(reference)
                    continue

                if matching:
                    if reference in exclusions:
                        double_accounted.append(reference)
                    obligation_hint = candidate.get("obligation_hint")
                    if obligation_hint in {"required", "preferred", "contextual"} and not any(
                        item.requirement_type == obligation_hint for item in matching
                    ):
                        obligation_mismatches.append(
                            f"{reference}=>{obligation_hint}"
                        )
                    continue

                if reference not in exclusions:
                    if candidate.get("allow_exclusion", False):
                        unaccounted_excludable.append(reference)
                    else:
                        missing_non_excludable.append(reference)
                    continue

                if not candidate.get("allow_exclusion", False):
                    illegally_excluded_required.append(reference)

        responsibility_plan = context.get("responsibility_coverage_plan") or {}
        missing_responsibilities: list[str] = []
        if responsibility_plan:
            represented_evidence = {
                _normalize(item.evidence)
                for item in [*self.role_purpose, *self.responsibilities]
            }
            missing_responsibilities = [
                reference
                for reference, evidence in responsibility_plan.items()
                if _normalize(evidence) not in represented_evidence
            ]

        has_defect = any(
            (
                missing_non_excludable,
                unaccounted_excludable,
                obligation_mismatches,
                double_accounted,
                context_only_conflicts,
                illegally_excluded_required,
                missing_responsibilities,
            )
        )
        if not has_defect:
            return self

        parts = [
            "Dense coverage validation failed. Correct ALL listed defects in the same retry; "
            "do not stop after repairing the first reference."
        ]
        if missing_non_excludable:
            parts.append(
                "missing_non_excludable_requirement_refs="
                f"{missing_non_excludable} (must be cited by requirements)"
            )
        if unaccounted_excludable:
            parts.append(
                "unaccounted_requirement_refs="
                f"{unaccounted_excludable} (extract each genuine qualification; otherwise add "
                "a justified coverage_exclusion)"
            )
        if obligation_mismatches:
            parts.append(f"obligation_mismatches={obligation_mismatches}")
        if double_accounted:
            parts.append(f"both_extracted_and_excluded={double_accounted}")
        if context_only_conflicts:
            parts.append(
                f"context_only_refs_must_not_be_extracted_or_excluded={context_only_conflicts}"
            )
        if illegally_excluded_required:
            parts.append(
                "non_excludable_refs_illegally_excluded="
                f"{illegally_excluded_required}"
            )
        if missing_responsibilities:
            parts.append(
                "missing_responsibility_refs="
                f"{missing_responsibilities} (represent each as role_purpose or responsibility)"
            )
        raise ValueError(" ".join(parts))


__all__ = ["JobAnalysisResponseV17"]
