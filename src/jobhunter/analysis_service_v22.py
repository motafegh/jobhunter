"""Isolated P1.6 v22 candidate service.

V22 is not public/current routing. It keeps v21 exact-item evidence and adds one
versioned ontology-abstention rule for unsupported experience classification.
"""

from jobhunter.analysis_service_v21 import (
    ANALYSIS_SCHEMA_VERSION,
    JobAnalysisServiceV21,
    _ENGLISH_SYSTEM_PROMPT_V21,
)

ENGLISH_PROMPT_VERSION = "job-analysis-english-v22"

_V22_RULES = """

P1.6 V22 CANDIDATE — ONTOLOGY ABSTENTION:
- Keep every v21 exact-item, coverage, obligation, depth, subject and provenance rule.
- concept_type=experience is allowed only when the exact item proves prior applied exposure or an
  exact source-backed checklist item explicitly requires experience.
- A source-backed capability requirement is still a valid factual requirement when prior experience
  is not stated. Do not invent historical experience merely because the capability is advanced.
- When the factual requirement is explicit but the exact item does not justify a more specific
  ontology type, use concept_type=other rather than fabricating experience.
- This abstention changes only the ontology label. Preserve concept, evidence, item_excerpt,
  requirement strength, depth and confidence according to their existing source-backed rules.
"""

_ENGLISH_SYSTEM_PROMPT_V22 = _ENGLISH_SYSTEM_PROMPT_V21 + _V22_RULES


class JobAnalysisServiceV22(JobAnalysisServiceV21):
    """Persist v22 candidates under a distinct prompt/runtime identity."""

    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = _ENGLISH_SYSTEM_PROMPT_V22
    schema_name = "jobhunter_job_analysis_english_v22"


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV22",
    "_ENGLISH_SYSTEM_PROMPT_V22",
    "_V22_RULES",
]
