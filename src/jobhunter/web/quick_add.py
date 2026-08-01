"""Interpret one user-facing Quick Add input for bounded Jobinja acquisition."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from urllib.parse import urlsplit

from jobhunter.search_registry import build_jobinja_keyword_url
from jobhunter.sources import (
    DiscoveredJobLink,
    JobinjaUrlError,
    canonicalize_job_url,
    canonicalize_search_url,
)


@dataclass(frozen=True, slots=True)
class QuickAddTarget:
    """One validated user input resolved to a supported Jobinja acquisition target."""

    kind: str
    display_value: str
    job: DiscoveredJobLink | None = None
    search_url: str | None = None

    def search_name(self) -> str:
        digest = hashlib.sha256(
            f"{self.kind}\0{self.display_value}".encode()
        ).hexdigest()[:10]
        return f"quick-add:{self.kind}:{digest}"


def _looks_like_url(value: str) -> bool:
    lowered = value.casefold()
    return lowered.startswith(("http://", "https://", "jobinja.ir/", "www.jobinja.ir/"))


def _normalize_url(value: str) -> str:
    if value.casefold().startswith(("jobinja.ir/", "www.jobinja.ir/")):
        return f"https://{value}"
    return value


def parse_quick_add_input(value: str) -> QuickAddTarget:
    """Resolve a job URL, search URL, or plain Persian/English keyword."""

    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Enter a Jobinja job URL, Jobinja search URL, or search keyword")
    if len(cleaned) > 500:
        raise ValueError("Quick Add input is too long; use one URL or one search phrase")

    if _looks_like_url(cleaned):
        candidate = _normalize_url(cleaned)
        parsed = urlsplit(candidate)
        if parsed.hostname not in {"jobinja.ir", "www.jobinja.ir"}:
            raise ValueError("Quick Add currently accepts public Jobinja URLs only")
        try:
            job = canonicalize_job_url(candidate)
        except JobinjaUrlError:
            job = None
        if job is not None:
            return QuickAddTarget(kind="job", display_value=job.canonical_url, job=job)

        try:
            search_url = canonicalize_search_url(candidate)
        except JobinjaUrlError as exc:
            raise ValueError(
                "The Jobinja URL is neither a supported job page nor a /jobs search page"
            ) from exc
        return QuickAddTarget(
            kind="search-url",
            display_value=search_url,
            search_url=search_url,
        )

    term = " ".join(cleaned.split())
    if len(term) > 160:
        raise ValueError("Search phrases are limited to 160 characters")
    return QuickAddTarget(
        kind="keyword",
        display_value=term,
        search_url=build_jobinja_keyword_url(term),
    )
