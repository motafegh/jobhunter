"""Reviewed Phase-2 canonical concepts and accepted P1.6 claim mappings."""

from __future__ import annotations

import re
import sqlite3
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.config import Settings
from jobhunter.translation_service import TranslationService, build_translation_service

CANONICAL_REGISTRY_CONTRACT_VERSION = "jobhunter-canonical-concept-registry-v1"


class ConceptCategory(StrEnum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    TOOL = "tool"
    PLATFORM = "platform"
    SKILL = "skill"
    KNOWLEDGE_AREA = "knowledge_area"
    PRACTICE = "practice"
    DOMAIN = "domain"
    EXPERIENCE_SIGNAL = "experience_signal"
    EDUCATION_CREDENTIAL = "education_credential"
    RESPONSIBILITY = "responsibility"
    DELIVERABLE = "deliverable"


class ConceptStatus(StrEnum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class AliasStatus(StrEnum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class MappingDisposition(StrEnum):
    MAPPED = "mapped"
    UNMAPPED = "unmapped"
    REJECTED = "rejected"


class ClaimKind(StrEnum):
    REQUIREMENT = "requirement"
    RESPONSIBILITY = "responsibility"


class AliasProvenanceKind(StrEnum):
    MANUAL = "manual"
    ACCEPTED_P16_CLAIM = "accepted_p16_claim"
    EXTERNAL_STANDARD = "external_standard"


class CanonicalRegistryError(ValueError):
    """Raised when a registry mutation violates the reviewed contract."""


@dataclass(frozen=True, slots=True)
class CanonicalConcept:
    concept_id: str
    category: str
    preferred_label: str
    normalized_preferred_label: str
    description: str | None
    status: str
    successor_concept_id: str | None
    created_at: str
    updated_at: str
    review_note: str


@dataclass(frozen=True, slots=True)
class CanonicalAlias:
    id: int
    concept_id: str
    category: str
    alias_text: str
    normalized_alias: str
    provenance_kind: str
    provenance_reference: str
    status: str
    reviewed_at: str
    review_note: str


@dataclass(frozen=True, slots=True)
class JobClaimMapping:
    id: int
    analysis_artifact_id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int
    claim_kind: str
    claim_index: int
    source_text: str
    normalized_source_text: str
    canonical_concept_id: str | None
    disposition: str
    reviewed_at: str
    review_note: str


def normalize_registry_text(value: str) -> str:
    """Normalize lookup text without erasing punctuation or source wording."""

    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def validate_concept_id(concept_id: str, category: ConceptCategory | str) -> str:
    """Require a stable explicit ``category:slug`` identifier."""

    category_value = ConceptCategory(category).value
    normalized = concept_id.strip()
    pattern = rf"{re.escape(category_value)}:[a-z0-9]+(?:-[a-z0-9]+)*"
    if not re.fullmatch(pattern, normalized):
        raise CanonicalRegistryError(
            f"concept_id must match {category_value}:lowercase-kebab-slug"
        )
    return normalized


class CanonicalRegistryStore:
    """Persist manually reviewed concepts, aliases, and P1.6 claim mappings."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        return connection

    def initialize(self) -> None:
        AnalysisStore(self._database_path).initialize()
        categories = ", ".join(f"'{item.value}'" for item in ConceptCategory)
        with self._connect() as connection:
            connection.executescript(
                f"""
                CREATE TABLE IF NOT EXISTS canonical_concepts (
                    concept_id TEXT PRIMARY KEY,
                    category TEXT NOT NULL CHECK(category IN ({categories})),
                    preferred_label TEXT NOT NULL,
                    normalized_preferred_label TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL CHECK(status IN ('active', 'deprecated')),
                    successor_concept_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    review_note TEXT NOT NULL,
                    FOREIGN KEY(successor_concept_id) REFERENCES canonical_concepts(concept_id),
                    CHECK(successor_concept_id IS NULL OR successor_concept_id != concept_id),
                    CHECK(status = 'deprecated' OR successor_concept_id IS NULL),
                    UNIQUE(category, normalized_preferred_label),
                    UNIQUE(concept_id, category)
                );

                CREATE TABLE IF NOT EXISTS canonical_concept_aliases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    concept_id TEXT NOT NULL,
                    category TEXT NOT NULL CHECK(category IN ({categories})),
                    alias_text TEXT NOT NULL,
                    normalized_alias TEXT NOT NULL,
                    provenance_kind TEXT NOT NULL CHECK(
                        provenance_kind IN (
                            'manual', 'accepted_p16_claim', 'external_standard'
                        )
                    ),
                    provenance_reference TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('active', 'deprecated')),
                    reviewed_at TEXT NOT NULL,
                    review_note TEXT NOT NULL,
                    FOREIGN KEY(concept_id, category)
                        REFERENCES canonical_concepts(concept_id, category),
                    UNIQUE(category, normalized_alias)
                );

                CREATE TABLE IF NOT EXISTS job_claim_canonical_mappings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_artifact_id INTEGER NOT NULL,
                    source_job_id TEXT NOT NULL,
                    job_detail_version_id INTEGER NOT NULL,
                    translation_artifact_id INTEGER NOT NULL,
                    claim_kind TEXT NOT NULL CHECK(
                        claim_kind IN ('requirement', 'responsibility')
                    ),
                    claim_index INTEGER NOT NULL CHECK(claim_index >= 0),
                    source_text TEXT NOT NULL,
                    normalized_source_text TEXT NOT NULL,
                    canonical_concept_id TEXT,
                    disposition TEXT NOT NULL CHECK(
                        disposition IN ('mapped', 'unmapped', 'rejected')
                    ),
                    reviewed_at TEXT NOT NULL,
                    review_note TEXT NOT NULL,
                    FOREIGN KEY(analysis_artifact_id) REFERENCES job_analysis_artifacts(id),
                    FOREIGN KEY(job_detail_version_id) REFERENCES job_detail_versions(id),
                    FOREIGN KEY(translation_artifact_id)
                        REFERENCES job_translation_artifacts(id),
                    FOREIGN KEY(canonical_concept_id)
                        REFERENCES canonical_concepts(concept_id),
                    CHECK(
                        (disposition = 'mapped' AND canonical_concept_id IS NOT NULL)
                        OR
                        (disposition != 'mapped' AND canonical_concept_id IS NULL)
                    ),
                    UNIQUE(analysis_artifact_id, claim_kind, claim_index)
                );

                CREATE INDEX IF NOT EXISTS idx_canonical_concepts_category_status
                ON canonical_concepts(category, status, preferred_label);
                CREATE INDEX IF NOT EXISTS idx_canonical_alias_lookup
                ON canonical_concept_aliases(category, normalized_alias, status);
                CREATE INDEX IF NOT EXISTS idx_job_claim_mapping_concept
                ON job_claim_canonical_mappings(canonical_concept_id, disposition);
                CREATE INDEX IF NOT EXISTS idx_job_claim_mapping_source
                ON job_claim_canonical_mappings(source_job_id, analysis_artifact_id);
                """
            )

    def create_concept(
        self,
        *,
        concept_id: str,
        category: ConceptCategory | str,
        preferred_label: str,
        description: str | None,
        reviewed_at: datetime,
        review_note: str,
    ) -> CanonicalConcept:
        category_value = ConceptCategory(category).value
        concept_id = validate_concept_id(concept_id, category_value)
        label = _bounded_text(preferred_label, name="preferred_label", maximum=120)
        normalized_label = normalize_registry_text(label)
        description_value = _optional_bounded_text(
            description,
            name="description",
            maximum=1000,
        )
        note = _review_note(review_note)
        timestamp = reviewed_at.isoformat()
        self.initialize()
        existing = self.get_concept(concept_id)
        if existing is not None:
            expected = (
                category_value,
                label,
                normalized_label,
                description_value,
            )
            actual = (
                existing.category,
                existing.preferred_label,
                existing.normalized_preferred_label,
                existing.description,
            )
            if actual == expected:
                return existing
            raise CanonicalRegistryError(
                f"concept_id {concept_id!r} already exists with different reviewed content"
            )

        with self._connect() as connection:
            collision = connection.execute(
                """
                SELECT concept_id FROM canonical_concept_aliases
                WHERE category = ? AND normalized_alias = ? AND status = 'active'
                """,
                (category_value, normalized_label),
            ).fetchone()
            if collision is not None:
                raise CanonicalRegistryError(
                    "preferred label collides with an active reviewed alias in this category"
                )
            try:
                connection.execute(
                    """
                    INSERT INTO canonical_concepts(
                        concept_id, category, preferred_label,
                        normalized_preferred_label, description, status,
                        successor_concept_id, created_at, updated_at, review_note
                    ) VALUES (?, ?, ?, ?, ?, 'active', NULL, ?, ?, ?)
                    """,
                    (
                        concept_id,
                        category_value,
                        label,
                        normalized_label,
                        description_value,
                        timestamp,
                        timestamp,
                        note,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise CanonicalRegistryError(
                    "preferred label already belongs to another concept in this category"
                ) from exc
        result = self.get_concept(concept_id)
        if result is None:
            raise RuntimeError("Canonical concept disappeared after persistence")
        return result

    def get_concept(self, concept_id: str) -> CanonicalConcept | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM canonical_concepts WHERE concept_id = ?",
                (concept_id,),
            ).fetchone()
        return _concept(row) if row is not None else None

    def list_concepts(
        self,
        *,
        category: ConceptCategory | str | None = None,
        include_deprecated: bool = False,
        limit: int = 500,
    ) -> tuple[CanonicalConcept, ...]:
        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        category_value = ConceptCategory(category).value if category is not None else None
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM canonical_concepts
                WHERE (? IS NULL OR category = ?)
                  AND (? = 1 OR status = 'active')
                ORDER BY category, preferred_label COLLATE NOCASE, concept_id
                LIMIT ?
                """,
                (category_value, category_value, int(include_deprecated), limit),
            ).fetchall()
        return tuple(_concept(row) for row in rows)

    def deprecate_concept(
        self,
        concept_id: str,
        *,
        successor_concept_id: str | None,
        reviewed_at: datetime,
        review_note: str,
    ) -> CanonicalConcept:
        note = _review_note(review_note)
        self.initialize()
        concept = self.get_concept(concept_id)
        if concept is None:
            raise CanonicalRegistryError(f"Unknown canonical concept {concept_id!r}")
        successor = None
        if successor_concept_id is not None:
            successor = self.get_concept(successor_concept_id)
            if successor is None or successor.status != ConceptStatus.ACTIVE:
                raise CanonicalRegistryError("successor concept must exist and remain active")
            if successor.category != concept.category:
                raise CanonicalRegistryError("successor concept must use the same category")
            if successor.concept_id == concept.concept_id:
                raise CanonicalRegistryError("concept cannot supersede itself")
        if concept.status == ConceptStatus.DEPRECATED:
            if concept.successor_concept_id == successor_concept_id:
                return concept
            raise CanonicalRegistryError("deprecated concept history is immutable")
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE canonical_concepts
                SET status = 'deprecated', successor_concept_id = ?,
                    updated_at = ?, review_note = ?
                WHERE concept_id = ?
                """,
                (successor_concept_id, reviewed_at.isoformat(), note, concept_id),
            )
        result = self.get_concept(concept_id)
        if result is None:
            raise RuntimeError("Canonical concept disappeared after deprecation")
        return result

    def add_alias(
        self,
        concept_id: str,
        *,
        alias_text: str,
        provenance_kind: AliasProvenanceKind | str,
        provenance_reference: str,
        reviewed_at: datetime,
        review_note: str,
    ) -> CanonicalAlias:
        alias = _bounded_text(alias_text, name="alias_text", maximum=200)
        normalized_alias = normalize_registry_text(alias)
        provenance = AliasProvenanceKind(provenance_kind).value
        reference = _bounded_text(
            provenance_reference,
            name="provenance_reference",
            maximum=500,
        )
        note = _review_note(review_note)
        self.initialize()
        concept = self.get_concept(concept_id)
        if concept is None or concept.status != ConceptStatus.ACTIVE:
            raise CanonicalRegistryError("aliases require an active canonical concept")
        with self._connect() as connection:
            preferred_collision = connection.execute(
                """
                SELECT concept_id FROM canonical_concepts
                WHERE category = ? AND normalized_preferred_label = ?
                """,
                (concept.category, normalized_alias),
            ).fetchone()
            if (
                preferred_collision is not None
                and str(preferred_collision["concept_id"]) != concept_id
            ):
                raise CanonicalRegistryError(
                    "alias collides with another preferred label in this category"
                )
            existing = connection.execute(
                """
                SELECT * FROM canonical_concept_aliases
                WHERE category = ? AND normalized_alias = ?
                """,
                (concept.category, normalized_alias),
            ).fetchone()
            if existing is not None:
                result = _alias(existing)
                if result.concept_id == concept_id and result.status == AliasStatus.ACTIVE:
                    return result
                raise CanonicalRegistryError(
                    "alias already maps to another concept in this category"
                )
            cursor = connection.execute(
                """
                INSERT INTO canonical_concept_aliases(
                    concept_id, category, alias_text, normalized_alias,
                    provenance_kind, provenance_reference, status,
                    reviewed_at, review_note
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    concept_id,
                    concept.category,
                    alias,
                    normalized_alias,
                    provenance,
                    reference,
                    reviewed_at.isoformat(),
                    note,
                ),
            )
            alias_id = int(cursor.lastrowid)
        result = self.alias_by_id(alias_id)
        if result is None:
            raise RuntimeError("Canonical alias disappeared after persistence")
        return result

    def alias_by_id(self, alias_id: int) -> CanonicalAlias | None:
        if alias_id <= 0:
            raise ValueError("alias_id must be greater than zero")
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM canonical_concept_aliases WHERE id = ?",
                (alias_id,),
            ).fetchone()
        return _alias(row) if row is not None else None

    def record_claim_mapping(
        self,
        *,
        analysis_artifact_id: int,
        claim_kind: ClaimKind | str,
        claim_index: int,
        disposition: MappingDisposition | str,
        canonical_concept_id: str | None,
        reviewed_at: datetime,
        review_note: str,
    ) -> JobClaimMapping:
        if claim_index < 0:
            raise CanonicalRegistryError("claim_index must not be negative")
        kind = ClaimKind(claim_kind)
        disposition_value = MappingDisposition(disposition)
        note = _review_note(review_note)
        artifact = AnalysisStore(self._database_path).artifact_by_id(analysis_artifact_id)
        if artifact is None:
            raise CanonicalRegistryError("Unknown P1.6 analysis artifact")
        _validate_mapping_artifact(artifact)
        source_text = _claim_text(artifact, kind, claim_index)

        concept = None
        if disposition_value == MappingDisposition.MAPPED:
            if canonical_concept_id is None:
                raise CanonicalRegistryError("mapped disposition requires a canonical concept")
            concept = self.get_concept(canonical_concept_id)
            if concept is None or concept.status != ConceptStatus.ACTIVE:
                raise CanonicalRegistryError("mapping requires an active canonical concept")
            if kind == ClaimKind.RESPONSIBILITY and (
                concept.category != ConceptCategory.RESPONSIBILITY
            ):
                raise CanonicalRegistryError(
                    "responsibility claims require a responsibility concept"
                )
        elif canonical_concept_id is not None:
            raise CanonicalRegistryError(
                "unmapped/rejected dispositions cannot reference a canonical concept"
            )

        self.initialize()
        with self._connect() as connection:
            existing = connection.execute(
                """
                SELECT * FROM job_claim_canonical_mappings
                WHERE analysis_artifact_id = ? AND claim_kind = ? AND claim_index = ?
                """,
                (analysis_artifact_id, kind.value, claim_index),
            ).fetchone()
            if existing is not None:
                result = _mapping(existing)
                if (
                    result.disposition == disposition_value
                    and result.canonical_concept_id == canonical_concept_id
                ):
                    return result
                raise CanonicalRegistryError(
                    "this immutable P1.6 claim already has a reviewed mapping decision"
                )
            cursor = connection.execute(
                """
                INSERT INTO job_claim_canonical_mappings(
                    analysis_artifact_id, source_job_id, job_detail_version_id,
                    translation_artifact_id, claim_kind, claim_index, source_text,
                    normalized_source_text, canonical_concept_id, disposition,
                    reviewed_at, review_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact.id,
                    artifact.source_job_id,
                    artifact.job_detail_version_id,
                    artifact.translation_artifact_id,
                    kind.value,
                    claim_index,
                    source_text,
                    normalize_registry_text(source_text),
                    canonical_concept_id,
                    disposition_value.value,
                    reviewed_at.isoformat(),
                    note,
                ),
            )
            mapping_id = int(cursor.lastrowid)
        result = self.mapping_by_id(mapping_id)
        if result is None:
            raise RuntimeError("Canonical claim mapping disappeared after persistence")
        return result

    def mapping_by_id(self, mapping_id: int) -> JobClaimMapping | None:
        if mapping_id <= 0:
            raise ValueError("mapping_id must be greater than zero")
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM job_claim_canonical_mappings WHERE id = ?",
                (mapping_id,),
            ).fetchone()
        return _mapping(row) if row is not None else None


class CanonicalRegistryService:
    """Apply mapping decisions only to the exact configured accepted P1.6 chain."""

    def __init__(
        self,
        *,
        registry_store: CanonicalRegistryStore,
        analysis_store: AnalysisStore,
        translation_service: TranslationService,
        analysis_model: str,
    ) -> None:
        if not analysis_model.strip():
            raise ValueError("A concrete current analysis model is required")
        self._registry_store = registry_store
        self._analysis_store = analysis_store
        self._translation_service = translation_service
        self._analysis_model = analysis_model.strip()

    def record_current_claim_mapping(
        self,
        source_job_id: str,
        *,
        claim_kind: ClaimKind | str,
        claim_index: int,
        disposition: MappingDisposition | str,
        canonical_concept_id: str | None,
        reviewed_at: datetime,
        review_note: str,
    ) -> JobClaimMapping:
        translation = self._translation_service.current_artifact(source_job_id)
        if translation is None:
            raise CanonicalRegistryError("Job has no configured current English projection")
        analysis = self._analysis_store.find_artifact(
            job_detail_version_id=translation.job_detail_version_id,
            translation_artifact_id=translation.id,
            require_translation_dependency=True,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
        )
        if analysis is None or analysis.semantic_review_status != "accepted":
            raise CanonicalRegistryError(
                "Job has no accepted English P1.6 artifact on the configured translation"
            )
        return self._registry_store.record_claim_mapping(
            analysis_artifact_id=analysis.id,
            claim_kind=claim_kind,
            claim_index=claim_index,
            disposition=disposition,
            canonical_concept_id=canonical_concept_id,
            reviewed_at=reviewed_at,
            review_note=review_note,
        )


def build_canonical_registry_service(settings: Settings) -> CanonicalRegistryService:
    """Build the P2.1 reviewed-mapping boundary on configured current P1.6."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for current English P1.6")
    return CanonicalRegistryService(
        registry_store=CanonicalRegistryStore(settings.database_path),
        analysis_store=AnalysisStore(settings.database_path),
        translation_service=build_translation_service(settings),
        analysis_model=analysis_model,
    )


