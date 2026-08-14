"""Candidate-only Instructor response model for P1.6 v17.

The accepted P1.6 schema historically capped ``requirements`` at 32. Later source-led coverage
rules can legitimately require more records than that on dense postings, so v17 removes only that
arbitrary array bound while preserving every v14/v16 requirement validator.
"""

from __future__ import annotations

from pydantic import Field

from jobhunter.inference.instructor_lm_studio_v14 import (
    AnalysisRequirementV14,
    JobAnalysisResponseV14,
)


class JobAnalysisResponseV17(JobAnalysisResponseV14):
    """P1.6 candidate response whose requirement count follows supported source evidence."""

    requirements: list[AnalysisRequirementV14] = Field()


__all__ = ["JobAnalysisResponseV17"]
