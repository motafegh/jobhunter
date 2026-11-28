"""Combined A1 research adapter and private candidate envelope.

Only the fixed offline worker uses this adapter. No production registration,
V5 artifact, semantic acceptance or live transport.
"""

from __future__ import annotations

from dataclasses import asdict
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import httpx

from jobhunter import analysis_persistence_v23 as persistence
from jobhunter import analysis_runtime_v20 as runtime20
from jobhunter.analysis_runtime_v23 import _filter_unassigned_partition_claims
from jobhunter.analysis_runtime_v30 import V30CandidateAnalysisProvider
from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.analysis_service_v16 import validate_v16_candidate_structured
from jobhunter.analysis_service_v17 import _validate_evidence_v17
from jobhunter.analysis_service_v30 import JobAnalysisServiceV30
from jobhunter.evidence_refs_v28 import persisted_qualification_plan_v28
from jobhunter.inference import instructor_lm_studio_v20 as sdk20
from jobhunter.inference.instructor_lm_studio_v24 import (
    complete_analysis_partition_with_instructor_v24,
)
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.p16_lab import OfflineGuard, OfflineRun, canonical, digest, publish_new
from jobhunter.p16_lab_a1_r4 import separate_board_skills, verify_board_observations
from jobhunter.p16_lab_a1_r23 import JobAnalysisResponseR12, corrected_duty_plan
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion

CONTRACT = "p16-e3-candidate-envelope-v1"
ADAPTER = "p16-e3-a1-repair-v1"


# Replace the directly conflicting incumbent clauses, not its whole prompt.
def _a1_prompt():
    prompt = JobAnalysisServiceV30.system_prompt
    replacements = (
        (
            "- The top-level skills array is an explicit structured job requirement "
            "surface. Every non-empty\n"
            "  skills item MUST be represented by a requirement that cites that exact "
            "skills item as evidence.\n"
            "  Do not omit a structured skill merely because related wording also "
            "appears in description text.\n"
            "- Preserve structured skills as required unless the exact structured skill "
            "evidence itself states\n"
            "  otherwise. Do not weaken them to contextual just because a nearby prose "
            "sentence is ambiguous.",
            "- Board skill tags are recorded separately as observations, not employer obligations.",
        ),
        (
            "- Keep concept depth-neutral: it identifies what skill, tool, knowledge, "
            "experience, education,\n"
            "  or practice is requested, without "
            "expert/proficient/familiar/strong/solid/hands-on/comfort or\n"
            "  years wording.",
            "- Keep technical concepts depth-neutral. Retain explicit motivation wording "
            "as meaning, not degree.",
        ),
        (
            "- item_excerpt is candidate validation evidence. JobHunter removes it "
            "before unchanged v5\n"
            "  persistence; parent evidence and exact depth_signal remain the durable "
            "factual representation.",
            "- Keep item_excerpt and its exact parent in the private research candidate.",
        ),
        (
            "- Decide depth_signal only from item_excerpt. Supply the exact applicable "
            "marker when the item has\n"
            "  one. Use null when this exact item has no accepted depth marker, even if "
            "neighboring items in the\n"
            "  parent have markers. Never borrow neighboring depth.",
            "- Decide technical depth from item_excerpt. Preserve the complete "
            "applicable degree phrase.\n"
            "  A motivational adjective is not a technical degree. Never borrow neighboring depth.",
        ),
        (
            "- Keep depth wording out of concept. If the exact item starts with one "
            "source marker, JobHunter may\n"
            "  materialize that one marker into depth_signal even when the generated "
            "concept uses wording such\n"
            '  as "Working with X". If the concept itself starts with the same generated '
            "wrapper, JobHunter may\n"
            "  also remove that wrapper and retain X as the concept.",
            "- Separate explicit technical degree from its subject, not words expressing "
            "motivation.",
        ),
        (
            "- JobHunter owns top-level structured skill tags and adds their exact "
            "source facts after\n"
            "  generation. They are absent from model-facing evidence and coverage. Do "
            "not reconstruct,\n"
            "  classify, or cite absent structured skill tags. Extract description "
            "requirements only\n"
            "  from the supplied coverage, even when they also mention a structured skill.",
            "- Board tags are absent from model-facing evidence and coverage. Do not "
            "reconstruct them.\n"
            "  Interpret actual description requirements from supplied evidence.",
        ),
    )
    for old, new in replacements:
        if prompt.count(old) != 1:
            raise ValueError("A1 prompt replacement no longer unique")
        prompt = prompt.replace(old, new)
    return (
        prompt
        + """

A1 EXPERIMENTAL SCOPE:
Keep distinct subjects and complete degree scopes; preserve OR alternatives.
Explicit motivation or interest is not technical proficiency or prior work.
Retain its meaning and use null technical depth if no technical degree is stated.
The supplied duty ledger excludes proven duplicate qualification headings.
All other source, coverage and obligation guards remain in force.
"""
    )


PROMPT = _a1_prompt()