def _validate_mapping_artifact(artifact: AnalysisArtifact) -> None:
    if artifact.prompt_version != ENGLISH_PROMPT_VERSION or (
        artifact.schema_version != ENGLISH_ANALYSIS_SCHEMA_VERSION
    ):
        raise CanonicalRegistryError("mapping input must use the frozen English P1.6 contract")
    if artifact.translation_artifact_id is None:
        raise CanonicalRegistryError("mapping input must reference an English projection")
    if artifact.semantic_review_status != "accepted":
        raise CanonicalRegistryError("mapping input must be semantically accepted")


def _claim_text(
    artifact: AnalysisArtifact,
    kind: ClaimKind,
    claim_index: int,
) -> str:
    field = "requirements" if kind == ClaimKind.REQUIREMENT else "responsibilities"
    values = artifact.analysis.get(field) or []
    if not isinstance(values, list) or claim_index >= len(values):
        raise CanonicalRegistryError(
            f"{kind.value} claim index {claim_index} is outside artifact {artifact.id}"
        )
    claim = values[claim_index]
    if not isinstance(claim, dict):
        raise CanonicalRegistryError("P1.6 claim must be an object")
    key = "concept" if kind == ClaimKind.REQUIREMENT else "statement"
    text = claim.get(key)
    if not isinstance(text, str) or not text.strip():
        raise CanonicalRegistryError(f"P1.6 {kind.value} has no canonicalizable {key}")
    return " ".join(text.split())


