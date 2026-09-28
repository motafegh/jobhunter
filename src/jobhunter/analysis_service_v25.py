"""Isolated P1.6 v25 candidate with source-grouped evidence partitions."""

from jobhunter.analysis_service_v24 import (
    _ENGLISH_SYSTEM_PROMPT_V24,
    JobAnalysisServiceV24,
)

ENGLISH_PROMPT_VERSION = "job-analysis-english-v25"

_V25_RULES = """

P1.6 V25 SOURCE-GROUPED PARTITIONS:
- Adjacent exact sentences from the same source paragraph are supplied together.
- This call may cite only the evidence references supplied in its evidence_references.
- Account for every assigned requirement_coverage reference once, by a grounded
  claim or a justified exclusion when exclusion is allowed.
- Explicit preferred prior-work sentences carried as exact source quotations
  are outside this call's ledger. Do not invent candidate history or re-extract
  them from another reference.
"""


class JobAnalysisServiceV25(JobAnalysisServiceV24):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = _ENGLISH_SYSTEM_PROMPT_V24 + _V25_RULES
    schema_name = "jobhunter_job_analysis_english_v25"


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV25"]
