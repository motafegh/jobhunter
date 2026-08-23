from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import SEMANTIC_REVIEW_PENDING, AnalysisStore
from jobhunter.canonical_registry import (
    AliasProvenanceKind,
    CanonicalRegistryError,
    CanonicalRegistryService,
    CanonicalRegistryStore,
    ClaimKind,
    ConceptCategory,
    MappingDisposition,
    normalize_registry_text,
    validate_concept_id,
)
from jobhunter.sources import DiscoveredJobLink
from jobhunter.storage import JobHunterStore
from jobhunter.translation_service import TranslationService
from jobhunter.translation_store import TranslationStore

_NOW = datetime(2026, 8, 23, 12, tzinfo=UTC)


def _seed_analysis(
    database_path: Path,
    *,
    job_id: str = "registry1",
    review_status: str = "accepted",
) -> tuple[TranslationService, int]:
    source_store = JobHunterStore(database_path)
    source_store.initialize()
    posting = source_store.upsert_job(
        job=DiscoveredJobLink(
            source_job_id=job_id,
            company_slug="example",
            canonical_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
            observed_text="Python Engineer",
        ),
        observed_at=_NOW,
    )
    detail = source_store.record_job_detail(
        job_posting_id=posting.job_posting_id,
        fetched_at=_NOW,
        requested_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        final_url=f"https://jobinja.ir/companies/example/jobs/{job_id}/role",
        status_code=200,
        content_sha256=f"content-{job_id}",
        semantic_sha256=f"semantic-{job_id}",
        evidence_path=Path(f"{job_id}.html"),
        metadata_path=Path(f"{job_id}.json"),
        parser_version="jobinja-detail-v2",
        parse_status="parsed",
        fields={
            "language": "en",
            "title": "Python Engineer",
            "description": "Build Python services.",
            "skills": ["Python"],
        },
    )
    translation_service = TranslationService(
        store=TranslationStore(database_path),
        provider=None,
    )
    translation = translation_service.translate_job(job_id)
    analysis_id = AnalysisStore(database_path).record_artifact(
        job_detail_version_id=detail.version_id,
        translation_artifact_id=translation.artifact_id,
        model="analysis-model",
        prompt_version=ENGLISH_PROMPT_VERSION,
        schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        analysis={
            "requirements": [
                {
                    "concept": "Python",
                    "concept_type": "skill",
                    "evidence": "Python",
                },
                {
                    "concept": "Unclear internal stack",
                    "concept_type": "context",
                    "evidence": "Internal stack",
                },
                {
                    "concept": "Generic technology wording",
                    "concept_type": "context",
                    "evidence": "Technology",
                },
            ],
            "responsibilities": [
                {
                    "statement": "Build Python services",
                    "evidence": "Build Python services.",
                }
            ],
        },
        request_body={},
        raw_response={},
        created_at=_NOW,
        semantic_review_status=review_status,
    )
    return translation_service, analysis_id


def _create_concept(
    store: CanonicalRegistryStore,
    concept_id: str,
    category: ConceptCategory,
    label: str,
):
    return store.create_concept(
        concept_id=concept_id,
        category=category,
        preferred_label=label,
        description=None,
        reviewed_at=_NOW,
        review_note="Reviewed canonical concept",
    )


def test_registry_normalization_preserves_punctuation_and_validates_stable_id() -> None:
    assert normalize_registry_text("  ＰｏｓｔｇｒｅＳＱＬ  /  SQL ") == "postgresql / sql"
    assert validate_concept_id("tool:postgresql", ConceptCategory.TOOL) == (
        "tool:postgresql"
    )
    with pytest.raises(CanonicalRegistryError, match="lowercase-kebab-slug"):
        validate_concept_id("tool:PostgreSQL", ConceptCategory.TOOL)
    with pytest.raises(CanonicalRegistryError, match="tool:"):
        validate_concept_id("platform:postgresql", ConceptCategory.TOOL)


