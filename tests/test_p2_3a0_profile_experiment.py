from __future__ import annotations

from typing import Any

import pytest

from jobhunter.canonical_registry import JobClaimMapping, MappingDisposition
from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.p2_3a0_profile_experiment import (
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_a_for_job,
    compose_p23a0_strategy_b_from_public_capability,
)


def _mapping(
    *,
    mapping_id: int,
    claim_index: int,
    source_text: str,
    disposition: str = MappingDisposition.MAPPED.value,
    concept_id: str | None = "skill:python",
    claim_kind: str = "requirement",
) -> JobClaimMapping:
    return JobClaimMapping(
        id=mapping_id,
        analysis_artifact_id=101,
        source_job_id="job-1",
        job_detail_version_id=201,
        translation_artifact_id=301,
        claim_kind=claim_kind,
        claim_index=claim_index,
        source_text=source_text,
        normalized_source_text=source_text.casefold(),
        canonical_concept_id=concept_id,
        disposition=disposition,
        reviewed_at="2026-10-19T12:00:00+00:00",
        review_note="test review",
    )


def _claim(
    *,
    claim_index: int,
    source_text: str,
    claim_kind: str = "requirement",
    mapping: JobClaimMapping | None = None,
    source_job_id: str = "job-1",
) -> CanonicalClaimReviewItem:
    return CanonicalClaimReviewItem(
        analysis_artifact_id=101,
        source_job_id=source_job_id,
        job_detail_version_id=201,
        translation_artifact_id=301,
        claim_kind=claim_kind,
        claim_index=claim_index,
        source_text=source_text,
        evidence=None,
        concept_type=None,
        strength=None,
        depth_signal=None,
        mapping=mapping,
    )


def _public_capability(
    *,
    profiles: list[dict[str, Any]],
    analysis_artifact_id: int = 101,
    job_detail_version_id: int = 201,
    translation_artifact_id: int = 301,
) -> dict[str, Any]:
    return {
        "analysis_artifact_id": analysis_artifact_id,
        "artifact_id": 401,
        "capability_schema_version": "job-capability-intelligence-v5",
        "intelligence": {"capabilities": profiles},
        "job_detail_version_id": job_detail_version_id,
        "model": "accepted-local-model",
        "prompt_version": "job-capability-intelligence-v9",
        "schema_version": "jobhunter-public-corpus-v1",
        "source_job_id": "job-1",
        "stage": "capability",
        "translation_artifact_id": translation_artifact_id,
    }


def _profile(
    *,
    label: str,
    requirements: list[int] | None = None,
    responsibilities: list[int] | None = None,
) -> dict[str, Any]:
    return {
        "capability_label": label,
        "summary": f"Accepted job-local summary for {label}.",
        "requirement_strength": "required",
        "source_requirement_indices": requirements or [],
        "source_responsibility_indices": responsibilities or [],
        "depth_signals": [],
        "work_activities": [],
        "sub_capabilities": [],
        "underlying_knowledge": [],
        "operational_practices": [],
        "operational_context": [],
        "unknown_scope": [],
        "independence_expectation": None,
        "overall_confidence": "high",
    }


def test_strategy_a_groups_only_reviewed_shared_canonical_identity() -> None:
    first_text = "Strong Python programming skills"
    second_text = "Proficient knowledge of Python"
    claims = (
        _claim(
            claim_index=0,
            source_text=first_text,
            mapping=_mapping(mapping_id=1, claim_index=0, source_text=first_text),
        ),
        _claim(
            claim_index=1,
            source_text=second_text,
            mapping=_mapping(mapping_id=2, claim_index=1, source_text=second_text),
        ),
    )

    result = compose_p23a0_strategy_a("job-1", claims)

    assert result.claim_count == 2
    assert len(result.buckets) == 1
    assert result.canonical_bucket_count == 1
    assert result.source_local_bucket_count == 0
    assert result.deterministic_grouping_savings == 1
    assert result.buckets[0].key == "canonical:skill:python"
    assert result.buckets[0].canonical_concept_id == "skill:python"
    assert result.buckets[0].claims == claims


