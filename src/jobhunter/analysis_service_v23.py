"""Isolated P1.6 v23 candidate: source-backed proof preferences and claim wording."""

from jobhunter.analysis_service_v21 import (
    _ENGLISH_SYSTEM_PROMPT_V21,
    ANALYSIS_SCHEMA_VERSION,
)
from jobhunter.analysis_service_v22 import JobAnalysisServiceV22

ENGLISH_PROMPT_VERSION = "job-analysis-english-v23"

_V23_RULES = """

P1.6 V23 CANDIDATE — CLAIM WORDING AND PROOF OF ABILITY:
- Keep every v21 exact-item, coverage, obligation, depth, subject and provenance rule.
- A concept must express only the meaning supported by its exact item_excerpt. Never use
  "experience" or another prior-work assertion in a concept for an ability-only item,
  regardless of concept_type. An advanced ability does not establish previous delivery.
- Use concept_type=experience only for exact prior applied exposure. If a capability is
  explicit but its exact item does not establish prior exposure, describe the capability
  itself accurately and use an appropriate non-experience concept type. Do not rely on
  an ontology label change to repair inaccurate concept wording.
- A candidate_proof reference is an explicit preference for demonstrating prior work.
  Represent its exact source assertion as preferred and concept_type=other. Preserve
  alternatives such as a repository, project, demo or explanation; do not turn one
  alternative into a mandatory tool, credential or paid-employment requirement.
- Keep proof-of-ability preferences separate from substantive technical ability and
  experience requirements. Application instructions about sending a resume or links
  are not additional qualifications. Do not extract requirements from such instructions.
- Preserve every inherited strict source, strength, depth and full-coverage rule.
"""

_ENGLISH_SYSTEM_PROMPT_V23 = _ENGLISH_SYSTEM_PROMPT_V21 + _V23_RULES


class JobAnalysisServiceV23(JobAnalysisServiceV22):
    """Persist only explicitly selected v23 candidates under a distinct identity."""

    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = _ENGLISH_SYSTEM_PROMPT_V23
    schema_name = "jobhunter_job_analysis_english_v23"


__all__ = [
    "ANALYSIS_SCHEMA_VERSION",
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV23",
    "_ENGLISH_SYSTEM_PROMPT_V23",
    "_V23_RULES",
]