def test_reviewed_concepts_and_aliases_are_idempotent_and_collision_safe(
    tmp_path: Path,
) -> None:
    store = CanonicalRegistryStore(tmp_path / "registry.sqlite3")
    postgres = _create_concept(
        store,
        "tool:postgresql",
        ConceptCategory.TOOL,
        "PostgreSQL",
    )
    assert _create_concept(
        store,
        "tool:postgresql",
        ConceptCategory.TOOL,
        "PostgreSQL",
    ) == postgres
    alias = store.add_alias(
        postgres.concept_id,
        alias_text="Postgres",
        provenance_kind=AliasProvenanceKind.MANUAL,
        provenance_reference="review:postgres-alias",
        reviewed_at=_NOW,
        review_note="Reviewed common product alias",
    )
    assert alias.normalized_alias == "postgres"
    assert store.add_alias(
        postgres.concept_id,
        alias_text="  POSTGRES ",
        provenance_kind=AliasProvenanceKind.MANUAL,
        provenance_reference="review:duplicate",
        reviewed_at=_NOW,
        review_note="Reviewed idempotent alias",
    ).id == alias.id

    other_tool = _create_concept(
        store,
        "tool:other-database",
        ConceptCategory.TOOL,
        "Other Database",
    )
    with pytest.raises(CanonicalRegistryError, match="another concept"):
        store.add_alias(
            other_tool.concept_id,
            alias_text="postgres",
            provenance_kind=AliasProvenanceKind.MANUAL,
            provenance_reference="review:collision",
            reviewed_at=_NOW,
            review_note="Reviewed collision example",
        )

    platform = _create_concept(
        store,
        "platform:postgresql-service",
        ConceptCategory.PLATFORM,
        "PostgreSQL Service",
    )
    assert store.add_alias(
        platform.concept_id,
        alias_text="Postgres",
        provenance_kind=AliasProvenanceKind.MANUAL,
        provenance_reference="review:category-specific",
        reviewed_at=_NOW,
        review_note="Reviewed category-specific alias",
    ).category == ConceptCategory.PLATFORM


def test_concept_supersession_is_same_category_and_history_is_immutable(
    tmp_path: Path,
) -> None:
    store = CanonicalRegistryStore(tmp_path / "registry.sqlite3")
    old = _create_concept(store, "tool:k8s-cli", ConceptCategory.TOOL, "K8s CLI")
    successor = _create_concept(
        store,
        "tool:kubernetes-cli",
        ConceptCategory.TOOL,
        "Kubernetes CLI",
    )
    language = _create_concept(
        store,
        "language:python",
        ConceptCategory.LANGUAGE,
        "Python",
    )

    with pytest.raises(CanonicalRegistryError, match="same category"):
        store.deprecate_concept(
            old.concept_id,
            successor_concept_id=language.concept_id,
            reviewed_at=_NOW,
            review_note="Reviewed invalid cross-category successor",
        )

    deprecated = store.deprecate_concept(
        old.concept_id,
        successor_concept_id=successor.concept_id,
        reviewed_at=_NOW,
        review_note="Reviewed Kubernetes naming replacement",
    )
    assert deprecated.status == "deprecated"
    assert deprecated.successor_concept_id == successor.concept_id
    assert store.list_concepts() == (language, successor)
    with pytest.raises(CanonicalRegistryError, match="history is immutable"):
        store.deprecate_concept(
            old.concept_id,
            successor_concept_id=None,
            reviewed_at=_NOW,
            review_note="Attempted history rewrite",
        )


