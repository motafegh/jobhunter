"""Isolated P1.6 v24 candidate with one exact qualification ownership rule."""

from jobhunter.analysis_service_v23 import (
    _ENGLISH_SYSTEM_PROMPT_V23,
    JobAnalysisServiceV23,
)

ENGLISH_PROMPT_VERSION = "job-analysis-english-v24"

_V24_RULES = """

P1.6 V24 EXACT QUALIFICATION OWNERSHIP:
- Some exact qualification-item references fully decompose one broader source sentence.
  When the coverage ledger contains those items, extract every genuine item using its
  own exact reference. Do not additionally claim the broader sentence as a separate
  requirement or cite another partition's item reference.
- A broader sentence is removed from the model ledger only when the item excerpts
  account for its complete source wording and preserve the same obligation.
- All v23 source, subject, strength, depth, evidence, duty, and proof rules remain.
"""

_ENGLISH_SYSTEM_PROMPT_V24 = _ENGLISH_SYSTEM_PROMPT_V23 + _V24_RULES


class JobAnalysisServiceV24(JobAnalysisServiceV23):
    """Keep v5 persistence and semantic review under a distinct prompt identity."""

    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = _ENGLISH_SYSTEM_PROMPT_V24
    schema_name = "jobhunter_job_analysis_english_v24"


__all__ = [
    "ENGLISH_PROMPT_VERSION",
    "JobAnalysisServiceV24",
    "_ENGLISH_SYSTEM_PROMPT_V24",
    "_V24_RULES",
]