class A1Provider(V30CandidateAnalysisProvider):
    """Inherit the actual planner/retry chain; replace only selected seams."""

    def __init__(self, guard: OfflineGuard):
        if type(guard) is not OfflineGuard or type(guard.inner) is not httpx.MockTransport:
            raise TypeError("A1 requires the offline mock guard")
        self.guard = guard
        self.partition_requirements: list[dict] = []
        self.duty_plans: list[dict[str, str]] = []
        self.removed_duty_refs: list[tuple[str, ...]] = []
        super().__init__(
            base_url="http://127.0.0.1:18080/v1",
            configured_model=guard.run.models["M0"],
            api_token=None,
            timeout_seconds=30,
            max_retries=0,
        )

    def _run_once(self, **kwargs):
        # Each inherited V15/V16 correction starts a new whole attempt.
        # Only its final successfully returned partitions can feed the candidate.
        self.partition_requirements.clear()
        return super()._run_once(**kwargs)

    def _responsibility_coverage_plan(self, model_fields):
        plan, removed = corrected_duty_plan(model_fields)
        self.duty_plans.append(plan)
        self.removed_duty_refs.append(removed)
        return plan

    def _persistable_structured(self, structured):
        return structured  # keep normalized item_excerpt, no V5 conversion

    def _complete_partition(self, **kwargs: Any):
        refs = list(kwargs["requirement_coverage_plan"])
        refs.extend(kwargs["responsibility_coverage_plan"])
        result = complete_analysis_partition_with_instructor_v24(
            **kwargs,
            contract_version=ADAPTER,
            model_evidence_references=refs,
            response_model=JobAnalysisResponseR12,
        )
        result = _filter_unassigned_partition_claims(
            result,
            requirement_plan=kwargs["requirement_coverage_plan"],
            responsibility_plan=kwargs["responsibility_coverage_plan"],
        )
        self.partition_requirements.extend(dict(c) for c in result.structured["requirements"])
        return result

    def complete_structured(self, **kwargs):
        # The shared SDK exposes no transport parameter. This process-local
        # substitution is restricted to the fixed single-threaded worker.
        run = self.guard.run
        run.check_time()
        if not run.diagnostic_only or run.cell is None:
            run.stop("a1_offline_cell_required")
        if kwargs.get("model") != self._configured_model:
            run.stop("a1_model_mismatch")
        if "skills" in kwargs["user_payload"]["analysis_fields"]:
            run.stop("a1_board_separation_required")

        def control(**kw):
            return ensure_lm_studio_model_context(**kw, transport=self.guard)

        def client(**kw):
            if kw.get("trust_env") is not False:
                run.stop("a1_unexpected_client_configuration")
            return httpx.Client(**kw, transport=self.guard, follow_redirects=False)

        with (
            patch.object(runtime20, "ensure_lm_studio_model_context", control),
            patch.object(sdk20, "httpx", SimpleNamespace(Client=client, Timeout=httpx.Timeout)),
        ):
            return super().complete_structured(**kwargs)


def verify_scoped_merge(partition_claims: list[dict], final_claims: list[dict]) -> None:
    """No model-owned scoped claim may disappear or lose its child/degree in merge."""

    def identity(c):
        return tuple(
            c.get(k)
            for k in (
                "concept",
                "requirement_type",
                "concept_type",
                "evidence",
                "item_excerpt",
                "depth_signal",
            )
        )

    if any(
        not isinstance(c.get("item_excerpt"), str)
        or not c["item_excerpt"]
        or c["item_excerpt"] not in c["evidence"]
        for c in partition_claims
    ):
        raise ValueError("partition scope missing")
    expected = {identity(c) for c in partition_claims}
    observed = {identity(c) for c in final_claims if "item_excerpt" in c}
    if expected != observed:
        raise ValueError("scoped merge changed model claims")


def reconcile(structured: dict, fields: dict, provider: A1Provider) -> dict:
    """Reuse incumbent ledger checks with exactly the corrected duty plan.

    The scoped substitution is for the offline child only. The corrected plan
    must match the actual generation ledger, not merely the output claims.
    """
    if "skills" in fields:
        raise ValueError("board fields not separated")
    duty, removed = corrected_duty_plan(fields)
    if not provider.duty_plans or any(p != duty for p in provider.duty_plans):
        raise ValueError("generation/persistence duty ledger mismatch")
    if any(r != removed for r in provider.removed_duty_refs):
        raise ValueError("generation/persistence removed duty mismatch")
    validate_v16_candidate_structured(structured, fields)
    verify_scoped_merge(provider.partition_requirements, structured["requirements"])
    for claim in structured["requirements"]:
        if "item_excerpt" in claim and (
            not claim["item_excerpt"] or claim["item_excerpt"] not in claim["evidence"]
        ):
            raise ValueError("candidate lost exact child scope")
    with patch.object(persistence, "build_responsibility_coverage_plan_v21", lambda _: duty):
        analysis = persistence.persisted_analysis_v23(
            structured, fields, requirement_plan=persisted_qualification_plan_v28(fields)
        )
    _validate_evidence_v17(analysis, fields)
    return {"analysis": analysis, "removed_duty_refs": list(removed)}


