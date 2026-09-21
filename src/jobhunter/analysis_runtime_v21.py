"""Offline runtime boundary for the isolated P1.6 v21 scoped-evidence candidate."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_runtime_v20 import V20CandidateAnalysisProvider
from jobhunter.inference.instructor_lm_studio_v21 import (
    complete_analysis_partition_with_instructor_v21,
    persisted_v20_shape,
)
from jobhunter.inference.lm_studio import StructuredInferenceResult


class V21CandidateAnalysisProvider(V20CandidateAnalysisProvider):
    """Use v21 validation while returning the unchanged v5 persistable shape."""

    def _complete_partition(self, **kwargs: Any) -> StructuredInferenceResult:
        return complete_analysis_partition_with_instructor_v21(**kwargs)

    def _persistable_structured(self, structured: dict[str, Any]) -> dict[str, Any]:
        persisted = persisted_v20_shape(structured)
        return {str(key): value for key, value in persisted.items()}


__all__ = ["V21CandidateAnalysisProvider"]
