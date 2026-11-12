"""Isolated candidate for source-section fidelity; no public routing or promotion."""
from __future__ import annotations

from jobhunter.analysis_persistence_v23 import persisted_analysis_v23
from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
from jobhunter.evidence_refs_v28 import persisted_qualification_plan_v28
from jobhunter.evidence_refs_v31 import v31_requirement_plan

ENGLISH_PROMPT_VERSION = "job-analysis-english-v31"

_V31_RULES = """
P1.6 V31 SOURCE-SECTION FIDELITY:
- Preserve exact section ownership supplied by source-scoped coverage references.
  Distinguish explicit job duties, required qualifications, preferred conditions,
  alternative Middle/Senior eligibility tracks, arrangements and application text.
- A role headline never establishes a technical qualification not stated in the
  description. A GitHub/portfolio invitation is not automatically a skill.
- When Middle and Senior eligibility are stated as alternatives, never require
  the applicant to meet BOTH. Preserve both pathways and their explicit bounds.
  A higher experience tier is not a source-wide minimum.
- Employer tools named as examples are not individually mandatory.
- A source heading marked preferred supplies conditional strength only for the
  exact evidence span it owns; a nearby unrelated required item is not preferred.
- Preserve source-explicit EDR and other technical support actions as duties
  rather than dropping an information-rich description. Evidence must remain
  exact and never be invented from the job title.
- A logistical possibility such as remote work is not a required applicant
  qualification. If source sections are ambiguous, explicitly omit or abstain.
"""


class JobAnalysisServiceV31(JobAnalysisServiceV30):
    prompt_version = ENGLISH_PROMPT_VERSION
    system_prompt = JobAnalysisServiceV30.system_prompt + _V31_RULES
    schema_name = "jobhunter_job_analysis_english_v31"

    def _persist_analysis(self, structured: dict, analysis_fields: dict) -> dict:
        return persisted_analysis_v23(
            structured,
            analysis_fields,
            requirement_plan=v31_requirement_plan(
                analysis_fields, persisted_qualification_plan_v28(analysis_fields)
            ),
        )


__all__ = ["ENGLISH_PROMPT_VERSION", "JobAnalysisServiceV31"]