def test_pending_same_wording_remains_two_source_local_claims() -> None:
    claims = (
        _claim(claim_index=0, source_text="Python"),
        _claim(claim_index=1, source_text="Python"),
    )

    result = compose_p23a0_strategy_a("job-1", claims)

    assert result.claim_count == 2
    assert len(result.buckets) == 2
    assert result.canonical_bucket_count == 0
    assert result.source_local_bucket_count == 2
    assert result.deterministic_grouping_savings == 0
    assert {bucket.key for bucket in result.buckets} == {
        "source:101:requirement:0",
        "source:101:requirement:1",
    }


@pytest.mark.parametrize("disposition", ["unmapped", "rejected"])
def test_reviewed_nonmapped_claim_remains_source_local(disposition: str) -> None:
    text = "Python"
    mapping = _mapping(
        mapping_id=1,
        claim_index=0,
        source_text=text,
        disposition=disposition,
        concept_id=None,
    )

    result = compose_p23a0_strategy_a(
        "job-1",
        (_claim(claim_index=0, source_text=text, mapping=mapping),),
    )

    assert result.buckets[0].basis == "exact_source_claim"
    assert result.buckets[0].canonical_concept_id is None
    assert result.mapped_claim_count == 0


def test_requirement_only_input_never_fabricates_responsibility_claims() -> None:
    mapped_text = "Python proficiency"
    claims = (
        _claim(
            claim_index=0,
            source_text=mapped_text,
            mapping=_mapping(mapping_id=1, claim_index=0, source_text=mapped_text),
        ),
        _claim(claim_index=1, source_text="PyTorch experience"),
    )

    result = compose_p23a0_strategy_a("job-1", claims)

    assert result.requirement_claim_count == 2
    assert result.responsibility_claim_count == 0
    assert all(
        claim.claim_kind == "requirement"
        for bucket in result.buckets
        for claim in bucket.claims
    )


def test_mapped_claim_requires_exact_registry_provenance_match() -> None:
    mapping = _mapping(mapping_id=1, claim_index=0, source_text="Different wording")
    claim = _claim(claim_index=0, source_text="Python")
    claim = CanonicalClaimReviewItem(
        analysis_artifact_id=claim.analysis_artifact_id,
        source_job_id=claim.source_job_id,
        job_detail_version_id=claim.job_detail_version_id,
        translation_artifact_id=claim.translation_artifact_id,
        claim_kind=claim.claim_kind,
        claim_index=claim.claim_index,
        source_text=claim.source_text,
        evidence=claim.evidence,
        concept_type=claim.concept_type,
        strength=claim.strength,
        depth_signal=claim.depth_signal,
        mapping=mapping,
    )

    with pytest.raises(ValueError, match="provenance does not match"):
        compose_p23a0_strategy_a("job-1", (claim,))


def test_strategy_a_rejects_mixed_job_claims() -> None:
    claims = (
        _claim(claim_index=0, source_text="Python"),
        _claim(claim_index=1, source_text="RAG", source_job_id="job-2"),
    )

    with pytest.raises(ValueError, match="exactly one source job"):
        compose_p23a0_strategy_a("job-1", claims)


def test_strategy_a_rejects_duplicate_exact_claim_identity() -> None:
    claim = _claim(claim_index=0, source_text="Python")

    with pytest.raises(ValueError, match="Duplicate exact claim identity"):
        compose_p23a0_strategy_a("job-1", (claim, claim))


def test_for_job_reads_only_current_claims_for_requested_job() -> None:
    claims = (_claim(claim_index=0, source_text="Python"),)

    class FakeReader:
        def list_current_claims(self, **kwargs: object) -> tuple[CanonicalClaimReviewItem, ...]:
            assert kwargs == {
                "source_job_id": "job-1",
                "mapping_state": "all",
                "limit": 5000,
            }
            return claims

    result = compose_p23a0_strategy_a_for_job(FakeReader(), " job-1 ")  # type: ignore[arg-type]

    assert result.source_job_id == "job-1"
    assert result.claim_count == 1


