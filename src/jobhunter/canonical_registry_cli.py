"""Manual Phase-2 canonical-registry review workflows.

This module deliberately exposes only human-reviewed registry operations. It does not
seed concepts, call a model, mutate the browser, or project registry state into the
public corpus.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from jobhunter.analysis_current import (
    ENGLISH_ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.analysis_store import AnalysisArtifact, AnalysisStore
from jobhunter.canonical_registry import (
    AliasProvenanceKind,
    CanonicalAlias,
    CanonicalConcept,
    CanonicalRegistryError,
    CanonicalRegistryStore,
    ClaimKind,
    ConceptCategory,
    JobClaimMapping,
    MappingDisposition,
    build_canonical_registry_service,
)
from jobhunter.config import ConfigLoadError, Settings
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
    """Read the manual review queue without weakening the accepted P1.6 boundary."""

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
        """Return reviewed aliases for one concept in stable review order."""

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
    """Build the read-only claim-review surface for the configured current contract."""

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


def _bounded_limit(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("limit must be an integer") from exc
    if not 1 <= parsed <= 5000:
        raise argparse.ArgumentTypeError("limit must be between 1 and 5000")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    """Build the bounded manual registry CLI."""

    parser = argparse.ArgumentParser(
        prog="jobhunter-registry",
        description=(
            "Manually review the Phase-2 canonical concept registry. "
            "No model-driven concept or alias acceptance occurs here."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="TOML configuration path (default: ./jobhunter.toml)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    concepts = subparsers.add_parser("concepts", help="Review canonical concepts")
    concept_commands = concepts.add_subparsers(dest="concept_command", required=True)

    concept_list = concept_commands.add_parser("list", help="List reviewed concepts")
    concept_list.add_argument("--category", choices=tuple(item.value for item in ConceptCategory))
    concept_list.add_argument("--include-deprecated", action="store_true")
    concept_list.add_argument("--limit", type=_bounded_limit, default=500)

    concept_show = concept_commands.add_parser(
        "show",
        help="Show one concept and its reviewed aliases",
    )
    concept_show.add_argument("concept_id")
    concept_show.add_argument("--include-deprecated-aliases", action="store_true")

    concept_add = concept_commands.add_parser("add", help="Add one reviewed concept")
    concept_add.add_argument("concept_id")
    concept_add.add_argument(
        "--category",
        required=True,
        choices=tuple(item.value for item in ConceptCategory),
    )
    concept_add.add_argument("--label", required=True)
    concept_add.add_argument("--description")
    concept_add.add_argument("--reason", required=True)

    concept_deprecate = concept_commands.add_parser(
        "deprecate",
        help="Deprecate one reviewed concept without rewriting history",
    )
    concept_deprecate.add_argument("concept_id")
    concept_deprecate.add_argument("--successor")
    concept_deprecate.add_argument("--reason", required=True)

    aliases = subparsers.add_parser("aliases", help="Add reviewed concept aliases")
    alias_commands = aliases.add_subparsers(dest="alias_command", required=True)
    alias_add = alias_commands.add_parser("add", help="Add one reviewed alias")
    alias_add.add_argument("concept_id")
    alias_add.add_argument("alias_text")
    alias_add.add_argument(
        "--provenance",
        required=True,
        choices=tuple(item.value for item in AliasProvenanceKind),
    )
    alias_add.add_argument("--reference", required=True)
    alias_add.add_argument("--reason", required=True)

    claims = subparsers.add_parser(
        "claims",
        help="Inspect and decide accepted/current P1.6 claim mappings",
    )
    claim_commands = claims.add_subparsers(dest="claim_command", required=True)

    claim_list = claim_commands.add_parser(
        "list",
        help="List accepted/current claims and immutable mapping state",
    )
    claim_list.add_argument("--job-id")
    claim_list.add_argument("--kind", choices=tuple(item.value for item in ClaimKind))
    claim_list.add_argument(
        "--state",
        choices=("all", "pending", *(item.value for item in MappingDisposition)),
        default="all",
    )
    claim_list.add_argument("--limit", type=_bounded_limit, default=500)

    claim_decide = claim_commands.add_parser(
        "decide",
        help="Record mapped, unmapped, or rejected for one exact current claim",
    )
    claim_decide.add_argument("job_id")
    claim_decide.add_argument("kind", choices=tuple(item.value for item in ClaimKind))
    claim_decide.add_argument("index", type=int)
    claim_decide.add_argument(
        "disposition",
        choices=tuple(item.value for item in MappingDisposition),
    )
    claim_decide.add_argument("--concept")
    claim_decide.add_argument("--reason", required=True)

    return parser


def _load_settings(config_path: Path | None) -> Settings:
    try:
        return Settings.load(config_path)
    except (ConfigLoadError, ValidationError, ValueError) as exc:
        raise ValueError(f"Configuration error: {exc}") from exc


def _print_concept(concept: CanonicalConcept) -> None:
    print(f"{concept.concept_id} [{concept.status}]")
    print(f"Category: {concept.category}")
    print(f"Preferred label: {concept.preferred_label}")
    if concept.description:
        print(f"Description: {concept.description}")
    if concept.successor_concept_id:
        print(f"Successor: {concept.successor_concept_id}")
    print(f"Review note: {concept.review_note}")


def _print_claim(item: CanonicalClaimReviewItem) -> None:
    print(
        f"{item.source_job_id} artifact={item.analysis_artifact_id} "
        f"{item.claim_kind}[{item.claim_index}] state={item.mapping_state}"
    )
    print(f"  Source: {item.source_text}")
    if item.concept_type:
        print(f"  Concept type: {item.concept_type}")
    if item.strength:
        print(f"  Strength: {item.strength}")
    if item.depth_signal:
        print(f"  Depth: {item.depth_signal}")
    if item.evidence:
        print(f"  Evidence: {item.evidence}")
    if item.mapping is not None:
        if item.mapping.canonical_concept_id:
            print(f"  Canonical: {item.mapping.canonical_concept_id}")
        print(f"  Review note: {item.mapping.review_note}")


def _run_concepts(parsed: argparse.Namespace, settings: Settings) -> int:
    store = CanonicalRegistryStore(settings.database_path)
    if parsed.concept_command == "list":
        concepts = store.list_concepts(
            category=parsed.category,
            include_deprecated=parsed.include_deprecated,
            limit=parsed.limit,
        )
        if not concepts:
            print("No reviewed canonical concepts.")
            return 0
        for concept in concepts:
            print(
                f"{concept.concept_id}\t{concept.status}\t"
                f"{concept.category}\t{concept.preferred_label}"
            )
        return 0

    if parsed.concept_command == "show":
        concept = store.get_concept(parsed.concept_id)
        if concept is None:
            raise LookupError(f"Unknown canonical concept {parsed.concept_id!r}")
        _print_concept(concept)
        aliases = list_concept_aliases(
            settings.database_path,
            store,
            concept.concept_id,
            include_deprecated=parsed.include_deprecated_aliases,
        )
        if aliases:
            print("Aliases:")
            for alias in aliases:
                print(
                    f"  {alias.alias_text} [{alias.status}] "
                    f"{alias.provenance_kind}: {alias.provenance_reference}"
                )
        else:
            print("Aliases: none")
        return 0

    reviewed_at = datetime.now(UTC)
    if parsed.concept_command == "add":
        concept = store.create_concept(
            concept_id=parsed.concept_id,
            category=parsed.category,
            preferred_label=parsed.label,
            description=parsed.description,
            reviewed_at=reviewed_at,
            review_note=parsed.reason,
        )
        print(f"Reviewed concept: {concept.concept_id} [{concept.status}]")
        return 0

    concept = store.deprecate_concept(
        parsed.concept_id,
        successor_concept_id=parsed.successor,
        reviewed_at=reviewed_at,
        review_note=parsed.reason,
    )
    print(f"Deprecated concept: {concept.concept_id}")
    if concept.successor_concept_id:
        print(f"Successor: {concept.successor_concept_id}")
    return 0


def _run_aliases(parsed: argparse.Namespace, settings: Settings) -> int:
    store = CanonicalRegistryStore(settings.database_path)
    alias = store.add_alias(
        parsed.concept_id,
        alias_text=parsed.alias_text,
        provenance_kind=parsed.provenance,
        provenance_reference=parsed.reference,
        reviewed_at=datetime.now(UTC),
        review_note=parsed.reason,
    )
    print(f"Reviewed alias #{alias.id}: {alias.alias_text} -> {alias.concept_id}")
    return 0


def _run_claims(parsed: argparse.Namespace, settings: Settings) -> int:
    if parsed.claim_command == "list":
        items = build_canonical_registry_review_reader(settings).list_current_claims(
            source_job_id=parsed.job_id,
            claim_kind=parsed.kind,
            mapping_state=parsed.state,
            limit=parsed.limit,
        )
        if not items:
            print("No accepted/current P1.6 claims matched the review filter.")
            return 0
        for item in items:
            _print_claim(item)
        return 0

    if parsed.index < 0:
        raise ValueError("claim index must not be negative")
    if parsed.disposition == MappingDisposition.MAPPED and parsed.concept is None:
        raise ValueError("mapped disposition requires --concept")
    if parsed.disposition != MappingDisposition.MAPPED and parsed.concept is not None:
        raise ValueError("--concept is valid only for mapped disposition")

    mapping = build_canonical_registry_service(settings).record_current_claim_mapping(
        parsed.job_id,
        claim_kind=parsed.kind,
        claim_index=parsed.index,
        disposition=parsed.disposition,
        canonical_concept_id=parsed.concept,
        reviewed_at=datetime.now(UTC),
        review_note=parsed.reason,
    )
    print(
        f"Reviewed claim mapping #{mapping.id}: "
        f"{mapping.source_job_id} {mapping.claim_kind}[{mapping.claim_index}] "
        f"-> {mapping.disposition}"
    )
    if mapping.canonical_concept_id:
        print(f"Canonical concept: {mapping.canonical_concept_id}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the manual registry review CLI."""

    parser = build_parser()
    parsed = parser.parse_args(list(argv) if argv is not None else None)
    try:
        settings = _load_settings(parsed.config)
        if parsed.command == "concepts":
            return _run_concepts(parsed, settings)
        if parsed.command == "aliases":
            return _run_aliases(parsed, settings)
        if parsed.command == "claims":
            return _run_claims(parsed, settings)
    except (CanonicalRegistryError, LookupError, ValueError) as exc:
        print(f"Canonical registry review failed: {exc}", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"Canonical registry review failed: {exc}", file=sys.stderr)
        return 1
    raise RuntimeError("Unhandled canonical registry command")


if __name__ == "__main__":
    raise SystemExit(main())
