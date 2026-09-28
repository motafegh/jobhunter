"""Isolated v30 candidate preserving exact prior applied exposure."""

from jobhunter.analysis_service_v29 import JobAnalysisServiceV29

ENGLISH_PROMPT_VERSION = "job-analysis-english-v30"

_V30_RULES = """

P1.6 V30 EXPLICIT PRIOR EXPERIENCE:
- An exact source item saying practical or professional experience in
  designing, developing, or working with something requests prior applied
  exposure. Do not relabel it as only a skill or the named tool.
- Keep source-exact evidence, obligation, depth, and mixed-category abstention.
"""


class JobAnalysisServiceV30(JobAnalysisServiceV29):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV29.system_prompt + _V30_RULES
    schema_name = "jobhunter_job_analysis_english_v30"


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV30"]
