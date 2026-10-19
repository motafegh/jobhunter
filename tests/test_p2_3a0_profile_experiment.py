from __future__ import annotations

import pytest

from jobhunter.canonical_registry import JobClaimMapping, MappingDisposition
from jobhunter.canonical_registry_review import CanonicalClaimReviewItem
from jobhunter.p2_3a0_profile_experiment import (
    compose_p23a0_strategy_a,
    compose_p23a0_strategy_a_for_job,
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
