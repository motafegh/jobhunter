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
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from jobhunter.canonical_registry import (
    AliasProvenanceKind,
    CanonicalConcept,
    CanonicalRegistryError,
    CanonicalRegistryStore,
    ClaimKind,
    ConceptCategory,
    MappingDisposition,
    build_canonical_registry_service,
)
from jobhunter.canonical_registry_review import (
    CanonicalClaimReviewItem,
    build_canonical_registry_review_reader,
    list_concept_aliases,
)
from jobhunter.config import ConfigLoadError, Settings


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
