"""Bounded, ephemeral Market work and role-subfamily interpretation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import httpx

from jobhunter.analysis_store import AnalysisStore
from jobhunter.config import Settings
from jobhunter.inference.lm_studio import LMStudioProvider
from jobhunter.inference.lm_studio_runtime import ensure_lm_studio_model_context
from jobhunter.market_store import MarketStore
from jobhunter.storage import JobHunterStore

REPORT_CONTRACT = "market-role-family-candidate-v6"
PROMPT_VERSION = "market-role-family-candidate-prompt-v6"

_INTERNAL_CITATION_RE = re.compile(r"\bC\d+\b")


class CandidateProseIntegrityError(ValueError):
    """One model-authored interpretation item failed a user-facing integrity check."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class PreparedMarketCandidateReport:
    """Exact accepted V6 input and semantic generation identity before inference."""

    snapshot_id: int
    snapshot_contract: str
    target_definition_id: int
    model: str
    generation_identity: dict[str, Any]
    candidate_input: dict[str, Any]
    response_schema: dict[str, Any]
    evidence: dict[str, dict[str, Any]]
    sources: dict[str, dict[str, Any]]
    source_aliases: dict[str, str]
    compact_ref_map: dict[str, str]


@dataclass(frozen=True, slots=True)
class GeneratedMarketCandidateReport:
    """Validated V6 report plus private inference audit payloads."""

    report: dict[str, Any]
    request_body: dict[str, Any]
    raw_response: dict[str, Any]


def _evidence_bound_text_schema(
    citation_ids: list[str],
    *,
    text_key: str = "text",
    max_length: int = 600,
) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [text_key, "evidence_refs"],
        "properties": {
            text_key: {"type": "string", "minLength": 1, "maxLength": max_length},
            "evidence_refs": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"type": "string", "enum": citation_ids},
            },
        },
    }


