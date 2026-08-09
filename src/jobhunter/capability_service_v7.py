"""Capability v7 service: complete source truth plus bounded semantic reasoning."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.capability_inference import CapabilityInferenceProvider
from jobhunter.capability_service_v6 import (
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
    _evidence_catalog,
    _result,
)
from jobhunter.capability_service_v6 import (
    CapabilityIntelligenceService as _V6CapabilityIntelligenceService,
)
from jobhunter.capability_store import CapabilityIntelligenceStore
from jobhunter.capability_v7_models import (
    CapabilityReasoningDraft,
    partition_source_requirements,
    reconcile_capability_intelligence,
)
from jobhunter.config import Settings
from jobhunter.evidence_refs import evidence_reference_payload
from jobhunter.translation_store import TranslationStore

CAPABILITY_PROMPT_VERSION = "job-capability-intelligence-v7"
CAPABILITY_SCHEMA_VERSION = "job-capability-intelligence-v4"

_SYSTEM_PROMPT = """You are JobHunter's capability-reasoning engine.

BOUNDARY
Accepted P1.6 already contains the employer's factual requirements, responsibilities, role purpose,
strength, explicit depth, and exact evidence. JobHunter—not you—owns preservation of those facts.
Your job is semantic grouping and useful derived reasoning above that substrate.

SOURCE COVERAGE V7
The request contains source_partition:
- capability_requirement_indices: every accepted requirement that belongs in capability grouping;
- role_level_requirement_indices: education / standalone experience-duration constraints retained
  separately by JobHunter;
- responsibility_indices: every accepted responsibility.

Every capability_requirement_indices item MUST appear in at least one capability profile's
source_requirement_indices.
Every responsibility_indices item MUST appear in at least one profile's
source_responsibility_indices.
Do not attach facts to unrelated profiles merely to satisfy coverage. Instead create enough
coherent profiles to cover the job truthfully. Dense jobs must not collapse into one catch-all
technical-stack capability.

MODEL OUTPUT VS JOBHUNTER OUTPUT
For every profile:
- emit requirement_strength = "unspecified"; JobHunter derives it from linked P1.6 strengths;
- do not emit source-explicit depth; JobHunter inserts it from linked P1.6 depth_signal values;
- do not restate source responsibilities as source-explicit work activities; JobHunter inserts
  those deterministically;
- independence_expectation MUST be null in v7;
- cross_capability_observations MUST be [] in v7.

Use the model primarily for:
- coherent capability grouping;
- strongly implied technical sub-capabilities;
- defensible prerequisites;
- operational practices/context that genuinely follow from supported work;
- useful unknown-scope boundaries;
- derived depth only when work evidence supports it.

GROUNDING
Use only identifiers from evidence_reference_ids inside evidence[]. JobHunter resolves them to exact
source text. Prefer P1.6 references for claims grounded in accepted facts. Evidence must directly
support the subject of the analytical statement.

CALIBRATION
- Required/preferred/contextual/inferred strength comes from P1.6; preserve it in prose.
- Contextual or preferred tools are not automatically mandatory, necessary, mastery-level, or
  gatekeepers.
- A technology list is not an architecture specification.
- Build/pipeline/MLOps/production/partner/collaborate language does not establish end-to-end
  ownership, autonomy, leadership, or decision authority.
- Do not use cloud evidence for database claims, orchestration evidence for domain expertise, or
  one technology family to prove another.
- Do not expand the posting into a generic curriculum.
- Sparse evidence should produce modest conclusions and more unknowns; rich evidence may support
  deeper decomposition.

EVIDENCE STATUS
Use exactly one:
- source_explicit
- strongly_implied_by_work
- model_inferred_prerequisite
- unknown_or_unsupported

In v7, source_explicit is effectively reserved for JobHunter's deterministic reconciliation.
Your analytical additions should normally be strongly_implied_by_work,
model_inferred_prerequisite, or unknown_or_unsupported.

