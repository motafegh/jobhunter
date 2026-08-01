"""Data-driven bilingual Jobinja keyword search registry."""

from __future__ import annotations

import hashlib
import tomllib
import unicodedata
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlunsplit


@dataclass(frozen=True, slots=True)
class SearchPack:
    """One curated, versioned collection of Jobinja keyword searches."""

    name: str
    description: str
    terms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SearchCatalog:
    """Validated search vocabulary loaded from TOML rather than Python constants."""

    version: str
    packs: dict[str, SearchPack]
    profiles: dict[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class ExpandedKeywordSearch:
    """One concrete Jobinja search generated from a keyword term."""

    name: str
    url: str
    term: str
    origin: str
    max_pages: int


def normalize_search_term(value: str) -> str:
    """Return a stable comparison form without changing the displayed term."""

    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("ي", "ی").replace("ك", "ک")
    normalized = normalized.replace("\u200c", " ").replace("\u200f", "")
    return " ".join(normalized.casefold().split())


def _catalog_from_mapping(mapping: dict[str, Any], *, source: str) -> SearchCatalog:
    version = str(mapping.get("catalog_version") or "unversioned").strip()
    raw_packs = mapping.get("packs")
    raw_profiles = mapping.get("profiles")
    if not isinstance(raw_packs, dict) or not raw_packs:
        raise ValueError(f"Search catalog {source} must define a non-empty [packs] table")
    if not isinstance(raw_profiles, dict):
        raise ValueError(f"Search catalog {source} must define a [profiles] table")

    packs: dict[str, SearchPack] = {}
    for raw_name, raw_pack in raw_packs.items():
        name = str(raw_name).strip()
        if not name or not isinstance(raw_pack, dict):
            raise ValueError(f"Invalid search pack in {source}: {raw_name!r}")
        description = str(raw_pack.get("description") or "").strip()
        raw_terms = raw_pack.get("terms")
        if not isinstance(raw_terms, list):
            raise ValueError(f"Search pack {name!r} in {source} must define terms as a list")

        terms: list[str] = []
        seen_terms: set[str] = set()
        for raw_term in raw_terms:
            if not isinstance(raw_term, str):
                raise ValueError(f"Search pack {name!r} contains a non-text term")
            term = " ".join(raw_term.split())
            normalized = normalize_search_term(term)
            if not normalized or normalized in seen_terms:
                continue
            seen_terms.add(normalized)
            terms.append(term)
        if not terms:
            raise ValueError(f"Search pack {name!r} in {source} has no usable terms")
        packs[name] = SearchPack(name=name, description=description, terms=tuple(terms))

    profiles: dict[str, tuple[str, ...]] = {}
    for raw_name, raw_pack_names in raw_profiles.items():
        name = str(raw_name).strip()
        if not name or not isinstance(raw_pack_names, list):
            raise ValueError(f"Invalid search profile in {source}: {raw_name!r}")
        pack_names = tuple(dict.fromkeys(str(item).strip() for item in raw_pack_names))
        unknown = [pack_name for pack_name in pack_names if pack_name not in packs]
        if unknown:
            raise ValueError(
                f"Search profile {name!r} in {source} references unknown packs: "
                f"{', '.join(unknown)}"
            )
        profiles[name] = pack_names

    return SearchCatalog(version=version, packs=packs, profiles=profiles)


def _load_toml_bytes(content: bytes, *, source: str) -> SearchCatalog:
    try:
        mapping = tomllib.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"Could not parse search catalog {source}: {exc}") from exc
    return _catalog_from_mapping(mapping, source=source)


def load_builtin_search_catalog() -> SearchCatalog:
    """Load the packaged default vocabulary."""

    resource = files("jobhunter").joinpath("data/search_catalog.toml")
    return _load_toml_bytes(resource.read_bytes(), source="built-in search catalog")


def load_search_catalog(path: Path | None = None) -> SearchCatalog:
    """Load the built-in catalog or a complete user-supplied replacement catalog."""

    if path is None:
        return load_builtin_search_catalog()
    selected = path.expanduser()
    try:
        content = selected.read_bytes()
    except OSError as exc:
        raise ValueError(f"Could not read search catalog {selected}: {exc}") from exc
    return _load_toml_bytes(content, source=str(selected))


BUILTIN_SEARCH_CATALOG = load_builtin_search_catalog()
BUILTIN_SEARCH_PACKS = BUILTIN_SEARCH_CATALOG.packs
BUILTIN_SEARCH_PROFILES = BUILTIN_SEARCH_CATALOG.profiles


def build_jobinja_keyword_url(term: str) -> str:
    """Build a canonical Jobinja keyword-filter URL from one non-empty term."""

    cleaned = " ".join(term.split())
    if not cleaned:
        raise ValueError("Jobinja keyword term must not be empty")
    query = urlencode([("filters[keywords][0]", cleaned)])
    return urlunsplit(("https", "jobinja.ir", "/jobs", query, ""))