def _response_schema(citation_ids: list[str]) -> dict[str, Any]:
    interpretation_point = _evidence_bound_text_schema(citation_ids)
    alternative = _evidence_bound_text_schema(
        citation_ids,
        text_key="label",
        max_length=240,
    )
    item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "label",
            "interpretation_points",
            "confidence",
            "alternatives",
        ],
        "properties": {
            "label": {"type": "string", "minLength": 1, "maxLength": 120},
            "interpretation_points": {
                "type": "array",
                "minItems": 1,
                "maxItems": 4,
                "items": interpretation_point,
            },
            "confidence": {"type": "string", "enum": ["low", "moderate", "high"]},
            "alternatives": {
                "type": "array",
                "items": alternative,
                "maxItems": 4,
            },
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "overall_observations",
            "work_clusters",
            "possible_role_subfamilies",
            "limitations",
        ],
        "properties": {
            "overall_observations": {
                "type": "array",
                "minItems": 1,
                "maxItems": 6,
                "items": interpretation_point,
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


def _ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _resolve_evidence_refs(
    compact_refs: list[str],
    *,
    compact_ref_map: dict[str, str],
    evidence: dict[str, dict[str, Any]],
) -> tuple[list[str], list[dict[str, Any]]]:
    full_refs = [compact_ref_map[ref] for ref in compact_refs]
    return full_refs, [evidence[ref] for ref in full_refs]


def _normalize_declared_compact_citations(
    text: str,
    *,
    compact_refs: list[str],
) -> str:
    mentioned_refs = _ordered_unique(_INTERNAL_CITATION_RE.findall(text))
    undeclared_refs = [ref for ref in mentioned_refs if ref not in compact_refs]
    if undeclared_refs:
        raise CandidateProseIntegrityError("compact_evidence_id_without_matching_ref")
    if not mentioned_refs:
        return text

    normalized = re.sub(
        r"\s*[\(\[]\s*C\d+(?:\s*[,;/&]\s*C\d+)*\s*[\)\]]",
        "",
        text,
    )
    normalized = _INTERNAL_CITATION_RE.sub("", normalized)
    normalized = re.sub(r"\(\s*\)|\[\s*\]", "", normalized)
    normalized = re.sub(r"\s+([,.;:!?])", r"\1", normalized)
    normalized = re.sub(r"([,;:])\s*([,;:])+", r"\1", normalized)
    normalized = re.sub(r"\s{2,}", " ", normalized).strip()
    normalized = re.sub(r"^[,;:]\s*", "", normalized)
    if not normalized:
        raise CandidateProseIntegrityError("empty_after_compact_citation_normalization")
    return normalized


def _validate_and_resolve_prose(
    text: str,
    *,
    compact_refs: list[str],
    compact_ref_map: dict[str, str],
    evidence: dict[str, dict[str, Any]],
    source_aliases: dict[str, str],
) -> str:
    normalized_text = _normalize_declared_compact_citations(
        text,
        compact_refs=compact_refs,
    )

    cited_source_job_ids = {
        evidence[compact_ref_map[ref]]["source_job_id"] for ref in compact_refs
    }
    for source_job_id, alias in source_aliases.items():
        alias_is_mentioned = (
            re.search(rf"\b{re.escape(alias)}\b", normalized_text) is not None
        )
        if alias_is_mentioned and source_job_id not in cited_source_job_ids:
            raise CandidateProseIntegrityError("source_alias_without_matching_evidence")
    return _resolve_source_aliases(normalized_text, source_aliases)


def _hydrate_evidence_bound_text(
    item: dict[str, Any],
    *,
    text_key: str,
    compact_ref_map: dict[str, str],
    evidence: dict[str, dict[str, Any]],
    source_aliases: dict[str, str],
) -> dict[str, Any]:
    compact_refs = list(item["evidence_refs"])
    full_refs, used = _resolve_evidence_refs(
        compact_refs,
        compact_ref_map=compact_ref_map,
        evidence=evidence,
    )
    resolved_text = _validate_and_resolve_prose(
        item[text_key],
        compact_refs=compact_refs,
        compact_ref_map=compact_ref_map,
        evidence=evidence,
        source_aliases=source_aliases,
    )
    supporting_source_job_ids = sorted({entry["source_job_id"] for entry in used})
    return {
        text_key: resolved_text,
        "evidence_refs": full_refs,
        "evidence": used,
        "evidence_count": len(full_refs),
        "supporting_posting_count": len(supporting_source_job_ids),
        "supporting_source_job_ids": supporting_source_job_ids,
    }


def _support_basis(used: list[dict[str, Any]]) -> str:
    kinds = {item["kind"] for item in used}
    if kinds == {"responsibility"}:
        return "responsibility_supported_work"
    if kinds == {"requirement"}:
        return "requirement_derived_specialty"
    return "mixed_responsibility_and_requirement"


def _integrity_issue(path: str, code: str) -> dict[str, str]:
    return {"path": path, "code": code}


def _hydrate_group(
    group: dict[str, Any],
    *,
    path: str,
    compact_ref_map: dict[str, str],
    evidence: dict[str, dict[str, Any]],
    source_aliases: dict[str, str],
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    points: list[dict[str, Any]] = []
    accepted_raw_points: list[dict[str, Any]] = []
    for index, item in enumerate(group["interpretation_points"]):
        try:
            point = _hydrate_evidence_bound_text(
                item,
                text_key="text",
                compact_ref_map=compact_ref_map,
                evidence=evidence,
                source_aliases=source_aliases,
            )
        except CandidateProseIntegrityError as exc:
            issues.append(
                _integrity_issue(f"{path}.interpretation_points[{index}]", exc.code)
            )
            continue
        points.append(point)
        accepted_raw_points.append(item)

    if not points:
        issues.append(_integrity_issue(path, "no_integrity_safe_interpretation_points"))
        return None, issues

    compact_primary_refs = _ordered_unique(
        [
            ref
            for item in accepted_raw_points
            for ref in item["evidence_refs"]
        ]
    )
    full_refs, used = _resolve_evidence_refs(
        compact_primary_refs,
        compact_ref_map=compact_ref_map,
        evidence=evidence,
    )
    try:
        resolved_label = _validate_and_resolve_prose(
            group["label"],
            compact_refs=compact_primary_refs,
            compact_ref_map=compact_ref_map,
            evidence=evidence,
            source_aliases=source_aliases,
        )
    except CandidateProseIntegrityError as exc:
        issues.append(_integrity_issue(f"{path}.label", exc.code))
        return None, issues

    alternatives: list[dict[str, Any]] = []
    for index, item in enumerate(group["alternatives"]):
        try:
            alternative = _hydrate_evidence_bound_text(
                item,
                text_key="label",
                compact_ref_map=compact_ref_map,
                evidence=evidence,
                source_aliases=source_aliases,
            )
        except CandidateProseIntegrityError as exc:
            issues.append(_integrity_issue(f"{path}.alternatives[{index}]", exc.code))
            continue
        alternatives.append(alternative)

    supporting_source_job_ids = sorted({item["source_job_id"] for item in used})
    supporting_posting_count = len(supporting_source_job_ids)
    confidence = group["confidence"]
    if supporting_posting_count == 1:
        confidence = "low"
    elif supporting_posting_count < 4 and confidence == "high":
        confidence = "moderate"
    return (
        {
            "label": resolved_label,
            "interpretation_points": points,
            "evidence_refs": full_refs,
            "evidence": used,
            "evidence_count": len(full_refs),
            "supporting_posting_count": supporting_posting_count,
            "supporting_source_job_ids": supporting_source_job_ids,
            "confidence": confidence,
            "alternatives": alternatives,
            "support_basis": _support_basis(used),
            "candidate_scope": (
                "single_posting_specialty_or_outlier"
                if supporting_posting_count == 1
                else "multi_posting_pattern"
            ),
        },
        issues,
    )


def _safe_model_limitations(
    limitations: list[str],
    *,
    source_aliases: dict[str, str],
) -> tuple[list[str], list[dict[str, str]]]:
    safe: list[str] = []
    issues: list[dict[str, str]] = []
    aliases = tuple(source_aliases.values())
    for index, text in enumerate(limitations):
        if _INTERNAL_CITATION_RE.search(text):
            issues.append(
                _integrity_issue(
                    f"limitations[{index}]",
                    "internal_compact_evidence_id",
                )
            )
            continue
        if any(re.search(rf"\b{re.escape(alias)}\b", text) for alias in aliases):
            issues.append(
                _integrity_issue(
                    f"limitations[{index}]",
                    "uncited_source_alias_in_limitation",
                )
            )
            continue
        safe.append(text)
    return safe, issues


def prepare_market_candidate_report(
    settings: Settings,
    snapshot_id: int,
    *,
    model_override: str | None = None,
) -> PreparedMarketCandidateReport:
    """Derive the exact accepted V6 model input without calling LM Studio."""
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


    candidate_input = {
        "snapshot": {
            "id": snapshot.id,
            "contract": snapshot.snapshot_contract_version,
            "definition_id": snapshot.target_definition_version_id,
        },
        "source_aliases": list(source_aliases.values()),
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
    }
    max_tokens = min(settings.analysis_max_tokens, 2048)
    return PreparedMarketCandidateReport(
        snapshot_id=snapshot.id,
        snapshot_contract=snapshot.snapshot_contract_version,
        target_definition_id=snapshot.target_definition_version_id,
        model=model,
        generation_identity={
            "provider": "lm-studio",
            "model": model,
            "context_length": 16_384,
            "max_tokens": max_tokens,
            "seed": 0,
            "structured_schema": "jobhunter_market_candidate_report",
        },
        candidate_input=candidate_input,
        response_schema=_response_schema(list(compact_ref_map)),
        evidence=evidence,
        sources=sources,
        source_aliases=source_aliases,
        compact_ref_map=compact_ref_map,
    )


def generate_market_candidate_report(
    settings: Settings,
    prepared: PreparedMarketCandidateReport,
) -> GeneratedMarketCandidateReport:
    """Run accepted V6 inference over an already-derived exact candidate input."""

    model = prepared.model
    evidence = prepared.evidence
    sources = prepared.sources
    source_aliases = prepared.source_aliases
    compact_ref_map = prepared.compact_ref_map

    ensure_lm_studio_model_context(
        openai_base_url=settings.lm_studio_base_url,
        model=model,
        context_length=prepared.generation_identity["context_length"],
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
            "Group related work and suggest possible role subfamilies only where exact "
            "cited claims support the interpretation. These are hypotheses, not employer facts "
            "or promoted taxonomy. Responsibilities are primary evidence for performed work. "
            "Requirements may identify a specialty or qualification shape, but must never be "
            "relabeled as duties. Every overall observation, interpretation point, and "
            "alternative label must cite only the exact supplied evidence refs that support that "
            "text. Prefer not to mention source aliases in prose because JobHunter presents "
            "supporting postings separately. If you do mention one, that text must cite evidence "
            "from that same source. Do not write compact C-number citation IDs in prose; "
            "use them only in evidence_refs. JobHunter may normalize a declared compact citation "
            "if one still appears, but an undeclared compact citation invalidates that item. "
            "Do not import a concrete tool, system, employer, specialization, or "
            "other source detail from uncited claims. Jobs may support multiple work clusters or "
            "none. Possible role subfamilies must be supported by at least two distinct postings "
            "and must add a role-shape distinction rather than merely rename a work cluster; "
            "otherwise omit them. A one-posting pattern may remain a work cluster/specialty "
            "hypothesis but is not evidence of a reusable subfamily. Do not invent counts, "
            "prevalence, employers, tools, seniority, or source claims. State ambiguity and "
            "alternatives plainly. A small sample limits confidence; do not generalize broadly. "
            "Do not speculate that source wording is copied or erroneous. Employer names and job "
            "titles are intentionally omitted from the model input. Limitations must stay at the "
            "sample/method level and must not mention source aliases or compact evidence IDs. "
            "Describe counts as snapshot coverage, not market demand. Empty groups are valid."
        ),
        user_payload=prepared.candidate_input,
        schema_name=prepared.generation_identity["structured_schema"],
        schema=prepared.response_schema,
        model=model,
        max_tokens=prepared.generation_identity["max_tokens"],
        seed=prepared.generation_identity["seed"],
    )
    if result.model != model:
        raise ValueError(
            "Candidate report provider returned a different model identity than requested"
        )
    structured = result.structured
    integrity_rejections: list[dict[str, str]] = []

    overall_observations: list[dict[str, Any]] = []
    for index, item in enumerate(structured["overall_observations"]):
        try:
            observation = _hydrate_evidence_bound_text(
                item,
                text_key="text",
                compact_ref_map=compact_ref_map,
                evidence=evidence,
                source_aliases=source_aliases,
            )
        except CandidateProseIntegrityError as exc:
            integrity_rejections.append(
                _integrity_issue(f"overall_observations[{index}]", exc.code)
            )
            continue
        overall_observations.append(observation)

    work_clusters: list[dict[str, Any]] = []
    for index, group in enumerate(structured["work_clusters"]):
        hydrated, issues = _hydrate_group(
            group,
            path=f"work_clusters[{index}]",
            compact_ref_map=compact_ref_map,
            evidence=evidence,
            source_aliases=source_aliases,
        )
        integrity_rejections.extend(issues)
        if hydrated is not None:
            work_clusters.append(hydrated)

    hydrated_roles: list[dict[str, Any]] = []
    for index, group in enumerate(structured["possible_role_subfamilies"]):
        hydrated, issues = _hydrate_group(
            group,
            path=f"possible_role_subfamilies[{index}]",
            compact_ref_map=compact_ref_map,
            evidence=evidence,
            source_aliases=source_aliases,
        )
        integrity_rejections.extend(issues)
        if hydrated is not None:
            hydrated_roles.append(hydrated)

    model_limitations, limitation_issues = _safe_model_limitations(
        structured["limitations"],
        source_aliases=source_aliases,
    )
    integrity_rejections.extend(limitation_issues)

    if not (overall_observations or work_clusters or hydrated_roles):
        raise ValueError(
            "Candidate report contained no integrity-safe interpretation after post-validation"
        )

    possible_role_subfamilies = [
        group for group in hydrated_roles if group["supporting_posting_count"] >= 2
    ]
    specialty_candidates = [
        group for group in hydrated_roles if group["supporting_posting_count"] == 1
    ]

    cited_refs = _ordered_unique(
        [
            ref
            for item in overall_observations
            for ref in item["evidence_refs"]
        ]
        + [
            ref
            for group in work_clusters + hydrated_roles
            for ref in group["evidence_refs"]
        ]
        + [
            ref
            for group in work_clusters + hydrated_roles
            for alternative in group["alternatives"]
            for ref in alternative["evidence_refs"]
        ]
    )
    overall_source_job_ids = sorted(
        {
            source_job_id
            for item in overall_observations
            for source_job_id in item["supporting_source_job_ids"]
        }
    )
    source_ids_without_responsibilities = sorted(
        source_job_id
        for source_job_id in sources
        if not any(
            item["source_job_id"] == source_job_id
            and item["kind"] == "responsibility"
            for item in evidence.values()
        )
    )
    responsibility_claim_count = sum(
        item["kind"] == "responsibility" for item in evidence.values()
    )
    requirement_claim_count = sum(
        item["kind"] == "requirement" for item in evidence.values()
    )
    report = {
        "contract": REPORT_CONTRACT,
        "prompt_version": PROMPT_VERSION,
        "snapshot_id": snapshot.id,
        "snapshot_contract": snapshot.snapshot_contract_version,
        "target_definition_id": snapshot.target_definition_version_id,
        "model": result.model,
        "source_count": len(sources),
        "available_evidence_count": len(evidence),
        "available_responsibility_claim_count": responsibility_claim_count,
        "available_requirement_claim_count": requirement_claim_count,
        "cited_evidence_count": len(cited_refs),
        "source_aliases": {
            source_aliases[source_job_id]: {
                "source_job_id": source_job_id,
                "title": value["title"],
            }
            for source_job_id, value in sources.items()
        },
        "overall_observations": overall_observations,
        "overall_supporting_source_job_ids": overall_source_job_ids,
        "responsibility_coverage": {
            "postings_with_work_claims": sum(
                any(
                    item["source_job_id"] == source_job_id
                    and item["kind"] == "responsibility"
                    for item in evidence.values()
                )
                for source_job_id in sources
            ),
            "postings_without_work_claims": source_ids_without_responsibilities,
        },
        "scope_limitations": [
            f"Small snapshot sample: {len(sources)} accepted-semantic core postings.",
            f"{len(source_ids_without_responsibilities)} of {len(sources)} postings have no "
            "extracted responsibilities; their duties are not inferred.",
            "Requirement-only groups are specialty/qualification hypotheses, not inferred duties.",
            "Employer names and job titles are withheld from the interpretation input.",
            "This point-in-time snapshot does not establish broad-market prevalence or trends.",
            *(
                [
                    f"JobHunter omitted {len(integrity_rejections)} model-authored item(s) "
                    "that failed post-generation integrity checks."
                ]
                if integrity_rejections
                else []
            ),
        ],
        "work_clusters": work_clusters,
        "possible_role_subfamilies": possible_role_subfamilies,
        "specialty_candidates": specialty_candidates,
        "limitations": model_limitations,
        "integrity_rejection_count": len(integrity_rejections),
        "integrity_rejections": integrity_rejections,
        "sources": list(sources.values()),
        "authority_note": (
            "Ephemeral analytical candidate based on accepted P1.6 in this frozen snapshot. "
            "Not employer wording, a promoted taxonomy, or broad-market prevalence."
        ),
    }
    return GeneratedMarketCandidateReport(
        report=report,
        request_body=result.request_body,
        raw_response=result.raw_response,
    )



def build_market_candidate_report(
    settings: Settings,
    snapshot_id: int,
    *,
    model_override: str | None = None,
) -> dict[str, Any]:
    """Interpret accepted exact P1.6 from one immutable snapshot without persisting it."""

    prepared = prepare_market_candidate_report(
        settings,
        snapshot_id,
        model_override=model_override,
    )
    return generate_market_candidate_report(settings, prepared).report

