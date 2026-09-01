"""Typed contracts for P2.2A Job Work Intelligence v2.

The model-facing candidate contract contains only bounded analytical decisions. The persisted
artifact is assembled separately so exact accepted P1.6 work statements, not model paraphrases,
carry factual action authority.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Confidence = Literal["high", "medium", "low"]
RelativeEmphasis = Literal["primary", "supporting", "uncertain"]
WorkEvidenceStatus = Literal["sufficient", "limited"]
DeliverableStatus = Literal["source_explicit", "strongly_implied_by_work"]
AcceptedWorkKind = Literal["responsibility", "role_purpose"]


def _bounded_text(value: str, *, field_name: str, minimum: int, maximum: int) -> str:
    normalized = " ".join(value.split())
    if len(normalized) < minimum:
        raise ValueError(f"{field_name} must contain at least {minimum} characters")
    if len(normalized) > maximum:
        raise ValueError(f"{field_name} may contain at most {maximum} characters")
    return normalized


def _exact_statement(value: str) -> str:
    """Validate an accepted factual statement without normalizing or rewriting it."""

    if not value.strip():
        raise ValueError("statement must not be empty")
    if len(value) > 2400:
        raise ValueError("statement may contain at most 2400 characters")
    return value


def _unique_nonnegative(values: list[int], *, field_name: str) -> list[int]:
    unique = list(dict.fromkeys(values))
    if any(value < 0 for value in unique):
        raise ValueError(f"{field_name} must contain only zero-based non-negative indices")
    return unique


def _optional_bounded_text(
    value: str | None,
    *,
    field_name: str,
    minimum: int,
    maximum: int,
) -> str | None:
    if value is None:
        return None
    return _bounded_text(value, field_name=field_name, minimum=minimum, maximum=maximum)


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CandidateWorkTheme(_StrictModel):
    """One model-proposed grouping of accepted direct-work references."""

    theme_id: str = Field(pattern=r"^theme-[1-9][0-9]*$")
    label: str
    emphasis: RelativeEmphasis
    confidence: Confidence
    responsibility_indices: list[int] = Field(max_length=24)
    role_purpose_indices: list[int] = Field(max_length=8)
    supporting_requirement_indices: list[int] = Field(default_factory=list, max_length=24)
    rationale: str | None = None

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str | None) -> str | None:
        return _optional_bounded_text(
            value,
            field_name="rationale",
            minimum=6,
            maximum=1000,
        )

    @field_validator(
        "responsibility_indices",
        "role_purpose_indices",
        "supporting_requirement_indices",
    )
    @classmethod
    def indices_are_unique(cls, values: list[int], info) -> list[int]:
        return _unique_nonnegative(values, field_name=info.field_name)

    @model_validator(mode="after")
    def requires_direct_work_evidence(self) -> CandidateWorkTheme:
        if not self.responsibility_indices and not self.role_purpose_indices:
            raise ValueError(
                "A work theme requires at least one responsibility or role-purpose reference; "
                "requirements alone cannot become duties"
            )
        return self


class CandidateDeliverable(_StrictModel):
    """A model-proposed output backed by accepted direct work, never generic tool knowledge."""

    label: str
    status: DeliverableStatus
    confidence: Confidence
    responsibility_indices: list[int] = Field(max_length=16)
    role_purpose_indices: list[int] = Field(max_length=8)
    rationale: str | None = None

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str | None) -> str | None:
        return _optional_bounded_text(
            value,
            field_name="rationale",
            minimum=6,
            maximum=1000,
        )

    @field_validator("responsibility_indices", "role_purpose_indices")
    @classmethod
    def indices_are_unique(cls, values: list[int], info) -> list[int]:
        return _unique_nonnegative(values, field_name=info.field_name)

    @model_validator(mode="after")
    def requires_work_support(self) -> CandidateDeliverable:
        if not self.responsibility_indices and not self.role_purpose_indices:
            raise ValueError("Deliverable candidates require direct work evidence")
        if self.status == "strongly_implied_by_work" and self.rationale is None:
            raise ValueError("Work-implied deliverables require an interpretation rationale")
        return self


class CandidateRoleInterpretation(_StrictModel):
    """Tentative job-local role interpretation; not a promoted archetype."""

    label: str
    confidence: Confidence
    supporting_theme_ids: list[str] = Field(min_length=1, max_length=8)
    alternatives: list[str] = Field(default_factory=list, max_length=4)
    limitations: list[str] = Field(default_factory=list, max_length=6)

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=140)

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


class CandidateJobWorkIntelligence(_StrictModel):
    """Model-returned P2.2A candidate containing interpretation and structured references only."""

    evidence_status: WorkEvidenceStatus
    work_themes: list[CandidateWorkTheme] = Field(default_factory=list, max_length=8)
    deliverables: list[CandidateDeliverable] = Field(default_factory=list, max_length=8)
    role_interpretation: CandidateRoleInterpretation | None = None
    limitations: list[str] = Field(default_factory=list, max_length=8)

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
    def evidence_state_contract(self) -> CandidateJobWorkIntelligence:
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


class AcceptedWorkItem(_StrictModel):
    """Exact accepted P1.6 work copied deterministically into the final artifact."""

    kind: AcceptedWorkKind
    index: int = Field(ge=0)
    statement: str
    confidence: Confidence | None = None

    @field_validator("statement")
    @classmethod
    def statement_is_exact_and_usable(cls, value: str) -> str:
        return _exact_statement(value)


class WorkTheme(_StrictModel):
    """Persisted theme: candidate grouping plus deterministic accepted factual work."""

    theme_id: str = Field(pattern=r"^theme-[1-9][0-9]*$")
    label: str
    emphasis: RelativeEmphasis
    confidence: Confidence
    accepted_work_items: list[AcceptedWorkItem] = Field(min_length=1, max_length=32)
    supporting_requirement_indices: list[int] = Field(default_factory=list, max_length=24)
    rationale: str | None = None

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("supporting_requirement_indices")
    @classmethod
    def supporting_indices_are_unique(cls, values: list[int]) -> list[int]:
        return _unique_nonnegative(values, field_name="supporting_requirement_indices")

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str | None) -> str | None:
        return _optional_bounded_text(
            value,
            field_name="rationale",
            minimum=6,
            maximum=1000,
        )

    @model_validator(mode="after")
    def accepted_work_is_unique(self) -> WorkTheme:
        identities = [(item.kind, item.index) for item in self.accepted_work_items]
        if len(identities) != len(set(identities)):
            raise ValueError("accepted work items must be unique by source kind and index")
        return self


class DeliverableCandidate(_StrictModel):
    """Persisted candidate deliverable with deterministic accepted-work support."""

    label: str
    status: DeliverableStatus
    confidence: Confidence
    accepted_work_items: list[AcceptedWorkItem] = Field(min_length=1, max_length=24)
    rationale: str | None = None

    @field_validator("label")
    @classmethod
    def label_bounds(cls, value: str) -> str:
        return _bounded_text(value, field_name="label", minimum=2, maximum=120)

    @field_validator("rationale")
    @classmethod
    def rationale_bounds(cls, value: str | None) -> str | None:
        return _optional_bounded_text(
            value,
            field_name="rationale",
            minimum=6,
            maximum=1000,
        )

    @model_validator(mode="after")
    def accepted_work_contract(self) -> DeliverableCandidate:
        identities = [(item.kind, item.index) for item in self.accepted_work_items]
        if len(identities) != len(set(identities)):
            raise ValueError("deliverable accepted work items must be unique")
        if self.status == "strongly_implied_by_work" and self.rationale is None:
            raise ValueError("Work-implied deliverables require an interpretation rationale")
        return self


class JobWorkIntelligence(_StrictModel):
    """Persisted candidate artifact for ``job-work-intelligence-v2``."""

    evidence_status: WorkEvidenceStatus
    work_themes: list[WorkTheme] = Field(default_factory=list, max_length=8)
    deliverables: list[DeliverableCandidate] = Field(default_factory=list, max_length=8)
    role_interpretation: CandidateRoleInterpretation | None = None
    limitations: list[str] = Field(default_factory=list, max_length=8)

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
    "AcceptedWorkItem",
    "AcceptedWorkKind",
    "CandidateDeliverable",
    "CandidateJobWorkIntelligence",
    "CandidateRoleInterpretation",
    "CandidateWorkTheme",
    "Confidence",
    "DeliverableCandidate",
    "DeliverableStatus",
    "JobWorkIntelligence",
    "RelativeEmphasis",
    "WorkEvidenceStatus",
    "WorkTheme",
]
