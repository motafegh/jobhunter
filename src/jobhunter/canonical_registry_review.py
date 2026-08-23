"""Neutral read models for manual canonical-registry review surfaces.

This module is intentionally UI-agnostic. Both CLI and browser review paths consume the
same accepted/current P1.6 claim reader and exact registry persistence state.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.canonical_registry import (
    CanonicalAlias,
    CanonicalRegistryError,
    CanonicalRegistryStore,
    ClaimKind,
    JobClaimMapping,
    MappingDisposition,
)
from jobhunter.config import Settings
from jobhunter.translation_service import TranslationService, build_translation_service


@dataclass(frozen=True, slots=True)
class CanonicalClaimReviewItem:
    """One exact accepted/current P1.6 claim and its immutable review state."""

    analysis_artifact_id: int
    source_job_id: str
    job_detail_version_id: int
    translation_artifact_id: int
    claim_kind: str
    claim_index: int
    source_text: str
    evidence: str | None
    concept_type: str | None
    strength: str | None
    depth_signal: str | None
    mapping: JobClaimMapping | None

    @property
    def mapping_state(self) -> str:
        return self.mapping.disposition if self.mapping is not None else "pending"


@dataclass(frozen=True, slots=True)
class CanonicalConceptMappingReviewItem:
    """One reviewed mapping attached to a canonical concept plus currentness."""

    mapping: JobClaimMapping
    current: bool


def list_concept_aliases(
    database_path: Path,
    registry_store: CanonicalRegistryStore,
    concept_id: str,
    *,
    include_deprecated: bool = False,
) -> tuple[CanonicalAlias, ...]:
    """Return reviewed aliases for one concept in stable review order."""

    registry_store.initialize()
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT id
            FROM canonical_concept_aliases
            WHERE concept_id = ?
              AND (? = 1 OR status = 'active')
            ORDER BY status, normalized_alias, id
            """,
            (concept_id, int(include_deprecated)),
        ).fetchall()
    finally:
        connection.close()

    aliases: list[CanonicalAlias] = []
    for row in rows:
        alias = registry_store.alias_by_id(int(row["id"]))
        if alias is not None:
            aliases.append(alias)
    return tuple(aliases)