def _bounded_text(value: str, *, name: str, maximum: int) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise CanonicalRegistryError(f"{name} must not be empty")
    if len(normalized) > maximum:
        raise CanonicalRegistryError(f"{name} must be at most {maximum} characters")
    return normalized


def _optional_bounded_text(
    value: str | None,
    *,
    name: str,
    maximum: int,
) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.split())
    if not normalized:
        return None
    if len(normalized) > maximum:
        raise CanonicalRegistryError(f"{name} must be at most {maximum} characters")
    return normalized


def _review_note(value: str) -> str:
    note = _bounded_text(value, name="review_note", maximum=1000)
    if len(note) < 8:
        raise CanonicalRegistryError("review_note must contain at least 8 characters")
    return note


def _concept(row: sqlite3.Row) -> CanonicalConcept:
    return CanonicalConcept(
        concept_id=str(row["concept_id"]),
        category=str(row["category"]),
        preferred_label=str(row["preferred_label"]),
        normalized_preferred_label=str(row["normalized_preferred_label"]),
        description=str(row["description"]) if row["description"] is not None else None,
        status=str(row["status"]),
        successor_concept_id=(
            str(row["successor_concept_id"])
            if row["successor_concept_id"] is not None
            else None
        ),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
        review_note=str(row["review_note"]),
    )


