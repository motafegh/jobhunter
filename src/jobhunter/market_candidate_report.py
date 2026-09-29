"""Bounded, ephemeral Market work and role-subfamily interpretation."""

from __future__ import annotations

from typing import Any

from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import LMStudioProvider
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore

REPORT_CONTRACT = "market-role-family-candidate-v1"
PROMPT_VERSION = "market-role-family-candidate-prompt-v1"


def _response_schema(citation_ids: list[str]) -> dict[str, Any]:
    item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "label",
            "summary",
            "why_grouped",
            "evidence_refs",
            "confidence",
            "alternatives",
        ],
        "properties": {
            "label": {"type": "string", "minLength": 1, "maxLength": 120},
            "summary": {"type": "string", "minLength": 1, "maxLength": 600},
            "why_grouped": {"type": "string", "minLength": 1, "maxLength": 600},
            "evidence_refs": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string", "enum": citation_ids},
            },
            "confidence": {"type": "string", "enum": ["low", "moderate", "high"]},
            "alternatives": {
                "type": "array",
                "items": {"type": "string", "maxLength": 240},
                "maxItems": 4,
            },
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "overall_reading",
            "overall_evidence_refs",
            "work_clusters",
            "possible_role_subfamilies",
            "limitations",
        ],
        "properties": {
            "overall_reading": {"type": "string", "minLength": 1, "maxLength": 1000},
            "overall_evidence_refs": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string", "enum": citation_ids},
            },
            "work_clusters": {"type": "array", "items": item, "maxItems": 12},
            "possible_role_subfamilies": {"type": "array", "items": item, "maxItems": 8},
            "limitations": {
                "type": "array",
                "items": {"type": "string", "maxLength": 300},
                "maxItems": 8,
            },
        },
    }


def build_market_candidate_report(
    settings: Settings,
    snapshot_id: int,
    *,
    model_override: str | None = None,
) -> dict[str, Any]:
    """Interpret accepted exact P1.6 from one immutable snapshot without persisting it."""
    market = MarketStore(settings.database_path)
    snapshot = market.get_snapshot(snapshot_id)
    if snapshot is None:
        raise LookupError(f"Unknown Market snapshot {snapshot_id}")

    analysis_store = AnalysisStore(settings.database_path)
    job_store = JobHunterStore(settings.database_path)
    evidence: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    for member in market.list_snapshot_members(snapshot_id):
        if not member.included_in_primary_corpus or member.semantic_coverage_status != "accepted":
            continue
        if member.analysis_artifact_id is None:
            continue
        artifact = analysis_store.artifact_by_id(member.analysis_artifact_id)
        if artifact is None:
            raise ValueError(
                f"Snapshot references missing P1.6 artifact {member.analysis_artifact_id}"
            )
        if (
            artifact.semantic_review_status != "accepted"
            or artifact.source_job_id != member.source_job_id
            or artifact.job_detail_version_id != member.job_detail_version_id
            or artifact.translation_artifact_id != member.translation_artifact_id
        ):
            raise ValueError(f"Snapshot P1.6 identity mismatch for {member.source_job_id}")
        job = job_store.get_job(member.source_job_id)
        source = {
            "source_job_id": member.source_job_id,
            "title": job.title_observed if job else None,
            "job_url": job.canonical_url if job else None,
            "job_detail_version_id": member.job_detail_version_id,
            "translation_artifact_id": member.translation_artifact_id,
            "analysis_artifact_id": artifact.id,
            "analysis_prompt_version": artifact.prompt_version,
            "analysis_schema_version": artifact.schema_version,
        }
        sources[member.source_job_id] = source
        for kind, key, prefix in (
            ("responsibility", "responsibilities", "W"),
            ("requirement", "requirements", "Q"),
        ):
            for index, claim in enumerate(artifact.analysis.get(key, [])):
                ref = f"{prefix}:{member.source_job_id}:{index}"
                evidence[ref] = {
                    "ref": ref,
                    "kind": kind,
                    "source_job_id": member.source_job_id,
                    "analysis_artifact_id": artifact.id,
                    "statement": claim.get("statement") or claim.get("concept"),
                    "source_excerpt": claim.get("evidence"),
                    "requirement_type": claim.get("requirement_type"),
                    "confidence": claim.get("confidence"),
                }

    work_refs = [key for key, value in evidence.items() if value["kind"] == "responsibility"]
    if not evidence:
        raise ValueError("Snapshot has no accepted-core P1.6 claims for interpretation")
    model = model_override or settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No analysis model is configured")

    provider = LMStudioProvider(
        base_url=settings.lm_studio_base_url,
        configured_model=model,
        api_token=settings.lm_studio_api_token,
        timeout_seconds=settings.inference_timeout_seconds,
        max_retries=0,
    )
    result = provider.complete_structured(
        system_prompt=(
            "You are producing a bounded interpretation of one small, frozen job-market sample. "
            "Group related work and suggest possible role subfamilies only where cited claims "
            "support it. These are hypotheses, not employer facts or promoted taxonomy. Use "
            "responsibilities as primary support; requirements may explain differences. Jobs may "
            "support multiple groups or none. Do not invent counts, prevalence, employers, tools, "
            "seniority, or source claims. Cite only supplied evidence refs. State ambiguity and "
            "alternatives plainly. A small sample limits confidence; do not generalize broadly. "
            "Empty groups are valid."
        ),
        user_payload={
            "snapshot": {
                "id": snapshot.id,
                "contract": snapshot.snapshot_contract_version,
                "definition_id": snapshot.target_definition_version_id,
                "frozen_metadata": snapshot.metadata,
            },
            "candidate_evidence": list(evidence.values()),
            "primary_work_evidence_refs": work_refs,
            "sources": list(sources.values()),
        },
        schema_name="jobhunter_market_candidate_report",
        schema=_response_schema(list(evidence)),
        model=model,
        max_tokens=min(settings.analysis_max_tokens, 4096),
        seed=0,
    )
    structured = result.structured
    overall_evidence = [evidence[ref] for ref in structured.pop("overall_evidence_refs")]
    for section in ("work_clusters", "possible_role_subfamilies"):
        for group in structured[section]:
            refs = group["evidence_refs"]
            used = [evidence[ref] for ref in refs]
            group["supporting_posting_count"] = len({item["source_job_id"] for item in used})
            group["supporting_source_job_ids"] = sorted({item["source_job_id"] for item in used})
            group["evidence"] = used

    return {
        "contract": REPORT_CONTRACT,
        "prompt_version": PROMPT_VERSION,
        "snapshot_id": snapshot.id,
        "snapshot_contract": snapshot.snapshot_contract_version,
        "target_definition_id": snapshot.target_definition_version_id,
        "model": result.model,
        "source_count": len(sources),
        "evidence_count": len(evidence),
        "overall_evidence": overall_evidence,
        **structured,
        "sources": list(sources.values()),
        "authority_note": (
            "Ephemeral analytical candidate based on accepted P1.6 in this frozen snapshot. "
            "Not employer wording, a promoted taxonomy, or broad-market prevalence."
        ),
    }