def _search_name(origin: str, term: str) -> str:
    digest = hashlib.sha256(
        f"{origin}\0{normalize_search_term(term)}".encode("utf-8")
    ).hexdigest()[:10]
    return f"{origin} :: {term} [{digest}]"


def available_pack_names(catalog: SearchCatalog = BUILTIN_SEARCH_CATALOG) -> tuple[str, ...]:
    """Return stable pack identifiers from one catalog."""

    return tuple(catalog.packs)


def available_profile_names(
    catalog: SearchCatalog = BUILTIN_SEARCH_CATALOG,
) -> tuple[str, ...]:
    """Return stable profile identifiers from one catalog."""

    return tuple(catalog.profiles)


def resolve_pack_names(
    *,
    pack_names: tuple[str, ...] = (),
    profile_names: tuple[str, ...] = (),
    catalog: SearchCatalog = BUILTIN_SEARCH_CATALOG,
) -> tuple[str, ...]:
    """Expand profiles and packs into an ordered unique list of pack names."""

    resolved: list[str] = []
    for profile_name in profile_names:
        try:
            profile_packs = catalog.profiles[profile_name]
        except KeyError as exc:
            raise ValueError(f"Unknown Jobinja search profile: {profile_name!r}") from exc
        resolved.extend(profile_packs)
    resolved.extend(pack_names)

    unique = tuple(dict.fromkeys(resolved))
    unknown = [name for name in unique if name not in catalog.packs]
    if unknown:
        raise ValueError(f"Unknown Jobinja search pack(s): {', '.join(unknown)}")
    return unique


def _interleaved_pack_candidates(
    pack_names: tuple[str, ...],
    *,
    max_pages: int,
    catalog: SearchCatalog,
) -> list[tuple[str, str, int]]:
    """Round-robin terms so bounded windows represent every selected pack."""

    packs = tuple(catalog.packs[name] for name in pack_names)
    if not packs:
        return []

    candidates: list[tuple[str, str, int]] = []
    longest_pack = max(len(pack.terms) for pack in packs)
    for term_index in range(longest_pack):
        for pack in packs:
            if term_index >= len(pack.terms):
                continue
            candidates.append(
                (f"pack:{pack.name}", pack.terms[term_index], max_pages)
            )
    return candidates


def expand_keyword_searches(
    *,
    pack_names: tuple[str, ...] = (),
    profile_names: tuple[str, ...] = (),
    custom_groups: tuple[tuple[str, tuple[str, ...], int], ...] = (),
    extra_terms: tuple[str, ...] = (),
    excluded_terms: tuple[str, ...] = (),
    default_max_pages: int = 1,
    catalog: SearchCatalog = BUILTIN_SEARCH_CATALOG,
) -> tuple[ExpandedKeywordSearch, ...]:
    """Expand packs, profiles, custom groups, and terms into unique searches."""

    if not 1 <= default_max_pages <= 50:
        raise ValueError("default_max_pages must be between 1 and 50")

    excluded = {
        normalize_search_term(term)
        for term in excluded_terms
        if term.strip()
    }
    resolved_packs = resolve_pack_names(
        pack_names=pack_names,
        profile_names=profile_names,
        catalog=catalog,
    )
    candidates = _interleaved_pack_candidates(
        resolved_packs,
        max_pages=default_max_pages,
        catalog=catalog,
    )

    for group_name, terms, max_pages in custom_groups:
        if not 1 <= max_pages <= 50:
            raise ValueError("custom group max_pages must be between 1 and 50")
        candidates.extend(
            (f"group:{group_name}", term, max_pages)
            for term in terms
        )

    candidates.extend(
        ("term:adhoc", term, default_max_pages)
        for term in extra_terms
    )

    seen_terms: set[str] = set()
    expanded: list[ExpandedKeywordSearch] = []
    for origin, raw_term, max_pages in candidates:
        term = " ".join(raw_term.split())
        normalized = normalize_search_term(term)
        if not normalized or normalized in excluded or normalized in seen_terms:
            continue
        seen_terms.add(normalized)
        expanded.append(
            ExpandedKeywordSearch(
                name=_search_name(origin, term),
                url=build_jobinja_keyword_url(term),
                term=term,
                origin=origin,
                max_pages=max_pages,
            )
        )
    return tuple(expanded)


def format_search_catalog(
    catalog: SearchCatalog = BUILTIN_SEARCH_CATALOG,
    *,
    show_terms: bool = False,
) -> str:
    """Format profiles and packs for terminal inspection."""

    lines = [
        f"Jobinja search catalog version: {catalog.version}",
        "Built-in/configured Jobinja search profiles:",
    ]
    for name, packs in catalog.profiles.items():
        lines.append(f"- {name}: {', '.join(packs)}")
    lines.append("")
    lines.append("Jobinja search packs:")
    for pack in catalog.packs.values():
        lines.append(f"- {pack.name}: {len(pack.terms)} terms")
        lines.append(f"  {pack.description}")
        if show_terms:
            lines.append("  Terms:")
            lines.extend(f"  - {term}" for term in pack.terms)
    return "\n".join(lines)