def _alias(row: sqlite3.Row) -> CanonicalAlias:
    return CanonicalAlias(
        id=int(row["id"]),
        concept_id=str(row["concept_id"]),
        category=str(row["category"]),
        alias_text=str(row["alias_text"]),
        normalized_alias=str(row["normalized_alias"]),
        provenance_kind=str(row["provenance_kind"]),
        provenance_reference=str(row["provenance_reference"]),
        status=str(row["status"]),
        reviewed_at=str(row["reviewed_at"]),
        review_note=str(row["review_note"]),
    )


def _mapping(row: sqlite3.Row) -> JobClaimMapping:
    return JobClaimMapping(
        id=int(row["id"]),
        analysis_artifact_id=int(row["analysis_artifact_id"]),
        source_job_id=str(row["source_job_id"]),
        job_detail_version_id=int(row["job_detail_version_id"]),
        translation_artifact_id=int(row["translation_artifact_id"]),
        claim_kind=str(row["claim_kind"]),
        claim_index=int(row["claim_index"]),
        source_text=str(row["source_text"]),
        normalized_source_text=str(row["normalized_source_text"]),
        canonical_concept_id=(
            str(row["canonical_concept_id"])
            if row["canonical_concept_id"] is not None
            else None
        ),
        disposition=str(row["disposition"]),
        reviewed_at=str(row["reviewed_at"]),
        review_note=str(row["review_note"]),
    )
