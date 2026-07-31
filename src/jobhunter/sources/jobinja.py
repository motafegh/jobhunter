"""Jobinja public search acquisition and deterministic job-link parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import httpx

ALLOWED_JOBINJA_HOSTS = {"jobinja.ir", "www.jobinja.ir"}
_JOB_PATH_PATTERN = re.compile(
    r"^/companies/(?P<company_slug>[^/]+)/jobs/(?P<job_code>[^/]+)(?:/.*)?$"
)


class JobinjaUrlError(ValueError):
    """Raised when a URL is not a supported public Jobinja URL."""


class JobinjaAcquisitionError(RuntimeError):
    """Raised when a Jobinja page cannot be acquired safely."""


@dataclass(frozen=True, slots=True)
class DiscoveredJobLink:
    """One canonical Jobinja job identity discovered from a search page."""

    source_job_id: str
    company_slug: str
    canonical_url: str
    observed_text: str | None = None


@dataclass(frozen=True, slots=True)
class FetchedSearchPage:
    """Raw and decoded data returned from one Jobinja search-page request."""

    requested_url: str
    final_url: str
    status_code: int
    headers: dict[str, str]
    content: bytes
    text: str


def _validate_jobinja_host(url: str) -> tuple[str, str, str, str]:
    parsed = urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise JobinjaUrlError("Jobinja URL must use HTTP or HTTPS")
    if parsed.username or parsed.password or parsed.port:
        raise JobinjaUrlError("Jobinja URL must not contain credentials or a custom port")
    if parsed.hostname not in ALLOWED_JOBINJA_HOSTS:
        raise JobinjaUrlError("URL host must be jobinja.ir")
    return parsed.path, parsed.query, parsed.fragment, parsed.hostname


def canonicalize_search_url(url: str) -> str:
    """Validate and canonicalize a Jobinja search URL without a page number."""

    path, query, _fragment, _hostname = _validate_jobinja_host(url)
    if path.rstrip("/") != "/jobs":
        raise JobinjaUrlError("Jobinja search URL path must be /jobs")

    query_items = [(key, value) for key, value in parse_qsl(query, keep_blank_values=True) if key != "page"]
    canonical_query = urlencode(query_items, doseq=True)
    return urlunsplit(("https", "jobinja.ir", "/jobs", canonical_query, ""))


def with_search_page(search_url: str, page_number: int) -> str:
    """Return a canonical Jobinja search URL for one positive page number."""

    if page_number < 1:
        raise ValueError("page_number must be at least 1")

    canonical = canonicalize_search_url(search_url)
    parsed = urlsplit(canonical)
    query_items = parse_qsl(parsed.query, keep_blank_values=True)
    if page_number > 1:
        query_items.append(("page", str(page_number)))
    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urlencode(query_items, doseq=True), "")
    )


def canonicalize_job_url(raw_url: str, *, base_url: str = "https://jobinja.ir/") -> DiscoveredJobLink:
    """Convert a Jobinja job link into a stable source identity."""

    absolute_url = urljoin(base_url, raw_url.strip())
    path, _query, _fragment, _hostname = _validate_jobinja_host(absolute_url)
    normalized_path = path.rstrip("/")
    match = _JOB_PATH_PATTERN.fullmatch(normalized_path)
    if match is None:
        raise JobinjaUrlError("URL is not a supported Jobinja job-advertisement path")

    return DiscoveredJobLink(
        source_job_id=match.group("job_code"),
        company_slug=match.group("company_slug"),
        canonical_url=urlunsplit(("https", "jobinja.ir", normalized_path, "", "")),
    )


class _AnchorCollector(HTMLParser):
    """Collect anchor hrefs and visible text without executing page content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[tuple[str, str]] = []
        self._active_href: str | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a" or self._active_href is not None:
            return
        attributes = dict(attrs)
        href = attributes.get("href")
        if href:
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href is not None:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._active_href is None:
            return
        text = " ".join("".join(self._active_text).split())
        self.anchors.append((self._active_href, text))
        self._active_href = None
        self._active_text = []


def extract_job_links(html: str, *, base_url: str) -> tuple[DiscoveredJobLink, ...]:
    """Extract unique Jobinja job identities from one search-page document."""

    collector = _AnchorCollector()
    collector.feed(html)
    collector.close()

    discovered: list[DiscoveredJobLink] = []
    seen_job_ids: set[str] = set()
    for href, observed_text in collector.anchors:
        try:
            identity = canonicalize_job_url(href, base_url=base_url)
        except JobinjaUrlError:
            continue
        if identity.source_job_id in seen_job_ids:
            continue
        seen_job_ids.add(identity.source_job_id)
        discovered.append(
            DiscoveredJobLink(
                source_job_id=identity.source_job_id,
                company_slug=identity.company_slug,
                canonical_url=identity.canonical_url,
                observed_text=observed_text or None,
            )
        )

    return tuple(discovered)


class JobinjaClient:
    """Small synchronous client for public Jobinja search pages."""

    def __init__(
        self,
        *,
        user_agent: str,
        timeout_seconds: float,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._user_agent = user_agent
        self._timeout_seconds = timeout_seconds
        self._transport = transport

    def fetch_search_page(self, search_url: str, page_number: int) -> FetchedSearchPage:
        """Fetch one bounded Jobinja search page and validate its final destination."""

        requested_url = with_search_page(search_url, page_number)
        try:
            with httpx.Client(
                timeout=self._timeout_seconds,
                follow_redirects=True,
                transport=self._transport,
                headers={
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "fa,en;q=0.8",
                    "User-Agent": self._user_agent,
                },
            ) as client:
                response = client.get(requested_url)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise JobinjaAcquisitionError(
                f"Jobinja returned HTTP {exc.response.status_code} for {requested_url}"
            ) from exc
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
            raise JobinjaAcquisitionError(
                f"Could not fetch Jobinja search page {requested_url}: {exc}"
            ) from exc

        final_url = str(response.url)
        final_path, _query, _fragment, _hostname = _validate_jobinja_host(final_url)
        if final_path.rstrip("/") != "/jobs":
            raise JobinjaAcquisitionError(
                f"Jobinja search redirected to an unsupported path: {final_url}"
            )

        content_type = response.headers.get("content-type", "")
        if content_type and "text/html" not in content_type.lower():
            raise JobinjaAcquisitionError(
                f"Jobinja search returned unsupported content type {content_type!r}"
            )

        selected_headers = {
            key.lower(): value
            for key, value in response.headers.items()
            if key.lower() in {"content-type", "etag", "last-modified", "cache-control"}
        }
        return FetchedSearchPage(
            requested_url=requested_url,
            final_url=final_url,
            status_code=response.status_code,
            headers=selected_headers,
            content=response.content,
            text=response.text,
        )
