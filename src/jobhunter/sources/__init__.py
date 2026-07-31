"""Public job-source adapters."""

from jobhunter.sources.jobinja import (
    DiscoveredJobLink,
    FetchedSearchPage,
    JobinjaAcquisitionError,
    JobinjaClient,
    JobinjaUrlError,
    canonicalize_job_url,
    canonicalize_search_url,
    extract_job_links,
    with_search_page,
)

__all__ = [
    "DiscoveredJobLink",
    "FetchedSearchPage",
    "JobinjaAcquisitionError",
    "JobinjaClient",
    "JobinjaUrlError",
    "canonicalize_job_url",
    "canonicalize_search_url",
    "extract_job_links",
    "with_search_page",
]
