"""Bounded, ephemeral Market work and role-subfamily interpretation."""

from __future__ import annotations

import re
from typing import Any

import httpx

from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import LMStudioProvider
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore

REPORT_CONTRACT = "market-role-family-candidate-v3"
PROMPT_VERSION = "market-role-family-candidate-prompt-v3"


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


def _resolve_source_aliases(value: Any, aliases: dict[str, str]) -> Any:
    if isinstance(value, str):
        for source_job_id, alias in aliases.items():
            value = re.sub(rf"\b{re.escape(alias)}\b", source_job_id, value)
        return value
    if isinstance(value, list):
        return [_resolve_source_aliases(item, aliases) for item in value]
    if isinstance(value, dict):
        return {
            key: _resolve_source_aliases(item, aliases)
            for key, item in value.items()
        }
    return value


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

    if not evidence:
        raise ValueError("Snapshot has no accepted-core P1.6 claims for interpretation")
    model = model_override or settings.effective_analysis_lm_studio_model()
    if not model:
        raise ValueError("No analysis model is configured")

    source_aliases = {
        source_job_id: f"J{index}"
        for index, source_job_id in enumerate(sources, start=1)
    }
    compact_ref_map = {
        f"C{index}": full_ref for index, full_ref in enumerate(evidence, start=1)
    }
    compact_claims = [
        [
            compact_ref,
            source_aliases[evidence[full_ref]["source_job_id"]],
            "W" if evidence[full_ref]["kind"] == "responsibility" else "Q",
            evidence[full_ref]["statement"],
            evidence[full_ref].get("requirement_type"),
        ]
        for compact_ref, full_ref in compact_ref_map.items()
    ]

    ensure_lm_studio_model_context(
        openai_base_url=settings.lm_studio_base_url,
        model=model,
        context_length=16_384,
        api_token=settings.lm_studio_api_token,
        connect_timeout_seconds=min(settings.inference_timeout_seconds, 10.0),
        exclusive_llm=True,
    )

    provider = LMStudioProvider(
        base_url=settings.lm_studio_base_url,
        configured_model=model,
        api_token=settings.lm_studio_api_token,
        timeout_seconds=httpx.Timeout(
            connect=10.0,
            read=None,
            write=30.0,
            pool=10.0,
        ),
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
            "Do not speculate that source wording is copied or erroneous. Requirements are "
            "available as Q claims; do not claim tools or counts are unavailable. Employer names "
            "are intentionally omitted from the input. Describe counts as snapshot coverage, not "
            "market demand. If a title adds a specialization beyond its cited claims, lower "
            "confidence and state the uncertainty. Empty groups are valid."
        ),
        user_payload={
            "snapshot": {
                "id": snapshot.id,
                "contract": snapshot.snapshot_contract_version,
                "definition_id": snapshot.target_definition_version_id,
            },
            "source_aliases": [
                [source_aliases[source_job_id], value["title"]]
                for source_job_id, value in sources.items()
            ],
            "sample_counts": {
                "accepted_semantic_core_postings": len(sources),
                "responsibility_claims": sum(
                    item["kind"] == "responsibility" for item in evidence.values()
                ),
                "requirement_claims": sum(
                    item["kind"] == "requirement" for item in evidence.values()
                ),
            },
            "claims": compact_claims,
            "work_claim_refs": [
                compact_ref
                for compact_ref, full_ref in compact_ref_map.items()
                if evidence[full_ref]["kind"] == "responsibility"
            ],
        },
        schema_name="jobhunter_market_candidate_report",
        schema=_response_schema(list(compact_ref_map)),
        model=model,
        max_tokens=min(settings.analysis_max_tokens, 2048),
        seed=0,
    )
    structured = _resolve_source_aliases(result.structured, source_aliases)
    overall_evidence = [
        evidence[compact_ref_map[ref]]
        for ref in structured.pop("overall_evidence_refs")
    ]
    for section in ("work_clusters", "possible_role_subfamilies"):
        for group in structured[section]:
            refs = [compact_ref_map[ref] for ref in group["evidence_refs"]]
            used = [evidence[ref] for ref in refs]
            group["evidence_refs"] = refs
            group["supporting_posting_count"] = len({item["source_job_id"] for item in used})
            group["supporting_source_job_ids"] = sorted({item["source_job_id"] for item in used})
            if group["supporting_posting_count"] == 1:
                group["confidence"] = "low"
            elif group["supporting_posting_count"] < 4 and group["confidence"] == "high":
                group["confidence"] = "moderate"
            group["evidence"] = used

    source_ids_without_responsibilities = sorted(
        source_job_id
        for source_job_id in sources
        if not any(
            item["source_job_id"] == source_job_id
            and item["kind"] == "responsibility"
            for item in evidence.values()
        )
    )
    return {
        "contract": REPORT_CONTRACT,
        "prompt_version": PROMPT_VERSION,
        "snapshot_id": snapshot.id,
        "snapshot_contract": snapshot.snapshot_contract_version,
        "target_definition_id": snapshot.target_definition_version_id,
        "model": result.model,
        "source_count": len(sources),
        "evidence_count": len(evidence),
        "source_aliases": {
            source_aliases[source_job_id]: {
                "source_job_id": source_job_id,
                "title": value["title"],
            }
            for source_job_id, value in sources.items()
        },
        "responsibility_coverage": {
            "postings_with_work_claims": sum(
                any(
                    item["source_job_id"] == source_job_id
                    and item["kind"] == "responsibility"
                    for item in evidence.values()
                )
                for source_job_id in sources
            ),
            "postings_without_work_claims": sorted(
                source_ids_without_responsibilities
            ),
        },
        "scope_limitations": [
            f"Small snapshot sample: {len(sources)} accepted-semantic core postings.",
            f"{len(source_ids_without_responsibilities)} of {len(sources)} postings have no "
            "extracted responsibilities; their duties are not inferred.",
            "Employer names are withheld from the interpretation input.",
            "This point-in-time snapshot does not establish broad-market prevalence or trends.",
        ],
        "overall_evidence": overall_evidence,
        **structured,
        "sources": list(sources.values()),
        "authority_note": (
            "Ephemeral analytical candidate based on accepted P1.6 in this frozen snapshot. "
            "Not employer wording, a promoted taxonomy, or broad-market prevalence."
        ),
    }