PERSONAL BOUNDARY
Describe the job only. Do not assess the candidate, readiness, fit, or learning plan.
"""


class CapabilityIntelligenceService(_V6CapabilityIntelligenceService):
    """Persist Capability v7 while keeping the accepted P1.6 dependency fixed."""

    def analyze_job(self, source_job_id: str) -> CapabilityIntelligenceResult:
        source, translation, analysis = self._current_dependencies(source_job_id)
        attempted_at = self._clock()

        existing = self._capability_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if existing is not None:
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="reused",
                artifact_id=existing.id,
            )
            return _result(existing, outcome="reused")

        analysis_fields = self._analysis_fields(translation.fields)
        evidence_catalog = _evidence_catalog(analysis_fields, analysis.analysis)
        capability_requirements, role_level_requirements = partition_source_requirements(
            analysis.analysis
        )
        responsibilities = analysis.analysis.get("responsibilities") or []
        if not isinstance(responsibilities, list):
            raise CapabilityIntelligenceError(
                "Accepted English P1.6 responsibilities are not a list"
            )

        user_payload = {
            "source_job_id": source.source_job_id,
            "analysis_fields": analysis_fields,
            "accepted_extraction": analysis.analysis,
            "source_partition": {
                "capability_requirement_indices": capability_requirements,
                "role_level_requirement_indices": role_level_requirements,
                "responsibility_indices": list(range(len(responsibilities))),
            },
            "evidence_reference_ids": sorted(evidence_catalog),
            "evidence_references": evidence_reference_payload(evidence_catalog),
            "contract": {
                "prompt_version": CAPABILITY_PROMPT_VERSION,
                "schema_version": CAPABILITY_SCHEMA_VERSION,
                "analysis_artifact_id": analysis.id,
                "translation_artifact_id": translation.id,
                "deterministic_reconciliation": {
                    "requirement_strength": "from linked accepted P1.6 requirement types",
                    "source_explicit_depth": "from linked accepted P1.6 depth_signal values",
                },
                "v7_source_truth": {
                    "source_truth": "complete accepted P1.6 substrate and coverage",
                    "source_work_activities": (
                        "from linked accepted P1.6 responsibilities"
                    ),
                    "independence": "deferred; not positively inferred in Capability v7",
                    "cross_capability_synthesis": "deferred in Capability v7",
                },
            },
        }
        validation_context = {
            "analysis_fields": analysis_fields,
            "evidence_catalog": evidence_catalog,
            "accepted_extraction": analysis.analysis,
        }

        try:
            inference = self._provider.complete(
                system_prompt=_SYSTEM_PROMPT,
                user_payload=user_payload,
                evidence_catalog=evidence_catalog,
                max_tokens=self._max_tokens,
            )
            model_validated = CapabilityReasoningDraft.model_validate(
                inference.intelligence,
                context=validation_context,
            )
            reconciled = reconcile_capability_intelligence(
                model_validated,
                accepted_extraction=analysis.analysis,
                analysis_fields=analysis_fields,
                evidence_catalog=evidence_catalog,
            )
            intelligence = reconciled.model_dump(mode="json")
            artifact_id = self._capability_store.record_artifact(
                job_detail_version_id=source.job_detail_version_id,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=inference.model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                intelligence=intelligence,
                request_body=inference.request_body,
                raw_response=inference.raw_response,
                created_at=attempted_at,
            )
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="completed",
                artifact_id=artifact_id,
            )
        except Exception as exc:
            self._capability_store.record_attempt(
                job_detail_version_id=source.job_detail_version_id,
                attempted_at=attempted_at,
                translation_artifact_id=translation.id,
                analysis_artifact_id=analysis.id,
                model=self._capability_model,
                prompt_version=CAPABILITY_PROMPT_VERSION,
                schema_version=CAPABILITY_SCHEMA_VERSION,
                outcome="failed",
                error=exc,
            )
            raise

        artifact = self._capability_store.find_artifact(
            job_detail_version_id=source.job_detail_version_id,
            translation_artifact_id=translation.id,
            analysis_artifact_id=analysis.id,
            model=self._capability_model,
            prompt_version=CAPABILITY_PROMPT_VERSION,
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        if artifact is None:
            raise RuntimeError("Capability-intelligence artifact disappeared after persistence")
        return _result(artifact, outcome="completed")


def build_capability_intelligence_service(settings: Settings) -> CapabilityIntelligenceService:
    """Build the v7 local capability-intelligence dependency graph."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for the accepted English extraction")
    capability_model = settings.effective_capability_lm_studio_model()
    if not capability_model:
        raise ValueError("No LM Studio capability-intelligence model is configured")
    translation_store = TranslationStore(settings.database_path)
    return CapabilityIntelligenceService(
        source_store=translation_store,
        analysis_store=AnalysisStore(settings.database_path),
        capability_store=CapabilityIntelligenceStore(settings.database_path),
        provider=CapabilityInferenceProvider(
            base_url=settings.lm_studio_base_url,
            configured_model=capability_model,
            api_token=settings.lm_studio_api_token,
            timeout_seconds=settings.inference_timeout_seconds,
            network_retries=settings.inference_max_retries,
            validation_retries=1,
        ),
        analysis_model=analysis_model,
        capability_model=capability_model,
        max_tokens=settings.analysis_max_tokens,
    )


