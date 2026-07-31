"""Configurable bilingual Jobinja keyword search registry.

The registry keeps curated career-oriented search vocabulary separate from CLI
and acquisition code. Built-in packs are starting points, not hidden product
policy: users can combine packs with their own keyword groups and raw URLs.
"""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from urllib.parse import urlencode, urlunsplit


@dataclass(frozen=True, slots=True)
class SearchPack:
    """One curated, versioned collection of Jobinja keyword searches."""

    name: str
    description: str
    terms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExpandedKeywordSearch:
    """One concrete Jobinja search generated from a keyword term."""

    name: str
    url: str
    term: str
    origin: str
    max_pages: int


AI_ML_TERMS = (
    "هوش مصنوعی",
    "Artificial Intelligence",
    "AI Engineer",
    "مهندس هوش مصنوعی",
    "AI Developer",
    "توسعه دهنده هوش مصنوعی",
    "AI Specialist",
    "متخصص هوش مصنوعی",
    "یادگیری ماشین",
    "Machine Learning",
    "Machine Learning Engineer",
    "مهندس یادگیری ماشین",
    "یادگیری عمیق",
    "Deep Learning",
    "علم داده",
    "Data Science",
    "دانشمند داده",
    "Data Scientist",
    "بینایی ماشین",
    "Computer Vision",
    "پردازش تصویر",
    "Image Processing",
    "پردازش زبان طبیعی",
    "Natural Language Processing",
    "NLP",
    "هوش مصنوعی مولد",
    "Generative AI",
    "GenAI",
    "مدل زبانی بزرگ",
    "Large Language Model",
    "LLM",
    "MLOps",
)

LLM_APPLICATION_TERMS = (
    "RAG",
    "Retrieval Augmented Generation",
    "بازیابی افزوده",
    "AI Agent",
    "عامل هوش مصنوعی",
    "Agentic AI",
    "هوش مصنوعی عامل محور",
    "Prompt Engineering",
    "مهندسی پرامپت",
    "Prompt Engineer",
    "مهندس پرامپت",
    "Chatbot",
    "چت بات",
    "LangChain",
    "LlamaIndex",
    "Vector Database",
    "پایگاه داده برداری",
    "Embeddings",
    "تعبیه برداری",
)

PYTHON_DATA_TERMS = (
    "Python",
    "پایتون",
    "Python Developer",
    "توسعه دهنده پایتون",
    "برنامه نویس پایتون",
    "Python Engineer",
    "FastAPI",
    "Django",
    "Flask",
    "Data Engineer",
    "مهندس داده",
    "Data Engineering",
    "مهندسی داده",
    "ETL",
    "Apache Airflow",
    "Apache Spark",
    "SQL",
    "NoSQL",
    "API Developer",
    "توسعه دهنده API",
)

DEFENSIVE_SECURITY_TERMS = (
    "امنیت سایبری",
    "Cybersecurity",
    "امنیت اطلاعات",
    "Information Security",
    "مهندس امنیت",
    "Security Engineer",
    "کارشناس امنیت",
    "Security Analyst",
    "SOC Analyst",
    "تحلیلگر مرکز عملیات امنیت",
    "مرکز عملیات امنیت",
    "SOC",
    "SIEM",
    "Detection Engineer",
    "مهندس تشخیص",
    "Threat Hunting",
    "شکار تهدید",
    "Incident Response",
    "پاسخ به رخداد",
    "Blue Team",
    "تیم آبی",
    "Network Security",
    "امنیت شبکه",
    "Security Automation",
    "اتوماسیون امنیت",
    "SOAR",
    "DevSecOps",
    "Application Security",
    "امنیت نرم افزار",
    "Cloud Security",
    "امنیت ابری",
    "Vulnerability Management",
    "مدیریت آسیب پذیری",
    "Malware Analysis",
    "تحلیل بدافزار",
)

AI_SECURITY_TERMS = (
    "AI Security",
    "امنیت هوش مصنوعی",
    "Machine Learning Security",
    "امنیت یادگیری ماشین",
    "ML Security",
    "LLM Security",
    "امنیت مدل زبانی",
    "Model Security",
    "امنیت مدل",
    "AI Agent Security",
    "امنیت عامل هوش مصنوعی",
    "Adversarial Machine Learning",
    "یادگیری ماشین خصمانه",
    "AI Red Team",
    "Prompt Injection",
    "تزریق پرامپت",
    "Responsible AI",
    "هوش مصنوعی مسئولانه",
)

NETWORK_PLATFORM_TERMS = (
    "Linux",
    "لینوکس",
    "Network Engineer",
    "مهندس شبکه",
    "Computer Networks",
    "شبکه های کامپیوتری",
    "DevOps",
    "مهندس دواپس",
    "Site Reliability Engineer",
    "SRE",
    "Platform Engineer",
    "مهندس پلتفرم",
    "Cloud Engineer",
    "مهندس ابر",
    "System Administrator",
    "مدیر سیستم",
    "Docker",
    "Kubernetes",
)