class CanonicalRegistryReviewReader:
    """Read reviewed registry state without weakening the accepted P1.6 boundary."""

    def __init__(
        self,
        *,
        database_path: Path,
        registry_store: CanonicalRegistryStore,
        analysis_store: AnalysisStore,
        translation_service: TranslationService,
        analysis_model: str,
    ) -> None:
        if not analysis_model.strip():
            raise ValueError("A concrete current analysis model is required")
        self._database_path = database_path
        self._registry_store = registry_store
        self._analysis_store = analysis_store
        self._translation_service = translation_service
        self._analysis_model = analysis_model.strip()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def aliases_for_concept(
        self,
        concept_id: str,
        *,
        include_deprecated: bool = False,
    ) -> tuple[CanonicalAlias, ...]:
        return list_concept_aliases(
            self._database_path,
            self._registry_store,
            concept_id,
            include_deprecated=include_deprecated,
        )

    def mapping_for_claim(
        self,
        *,
        analysis_artifact_id: int,
        claim_kind: ClaimKind | str,
        claim_index: int,
    ) -> JobClaimMapping | None:
        """Return the immutable decision for one exact artifact claim, if reviewed."""

        kind = ClaimKind(claim_kind).value
        self._registry_store.initialize()
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id
                FROM job_claim_canonical_mappings
                WHERE analysis_artifact_id = ?
                  AND claim_kind = ?
                  AND claim_index = ?
                LIMIT 1
                """,
                (analysis_artifact_id, kind, claim_index),
            ).fetchone()
        if row is None:
            return None
        return self._registry_store.mapping_by_id(int(row["id"]))

    def list_current_claims(
        self,
        *,
        source_job_id: str | None = None,
        claim_kind: ClaimKind | str | None = None,
        mapping_state: str = "all",
        limit: int = 500,
    ) -> tuple[CanonicalClaimReviewItem, ...]:
        """List accepted/current English P1.6 claims and their mapping state.

        Currentness is checked twice: the analysis must belong to the current source
        detail and frozen v20/v5 contract, and its translation dependency must equal
        the translation service's configured current English projection.
        """

        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        allowed_states = {"all", "pending", *(item.value for item in MappingDisposition)}
        if mapping_state not in allowed_states:
            raise ValueError(
                "mapping_state must be all, pending, mapped, unmapped, or rejected"
            )
        kind_filter = ClaimKind(claim_kind) if claim_kind is not None else None
        job_filter = source_job_id.strip() if source_job_id is not None else None
        if job_filter == "":
            raise ValueError("source_job_id must not be empty")

        artifacts = self._analysis_store.list_current(
            limit=5000,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            accepted_only=True,
        )
        items: list[CanonicalClaimReviewItem] = []
        for artifact in artifacts:
            if job_filter is not None and artifact.source_job_id != job_filter:
                continue
            if not self._is_current_translation_dependency(artifact):
                continue
            for kind in ClaimKind:
                if kind_filter is not None and kind != kind_filter:
                    continue
                for item in self._claim_items(artifact, kind):
                    if mapping_state != "all" and item.mapping_state != mapping_state:
                        continue
                    items.append(item)
                    if len(items) >= limit:
                        return tuple(items)
        return tuple(items)

    def concept_mappings(
        self,
        concept_id: str,
        *,
        limit: int = 500,
    ) -> tuple[CanonicalConceptMappingReviewItem, ...]:
        """List reviewed mappings for one concept and derive whether each is current."""

        if not 1 <= limit <= 5000:
            raise ValueError("limit must be between 1 and 5000")
        if self._registry_store.get_concept(concept_id) is None:
            raise LookupError(f"Unknown canonical concept {concept_id!r}")
        self._registry_store.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id
                FROM job_claim_canonical_mappings
                WHERE canonical_concept_id = ? AND disposition = 'mapped'
                ORDER BY reviewed_at DESC, id DESC
                LIMIT ?
                """,
                (concept_id, limit),
            ).fetchall()

        items: list[CanonicalConceptMappingReviewItem] = []
        for row in rows:
            mapping = self._registry_store.mapping_by_id(int(row["id"]))
            if mapping is None:
                continue
            items.append(
                CanonicalConceptMappingReviewItem(
                    mapping=mapping,
                    current=self._mapping_is_current(mapping),
                )
            )
        return tuple(items)

    def _mapping_is_current(self, mapping: JobClaimMapping) -> bool:
        current_translation = self._translation_service.current_artifact(mapping.source_job_id)
        if (
            current_translation is None
            or current_translation.id != mapping.translation_artifact_id
        ):
            return False
        current_analysis = self._analysis_store.latest_current(
            mapping.source_job_id,
            model=self._analysis_model,
            prompt_version=ENGLISH_PROMPT_VERSION,
            schema_version=ENGLISH_ANALYSIS_SCHEMA_VERSION,
            accepted_only=True,
            translation_artifact_id=current_translation.id,
            require_translation_dependency=True,
        )
        return current_analysis is not None and current_analysis.id == mapping.analysis_artifact_id

    def _is_current_translation_dependency(self, artifact: AnalysisArtifact) -> bool:
        if artifact.translation_artifact_id is None:
            return False
        current = self._translation_service.current_artifact(artifact.source_job_id)
        return current is not None and current.id == artifact.translation_artifact_id

    def _claim_items(
        self,
        artifact: AnalysisArtifact,
        kind: ClaimKind,
    ) -> tuple[CanonicalClaimReviewItem, ...]:
        field = "requirements" if kind == ClaimKind.REQUIREMENT else "responsibilities"
        values = artifact.analysis.get(field) or []
        if not isinstance(values, list):
            raise CanonicalRegistryError(
                f"Accepted P1.6 artifact {artifact.id} has invalid {field}"
            )

        items: list[CanonicalClaimReviewItem] = []
        for index, claim in enumerate(values):
            if not isinstance(claim, dict):
                raise CanonicalRegistryError(
                    f"Accepted P1.6 artifact {artifact.id} has invalid {kind.value} claim"
                )
            source_key = "concept" if kind == ClaimKind.REQUIREMENT else "statement"
            raw_text = claim.get(source_key)
            if not isinstance(raw_text, str) or not raw_text.strip():
                raise CanonicalRegistryError(
                    f"Accepted P1.6 artifact {artifact.id} has empty {kind.value} text"
                )
            mapping = self.mapping_for_claim(
                analysis_artifact_id=artifact.id,
                claim_kind=kind,
                claim_index=index,
            )
            items.append(
                CanonicalClaimReviewItem(
                    analysis_artifact_id=artifact.id,
                    source_job_id=artifact.source_job_id,
                    job_detail_version_id=artifact.job_detail_version_id,
                    translation_artifact_id=artifact.translation_artifact_id,
                    claim_kind=kind.value,
                    claim_index=index,
                    source_text=" ".join(raw_text.split()),
                    evidence=_optional_claim_text(claim.get("evidence")),
                    concept_type=_optional_claim_text(claim.get("concept_type")),
                    strength=_optional_claim_text(
                        claim.get("strength") or claim.get("requirement_strength")
                    ),
                    depth_signal=_optional_claim_text(claim.get("depth_signal")),
                    mapping=mapping,
                )
            )
        return tuple(items)


def build_canonical_registry_review_reader(
    settings: Settings,
) -> CanonicalRegistryReviewReader:
    """Build the UI-neutral reader for the configured current P1.6 contract."""

    analysis_model = settings.effective_analysis_lm_studio_model()
    if not analysis_model:
        raise ValueError("No analysis model is configured for current English P1.6")
    store = CanonicalRegistryStore(settings.database_path)
    return CanonicalRegistryReviewReader(
        database_path=settings.database_path,
        registry_store=store,
        analysis_store=AnalysisStore(settings.database_path),
        translation_service=build_translation_service(settings),
        analysis_model=analysis_model,
    )


def _optional_claim_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = " ".join(value.split())
    return normalized or None
