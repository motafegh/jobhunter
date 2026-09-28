"""Isolated v28 candidate with source-exact dense item ownership."""

from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_service_v27 import JobAnalysisServiceV27
from jobhunter.evidence_refs_v28 import persisted_qualification_plan_v28

ENGLISH_PROMPT_VERSION = "job-analysis-english-v28"

_V28_RULES = """

P1.6 V28 DENSE SOURCE ITEMS:
- A required residual may provide multiple exact qualification item excerpts.
  Account for each supplied exact item; one citation to the broad parent is
  not sufficient for the complete list.
- Short explicit candidate-trait lists carried as exact source quotations are
  not model-owned. Never attach an unrelated technical skill to trait evidence.
"""


class JobAnalysisServiceV28(JobAnalysisServiceV27):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV27.system_prompt + _V28_RULES
    schema_name = "jobhunter_job_analysis_english_v28"

    def _persist_analysis(self, structured: dict, analysis_fields: dict) -> dict:
        return persisted_analysis_v23(
            structured,
            analysis_fields,
            requirement_plan=persisted_qualification_plan_v28(analysis_fields),
        )


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV28"]