def format_capability_intelligence(artifact: Any) -> str:
    """Readable CLI surface exposing both deterministic source truth and semantic profiles."""

    data = artifact.intelligence
    lines = [
        f"Capability intelligence for {artifact.source_job_id}",
        f"Model: {artifact.model}",
        f"Contract: {artifact.prompt_version} / {artifact.schema_version}",
        f"English analysis artifact: {artifact.analysis_artifact_id}",
    ]

    source_truth = data.get("source_truth") or {}
    if source_truth:
        capability_requirements = source_truth.get("capability_requirement_indices") or []
        linked_requirements = source_truth.get("linked_requirement_indices") or []
        responsibilities = source_truth.get("responsibilities") or []
        linked_responsibilities = source_truth.get("linked_responsibility_indices") or []
        depth = source_truth.get("explicit_depth_requirement_indices") or []
        linked_depth = source_truth.get("linked_explicit_depth_requirement_indices") or []
        role_level = source_truth.get("role_level_requirement_indices") or []
        lines.extend(
            [
                "",
                "Deterministic P1.6 source truth",
                (
                    "Capability requirements linked: "
                    f"{len(linked_requirements)}/{len(capability_requirements)}"
                ),
                (
                    "Responsibilities linked: "
                    f"{len(linked_responsibilities)}/{len(responsibilities)}"
                ),
                f"Explicit depth represented in profiles: {len(linked_depth)}/{len(depth)}",
                f"Role-level requirement indices: {role_level}",
            ]
        )

    lines.extend(["", "Role interpretation", str(data.get("role_interpretation") or "(none)")])
    for index, profile in enumerate(data.get("capabilities") or [], start=1):
        requirement_links = profile.get("source_requirement_indices") or []
        responsibility_links = profile.get("source_responsibility_indices") or []
        lines.extend(
            [
                "",
                f"Capability {index}: {profile.get('capability_label', '(unnamed)')}",
                f"Strength: {profile.get('requirement_strength', 'unspecified')}",
                f"Confidence: {profile.get('overall_confidence', 'unknown')}",
                (
                    "P1.6 links: requirements="
                    f"{requirement_links or '[]'} responsibilities={responsibility_links or '[]'}"
                ),
                str(profile.get("summary") or ""),
            ]
        )
        for section_name, label in (
            ("depth_signals", "Depth signals"),
            ("work_activities", "Work activities"),
            ("sub_capabilities", "Sub-capabilities"),
            ("underlying_knowledge", "Underlying knowledge"),
            ("operational_practices", "Operational practices"),
            ("operational_context", "Operational context"),
            ("unknown_scope", "Unknown / unsupported scope"),
        ):
            items = profile.get(section_name) or []
            if not items:
                continue
            lines.append(f"  {label}:")
            for item in items:
                lines.append(
                    "  - "
                    f"[{item.get('evidence_status', '?')}; {item.get('confidence', '?')}] "
                    f"{item.get('statement', '')}"
                )
                if item.get("rationale"):
                    lines.append(f"    Why: {item['rationale']}")

    uncertainties = data.get("uncertainties") or []
    if uncertainties:
        lines.extend(["", "Uncertainties"])
        lines.extend(f"- {item}" for item in uncertainties)
    return "\n".join(lines)


__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceError",
    "CapabilityIntelligenceResult",
    "CapabilityIntelligenceService",
    "build_capability_intelligence_service",
    "format_capability_intelligence",
]