def execute_a1(
    run: OfflineRun,
    guard: OfflineGuard,
    source: TranslationSourceVersion,
    translation: TranslationArtifact,
) -> dict:
    """Private candidate service; bind source and projection, never write V5."""
    if (
        guard.run is not run
        or translation.source_job_id != source.source_job_id
        or translation.job_detail_version_id != source.job_detail_version_id
        or translation.source_semantic_sha256 != source.semantic_sha256
        or translation.target_language != "en"
        or translation.translation_schema_version != "english-projection-v2"
    ):
        raise ValueError("A1 projection association mismatch")
    fields, board = separate_board_skills(source, _analysis_fields_for_english(translation.fields))
    observations = [asdict(b) for b in board]
    verify_board_observations(source, observations)
    provider = A1Provider(guard)
    result = provider.complete_structured(
        model=run.models["M0"],
        system_prompt=PROMPT,
        user_payload={"analysis_mode": "english", "analysis_fields": fields},
        max_tokens=8192,
        seed=17,
    )
    reconciled = reconcile(result.structured, fields, provider)
    run.check_time()
    envelope = {
        "contract_version": CONTRACT,
        "adapter": ADAPTER,
        "authority": "candidate_only",
        "semantic_review_status": "pending",
        "execution_scope": "offline_rehearsal_only",
        "actual_experiment_cell": False,
        "source": {
            "source_job_id": source.source_job_id,
            "job_detail_version_id": source.job_detail_version_id,
            "semantic_sha256": source.semantic_sha256,
            "fields_sha256": digest(canonical(source.fields)),
        },
        "projection": {
            "artifact_id": translation.id,
            "translation_sha256": translation.translation_sha256,
            "model": translation.provider_model,
            "analysis_fields_sha256": digest(canonical(fields)),
        },
        "model": result.model,
        "prompt_sha256": digest(PROMPT.encode()),
        "execution_identity": run.execution,
        "board_observations": observations,
        "normalized": result.structured,
        "raw_response": result.raw_response,
        "request_body": result.request_body,
        **reconciled,
    }
    data = canonical(envelope)
    publish_new(run.path / "a1-candidate.json", data)
    summary = {
        "candidate_sha256": digest(data),
        "requirements": len(result.structured["requirements"]),
        "scoped_requirements": sum("item_excerpt" in c for c in result.structured["requirements"]),
        "board_observations": len(observations),
        "removed_duty_refs": len(reconciled["removed_duty_refs"]),
        "authority": "candidate_only",
        "semantic_review_status": "pending",
    }
    run.event("a1_candidate_published", **summary)
    return summary


# Fixed synthetic positive: the real provider should exercise R1, R3 and R4.
COMPOUND = "Strong proficiency in Rust or Kotlin, with a solid understanding of distributed design."
DESCRIPTION = "Responsibilities: Deploy services. Skills: " + COMPOUND


def synthetic_input(*, motivation=False):
    description = (
        "Qualifications: Strong interest in hands-on robotics development."
        if motivation
        else DESCRIPTION
    )
    fields = {"title": "Synthetic", "description": description, "skills": ["Go"]}
    source = TranslationSourceVersion("synthetic-a1", 1, digest(canonical(fields)), "en", fields)
    projection = TranslationArtifact(
        1,
        source.source_job_id,
        1,
        source.semantic_sha256,
        "en",
        "en",
        "synthetic",
        "synthetic",
        "english-projection-v2",
        dict(fields),
        description,
        {},
        0,
        1,
        digest(canonical(fields)),
        "synthetic",
    )
    return source, projection


def synthetic_reply(*, motivation=False):
    if motivation:
        meaning = "Strong interest in hands-on robotics development"
        return {
            "role_purpose": [],
            "responsibilities": [],
            "coverage_exclusions": [],
            "requirements": [
                {
                    "concept": meaning,
                    "depth_signal": "strong interest",
                    "requirement_type": "required",
                    "concept_type": "other",
                    "evidence": "field:description:segment:0",
                    "confidence": "high",
                    "rationale": "Explicit motivation.",
                    "item_excerpt": meaning + ".",
                }
            ],
        }

    def claim(concept, degree):
        return {
            "concept": concept,
            "depth_signal": degree,
            "requirement_type": "required",
            "concept_type": "skill",
            "evidence": "field:description:segment:1",
            "confidence": "high",
            "rationale": "Explicit source qualification.",
            "item_excerpt": COMPOUND,
        }

    return {
        "role_purpose": [],
        "responsibilities": [
            {
                "statement": "Deploy services",
                "evidence": "field:description:segment:0:item:0",
                "confidence": "high",
            }
        ],
        "requirements": [
            claim("Rust or Kotlin", "Strong proficiency"),
            claim("distributed design", "solid understanding"),
        ],
        "coverage_exclusions": [],
    }