def test_current_accepted_p16_claim_mapping_preserves_exact_provenance(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation_service, analysis_id = _seed_analysis(database_path)
    store = CanonicalRegistryStore(database_path)
    concept = _create_concept(
        store,
        "language:python",
        ConceptCategory.LANGUAGE,
        "Python",
    )
    service = CanonicalRegistryService(
        registry_store=store,
        analysis_store=AnalysisStore(database_path),
        translation_service=translation_service,
        analysis_model="analysis-model",
    )

    mapping = service.record_current_claim_mapping(
        "registry1",
        claim_kind=ClaimKind.REQUIREMENT,
        claim_index=0,
        disposition=MappingDisposition.MAPPED,
        canonical_concept_id=concept.concept_id,
        reviewed_at=_NOW,
        review_note="Reviewed exact Python requirement mapping",
    )

    assert mapping.analysis_artifact_id == analysis_id
    assert mapping.source_job_id == "registry1"
    assert mapping.translation_artifact_id > 0
    assert mapping.source_text == "Python"
    assert mapping.normalized_source_text == "python"
    assert mapping.canonical_concept_id == "language:python"
    assert service.record_current_claim_mapping(
        "registry1",
        claim_kind=ClaimKind.REQUIREMENT,
        claim_index=0,
        disposition=MappingDisposition.MAPPED,
        canonical_concept_id=concept.concept_id,
        reviewed_at=_NOW,
        review_note="Reviewed exact Python requirement mapping",
    ).id == mapping.id
    with pytest.raises(CanonicalRegistryError, match="already has a reviewed mapping"):
        service.record_current_claim_mapping(
            "registry1",
            claim_kind=ClaimKind.REQUIREMENT,
            claim_index=0,
            disposition=MappingDisposition.UNMAPPED,
            canonical_concept_id=None,
            reviewed_at=_NOW,
            review_note="Attempted immutable decision rewrite",
        )


def test_mapping_supports_explicit_unmapped_and_responsibility_category(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation_service, _analysis_id = _seed_analysis(database_path)
    store = CanonicalRegistryStore(database_path)
    language = _create_concept(
        store,
        "language:python",
        ConceptCategory.LANGUAGE,
        "Python",
    )
    responsibility = _create_concept(
        store,
        "responsibility:build-software-services",
        ConceptCategory.RESPONSIBILITY,
        "Build software services",
    )
    service = CanonicalRegistryService(
        registry_store=store,
        analysis_store=AnalysisStore(database_path),
        translation_service=translation_service,
        analysis_model="analysis-model",
    )

    unmapped = service.record_current_claim_mapping(
        "registry1",
        claim_kind=ClaimKind.REQUIREMENT,
        claim_index=1,
        disposition=MappingDisposition.UNMAPPED,
        canonical_concept_id=None,
        reviewed_at=_NOW,
        review_note="Reviewed claim remains explicitly unmapped",
    )
    rejected = service.record_current_claim_mapping(
        "registry1",
        claim_kind=ClaimKind.REQUIREMENT,
        claim_index=2,
        disposition=MappingDisposition.REJECTED,
        canonical_concept_id=None,
        reviewed_at=_NOW,
        review_note="Reviewed claim is unsuitable for canonical mapping",
    )
    assert unmapped.disposition == "unmapped"
    assert unmapped.canonical_concept_id is None
    assert rejected.disposition == "rejected"
    assert rejected.canonical_concept_id is None

    with pytest.raises(CanonicalRegistryError, match="responsibility concept"):
        service.record_current_claim_mapping(
            "registry1",
            claim_kind=ClaimKind.RESPONSIBILITY,
            claim_index=0,
            disposition=MappingDisposition.MAPPED,
            canonical_concept_id=language.concept_id,
            reviewed_at=_NOW,
            review_note="Reviewed invalid responsibility category",
        )
    mapped = service.record_current_claim_mapping(
        "registry1",
        claim_kind=ClaimKind.RESPONSIBILITY,
        claim_index=0,
        disposition=MappingDisposition.MAPPED,
        canonical_concept_id=responsibility.concept_id,
        reviewed_at=_NOW,
        review_note="Reviewed service-building responsibility",
    )
    assert mapped.source_text == "Build Python services"


def test_pending_or_stale_p16_cannot_receive_current_mapping(tmp_path: Path) -> None:
    database_path = tmp_path / "jobhunter.sqlite3"
    translation_service, _analysis_id = _seed_analysis(
        database_path,
        job_id="pending1",
        review_status=SEMANTIC_REVIEW_PENDING,
    )
    store = CanonicalRegistryStore(database_path)
    concept = _create_concept(
        store,
        "language:python",
        ConceptCategory.LANGUAGE,
        "Python",
    )
    service = CanonicalRegistryService(
        registry_store=store,
        analysis_store=AnalysisStore(database_path),
        translation_service=translation_service,
        analysis_model="analysis-model",
    )
    with pytest.raises(CanonicalRegistryError, match="no accepted English P1.6"):
        service.record_current_claim_mapping(
            "pending1",
            claim_kind=ClaimKind.REQUIREMENT,
            claim_index=0,
            disposition=MappingDisposition.MAPPED,
            canonical_concept_id=concept.concept_id,
            reviewed_at=_NOW,
            review_note="Reviewed pending artifact boundary",
        )

    stale_service = CanonicalRegistryService(
        registry_store=store,
        analysis_store=AnalysisStore(database_path),
        translation_service=SimpleNamespace(
            current_artifact=lambda _job_id: SimpleNamespace(
                id=999,
                job_detail_version_id=1,
            )
        ),
        analysis_model="analysis-model",
    )
    with pytest.raises(CanonicalRegistryError, match="no accepted English P1.6"):
        stale_service.record_current_claim_mapping(
            "pending1",
            claim_kind=ClaimKind.REQUIREMENT,
            claim_index=0,
            disposition=MappingDisposition.MAPPED,
            canonical_concept_id=concept.concept_id,
            reviewed_at=_NOW,
            review_note="Reviewed stale translation boundary",
        )