def test_strategy_b_uses_capability_group_only_as_job_local_organization() -> None:
    python_text = "Python proficiency"
    work_text = "Build backend services"
    base = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(
                claim_index=0,
                source_text=python_text,
                mapping=_mapping(
                    mapping_id=1,
                    claim_index=0,
                    source_text=python_text,
                    concept_id="skill:python",
                ),
            ),
            _claim(
                claim_index=0,
                claim_kind="responsibility",
                source_text=work_text,
                mapping=_mapping(
                    mapping_id=2,
                    claim_index=0,
                    claim_kind="responsibility",
                    source_text=work_text,
                    concept_id="responsibility:build-backend-services",
                ),
            ),
            _claim(claim_index=1, source_text="FastAPI familiarity"),
        ),
    )
    capability = _public_capability(
        profiles=[
            _profile(
                label="Python backend engineering",
                requirements=[0, 1],
                responsibilities=[0],
            )
        ]
    )

    result = compose_p23a0_strategy_b_from_public_capability(base, capability)

    assert result.capability_artifact_id == 401
    assert result.capability_model == "accepted-local-model"
    assert len(result.groups) == 1
    group = result.groups[0]
    assert group.job_local_label == "Python backend engineering"
    assert group.requirement_claim_count == 2
    assert group.responsibility_claim_count == 1
    assert group.canonical_concept_ids == (
        "responsibility:build-backend-services",
        "skill:python",
    )
    assert result.canonical_concept_ids == group.canonical_concept_ids
    assert result.ungrouped_claims == ()


def test_strategy_b_does_not_turn_job_local_label_into_canonical_identity() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (_claim(claim_index=0, source_text="RAG familiarity"),),
    )
    capability = _public_capability(
        profiles=[_profile(label="RAG", requirements=[0])]
    )

    result = compose_p23a0_strategy_b_from_public_capability(base, capability)

    assert result.groups[0].job_local_label == "RAG"
    assert result.groups[0].canonical_concept_ids == ()
    assert result.canonical_concept_ids == ()


def test_strategy_b_preserves_claims_not_grouped_by_capability_v9() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (
            _claim(claim_index=0, source_text="Python"),
            _claim(claim_index=1, source_text="Three years experience"),
        ),
    )
    capability = _public_capability(
        profiles=[_profile(label="Programming", requirements=[0])]
    )

    result = compose_p23a0_strategy_b_from_public_capability(base, capability)

    assert result.grouped_claim_count == 1
    assert len(result.ungrouped_claims) == 1
    assert result.ungrouped_claims[0].claim_index == 1


def test_strategy_b_rejects_dependency_mismatch() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (_claim(claim_index=0, source_text="Python"),),
    )
    capability = _public_capability(
        profiles=[_profile(label="Programming", requirements=[0])],
        analysis_artifact_id=999,
    )

    with pytest.raises(ValueError, match="dependencies do not match"):
        compose_p23a0_strategy_b_from_public_capability(base, capability)


def test_strategy_b_rejects_non_public_or_non_v9_input() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (_claim(claim_index=0, source_text="Python"),),
    )
    capability = _public_capability(
        profiles=[_profile(label="Programming", requirements=[0])]
    )
    capability["schema_version"] = "local-private-artifact"

    with pytest.raises(ValueError, match="public-corpus"):
        compose_p23a0_strategy_b_from_public_capability(base, capability)


def test_strategy_b_requirement_only_job_rejects_fabricated_responsibility_link() -> None:
    base = compose_p23a0_strategy_a(
        "job-1",
        (_claim(claim_index=0, source_text="Python"),),
    )
    capability = _public_capability(
        profiles=[
            _profile(
                label="Programming",
                requirements=[0],
                responsibilities=[0],
            )
        ]
    )

    with pytest.raises(ValueError, match="unavailable .*responsibility.*0"):
        compose_p23a0_strategy_b_from_public_capability(base, capability)
