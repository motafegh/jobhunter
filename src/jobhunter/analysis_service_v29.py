"""Isolated v29 candidate with explicit mixed source ontology."""

from jobhunter.analysis_service_v28 import JobAnalysisServiceV28

ENGLISH_PROMPT_VERSION = "job-analysis-english-v29"

_V29_RULES = """

P1.6 V29 MIXED SOURCE ONTOLOGY:
- If one exact source item explicitly states both knowledge and practical
  experience, or both education and practical experience, retain the whole
  source fact but abstain from classifying it as only one of those categories.
- An exact phrase 'knowledge of X' is knowledge, even when X names a tool or
  programming language. Do not turn it into prior experience or tool use.
"""


class JobAnalysisServiceV29(JobAnalysisServiceV28):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV28.system_prompt + _V29_RULES
    schema_name = "jobhunter_job_analysis_english_v29"


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV29"]