BUILTIN_SEARCH_PACKS: dict[str, SearchPack] = {
    "ai-ml": SearchPack(
        name="ai-ml",
        description="AI, machine learning, data science, NLP, vision, and MLOps roles",
        terms=AI_ML_TERMS,
    ),
    "llm-applications": SearchPack(
        name="llm-applications",
        description="LLM, RAG, agents, prompt engineering, and applied GenAI roles",
        terms=LLM_APPLICATION_TERMS,
    ),
    "python-data": SearchPack(
        name="python-data",
        description="Python application, API, data engineering, and data-platform roles",
        terms=PYTHON_DATA_TERMS,
    ),
    "defensive-security": SearchPack(
        name="defensive-security",
        description="Defensive security, SOC, detection, response, AppSec, and automation",
        terms=DEFENSIVE_SECURITY_TERMS,
    ),
    "ai-security": SearchPack(
        name="ai-security",
        description="AI, ML, LLM, model, agent, and prompt-security roles",
        terms=AI_SECURITY_TERMS,
    ),
    "network-platform": SearchPack(
        name="network-platform",
        description="Linux, networking, DevOps, platform, cloud, and container roles",
        terms=NETWORK_PLATFORM_TERMS,
    ),
}

BUILTIN_SEARCH_PROFILES: dict[str, tuple[str, ...]] = {
    "ai-security-python": (
        "ai-ml",
        "llm-applications",
        "python-data",
        "defensive-security",
        "ai-security",
        "network-platform",
    ),
    "ai-focused": ("ai-ml", "llm-applications", "ai-security"),
    "security-focused": ("defensive-security", "ai-security", "network-platform"),
}


def normalize_search_term(value: str) -> str:
    """Return a stable comparison form without changing the displayed term."""

    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.replace("ي", "ی").replace("ك", "ک")
    normalized = normalized.replace("\u200c", " ").replace("\u200f", "")
    return " ".join(normalized.casefold().split())


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


def available_pack_names() -> tuple[str, ...]:
    """Return stable built-in pack identifiers."""

    return tuple(BUILTIN_SEARCH_PACKS)


def available_profile_names() -> tuple[str, ...]:
    """Return stable built-in profile identifiers."""

    return tuple(BUILTIN_SEARCH_PROFILES)


def resolve_pack_names(
    *,
    pack_names: tuple[str, ...] = (),
    profile_names: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Expand profiles and packs into an ordered unique list of pack names."""

    resolved: list[str] = []
    for profile_name in profile_names:
        try:
            profile_packs = BUILTIN_SEARCH_PROFILES[profile_name]
        except KeyError as exc:
            raise ValueError(f"Unknown Jobinja search profile: {profile_name!r}") from exc
        resolved.extend(profile_packs)
    resolved.extend(pack_names)

    unique = tuple(dict.fromkeys(resolved))
    unknown = [name for name in unique if name not in BUILTIN_SEARCH_PACKS]
    if unknown:
        raise ValueError(f"Unknown Jobinja search pack(s): {', '.join(unknown)}")
    return unique


def _interleaved_pack_candidates(
    pack_names: tuple[str, ...],
    *,
    max_pages: int,
) -> list[tuple[str, str, int]]:
    """Round-robin terms so bounded windows represent every selected pack."""

    packs = tuple(BUILTIN_SEARCH_PACKS[name] for name in pack_names)
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
    )
    candidates = _interleaved_pack_candidates(
        resolved_packs,
        max_pages=default_max_pages,
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


def format_search_catalog() -> str:
    """Format built-in profiles and packs for terminal inspection."""

    lines = ["Built-in Jobinja search profiles:"]
    for name, packs in BUILTIN_SEARCH_PROFILES.items():
        lines.append(f"- {name}: {', '.join(packs)}")
    lines.append("")
    lines.append("Built-in Jobinja search packs:")
    for pack in BUILTIN_SEARCH_PACKS.values():
        lines.append(f"- {pack.name}: {len(pack.terms)} terms")
        lines.append(f"  {pack.description}")
    return "\n".join(lines)


def format_search_plan(
    searches: tuple[ExpandedKeywordSearch, ...],
    *,
    request_budget: int,
) -> str:
    """Format the expanded search plan before any network request."""

    planned_requests = sum(search.max_pages for search in searches)
    effective_requests = min(planned_requests, request_budget)
    lines = [
        "Jobinja keyword search plan",
        f"Expanded searches: {len(searches)}",
        f"Planned page requests: {planned_requests}",
        f"Request budget: {request_budget}",
        f"Maximum requests this run: {effective_requests}",
    ]
    if planned_requests > request_budget:
        lines.append(
            "Plan exceeds the request budget; later searches will be "
            "reported as budget-skipped."
        )
    if not searches:
        lines.append("No keyword searches are configured.")
        return "\n".join(lines)

    lines.append("Searches:")
    for search in searches:
        lines.append(
            f"- {search.term} [{search.origin}, max_pages={search.max_pages}]"
        )
    return "\n".join(lines)
