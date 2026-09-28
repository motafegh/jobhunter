"""Isolated v26 candidate for exact mixed-strength and contextual source facts."""

from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_service_v25 import JobAnalysisServiceV25
from jobhunter.evidence_refs_v26 import persisted_qualification_plan_v26

ENGLISH_PROMPT_VERSION = "job-analysis-english-v26"

_V26_RULES = """

P1.6 V26 SOURCE CLAUSE OWNERSHIP:
- Exact source clauses with an explicit 'preferably' transition have separate
  required and preferred owners. Preserve alternatives within each clause.
- Negative candidate-suitability and compensation context is retained in
  source coverage, outside positive qualification extraction.
- Do not turn a negative insufficiency statement into a positive requirement.
"""


class JobAnalysisServiceV26(JobAnalysisServiceV25):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV25.system_prompt + _V26_RULES
    schema_name = "jobhunter_job_analysis_english_v26"

    def _persist_analysis(self, structured: dict, analysis_fields: dict) -> dict:
        return persisted_analysis_v23(
            structured,
            analysis_fields,
            requirement_plan=persisted_qualification_plan_v26(analysis_fields),
        )


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV26"]
