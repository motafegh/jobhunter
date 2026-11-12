"""V31 candidate: source-exact section-scoped preferred qualification validation."""
from __future__ import annotations

from typing import Any

from pydantic import Field

from jobhunter.inference.instructor_lm_studio_v30 import (
    AnalysisRequirementV30,
    JobAnalysisResponseV30,
)


class AnalysisRequirementV31(AnalysisRequirementV30):
    def _has_exact_preference_signal(
        self, text: str, plan: dict[str, Any]
    ) -> bool:
        if super()._has_exact_preference_signal(text, plan):
            return True
        # The canonical v30 guard does not recognize plural "advantages"
        # or "are scored based on" when the preference occurs in an exact
        # heading separate from the individual evidence span. Only an
        # internally built section reference qualifies here; the model
        # cannot assert this marker in its generated candidate.
        return any(
            isinstance(candidate, dict)
            and candidate.get("v31_source_section_kind") == "preferred"
            and candidate.get("obligation_hint") == "preferred"
            and candidate.get("text") == self.evidence
            and candidate.get("text") == text
            and isinstance(candidate.get("obligation_context"), str)
            and candidate["obligation_context"].endswith(self.evidence)
            for candidate in plan.values()
        )


class JobAnalysisResponseV31(JobAnalysisResponseV30):
    requirements: list[AnalysisRequirementV31] = Field()


__all__ = ["AnalysisRequirementV31", "JobAnalysisResponseV31"]
