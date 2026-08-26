"""Typed candidate contract for P2.2A Job Work Intelligence v1.

This module intentionally models *analytical interpretation*, not employer-authored truth and not
promoted canonical taxonomy. Source/state integrity is validated elsewhere against the accepted
P1.6 dependency; these models bound the shape of useful job-level work interpretation.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Confidence = Literal["high", "medium", "low"]
RelativeEmphasis = Literal["primary", "supporting", "uncertain"]
WorkEvidenceStatus = Literal["sufficient", "limited"]
DeliverableStatus = Literal["source_explicit", "strongly_implied_by_work"]


def _bounded_text(value: str, *, field_name: str, minimum: int, maximum: int) -> str:
    normalized = " ".join(value.split())
    if len(normalized) < minimum:
        raise ValueError(f"{field_name} must contain at least {minimum} characters")
    if len(normalized) > maximum:
        raise ValueError(f"{field_name} may contain at most {maximum} characters")
    return normalized


def _unique_nonnegative(values: list[int], *, field_name: str) -> list[int]:
    unique = list(dict.fromkeys(values))
    if any(value < 0 for value in unique):
        raise ValueError(f"{field_name} must contain only zero-based non-negative indices")
    return unique


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class WorkTheme(_StrictModel):
    """One candidate grouping of directly supported work."""

    theme_id: str = Field(pattern=r"^theme-[1-9][0-9]*$")
    label: str
    summary: str
    emphasis: RelativeEmphasis
    confidence: Confidence
    responsibility_indices: list[int] = Field(default_factory=list, max_length=24)
    role_purpose_indices: list[int] = Field(default_factory=list, max_length=8)
    supporting_requirement_indices: list[int] = Field(default_factory=list, max_length=24)
    rationale: str

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("summary")
    @classmethod
    def summary_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="summary", minimum=8, maximum=800)

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="rationale", minimum=6, maximum=1000)

    @field_validator(
        "responsibility_indices",
        "role_purpose_indices",
        "supporting_requirement_indices",
    )
    @classmethod
    def indices_are_unique(cls, values: list[int], info) -> list[int]:
        return _unique_nonnegative(values, field_name=info.field_name)

    @model_validator(mode="after")
    def requires_direct_work_evidence(self) -> WorkTheme:
        if not self.responsibility_indices and not self.role_purpose_indices:
            raise ValueError(
                "A work theme requires at least one responsibility or role-purpose reference; "
                "requirements alone cannot become duties"
            )
        return self


class DeliverableCandidate(_StrictModel):
    """A source-explicit or work-implied output of the job, never generic tool knowledge."""

    label: str
    summary: str
    status: DeliverableStatus
    confidence: Confidence
    responsibility_indices: list[int] = Field(default_factory=list, max_length=16)
    role_purpose_indices: list[int] = Field(default_factory=list, max_length=8)
    rationale: str

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("summary")
    @classmethod
    def summary_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="summary", minimum=8, maximum=800)

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="rationale", minimum=6, maximum=1000)

    @field_validator("responsibility_indices", "role_purpose_indices")
    @classmethod
    def indices_are_unique(cls, values: list[int], info) -> list[int]:
        return _unique_nonnegative(values, field_name=info.field_name)

    @model_validator(mode="after")
    def requires_work_support(self) -> DeliverableCandidate:
        if not self.responsibility_indices and not self.role_purpose_indices:
            raise ValueError("Deliverable candidates require direct work evidence")
        return self


class CandidateRoleInterpretation(_StrictModel):
    """Tentative job-local role interpretation; not a promoted archetype."""

    label: str
    summary: str
    confidence: Confidence
    supporting_theme_ids: list[str] = Field(min_length=1, max_length=8)
    alternatives: list[str] = Field(default_factory=list, max_length=4)
    limitations: list[str] = Field(default_factory=list, max_length=6)

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=140)

    @field_validator("summary")
    @classmethod
    def summary_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="summary", minimum=10, maximum=1000)

    @field_validator("supporting_theme_ids")
    @classmethod
    def theme_ids_are_unique(cls, values: list[str]) -> list[str]:
        return list(dict.fromkeys(value.strip() for value in values if value.strip()))

    @field_validator("alternatives", "limitations")
    @classmethod
    def text_lists_are_bounded(cls, values: list[str]) -> list[str]:
        return list(
            dict.fromkeys(
                _bounded_text(value, field_name="item", minimum=2, maximum=300)
                for value in values
            )
        )


class JobWorkIntelligence(_StrictModel):
    """Candidate job-level interpretation persisted by ``job-work-intelligence-v1``."""

    evidence_status: WorkEvidenceStatus
    work_summary: str
    work_themes: list[WorkTheme] = Field(default_factory=list, max_length=8)
    deliverables: list[DeliverableCandidate] = Field(default_factory=list, max_length=8)
    role_interpretation: CandidateRoleInterpretation | None = None
    limitations: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("work_summary")
    @classmethod
    def summary_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="work_summary", minimum=10, maximum=1400)

    @field_validator("limitations")
    @classmethod
    def limitations_are_bounded(cls, values: list[str]) -> list[str]:
        return list(
            dict.fromkeys(
                _bounded_text(value, field_name="limitation", minimum=4, maximum=400)
                for value in values
            )
        )

    @model_validator(mode="after")
    def evidence_state_contract(self) -> JobWorkIntelligence:
        theme_ids = [theme.theme_id for theme in self.work_themes]
        if len(theme_ids) != len(set(theme_ids)):
            raise ValueError("work theme IDs must be unique")

        if self.evidence_status == "limited":
            if self.work_themes or self.deliverables or self.role_interpretation is not None:
                raise ValueError(
                    "limited work evidence cannot contain inferred duties, deliverables, or role "
                    "interpretation"
                )
            if not self.limitations:
                raise ValueError("limited work evidence requires an explicit limitation")
            return self

        if not self.work_themes:
            raise ValueError("sufficient work evidence requires at least one work theme")
        if self.role_interpretation is not None:
            unknown = set(self.role_interpretation.supporting_theme_ids) - set(theme_ids)
            if unknown:
                raise ValueError(
                    "role interpretation references unknown work themes: "
                    + ", ".join(sorted(unknown))
                )
        return self


__all__ = [
    "CandidateRoleInterpretation",
    "Confidence",
    "DeliverableCandidate",
    "DeliverableStatus",
    "JobWorkIntelligence",
    "RelativeEmphasis",
    "WorkEvidenceStatus",
    "WorkTheme",
]
