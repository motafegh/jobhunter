"""Isolated v27 candidate with required residual and qualified-depth ownership."""

from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_service_v26 import JobAnalysisServiceV26
from jobhunter.evidence_refs_v27 import persisted_qualification_plan_v27

ENGLISH_PROMPT_VERSION = "job-analysis-english-v27"

_V27_RULES = """

P1.6 V27 REQUIRED RESIDUAL AND EXACT DEPTH:
- A residual span from an explicitly required qualification paragraph remains
  required even when exact first items decomposed the broad parent reference.
- Do not exclude that residual merely because the broad parent was removed.
- Preserve the complete exact source degree, including qualifiers such as
  relative mastery or initial familiarity, for the item it modifies.
- Explicit 'experience working with' describes prior applied exposure, not
  merely the named tool.
"""


class JobAnalysisServiceV27(JobAnalysisServiceV26):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV26.system_prompt + _V27_RULES
    schema_name = "jobhunter_job_analysis_english_v27"

    def _persist_analysis(self, structured: dict, analysis_fields: dict) -> dict:
        return persisted_analysis_v23(
            structured,
            analysis_fields,
            requirement_plan=persisted_qualification_plan_v27(analysis_fields),
        )


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV27"]
