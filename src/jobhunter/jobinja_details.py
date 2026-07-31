"""Deterministic extraction for public Jobinja job-detail HTML."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
from typing import Any

PARSER_VERSION = "jobinja-detail-v1"

_LABELS: dict[str, tuple[str, ...]] = {
    "job_category": ("دسته‌بندی شغلی", "دسته بندی شغلی"),
    "location": ("موقعیت مکانی",),
    "employment_type": ("نوع همکاری",),
    "minimum_experience": ("حداقل سابقه کار",),
    "salary": ("حقوق",),
    "description": ("شرح موقعیت شغلی",),
    "skills": ("مهارت‌های مورد نیاز", "مهارت های مورد نیاز"),
    "gender": ("جنسیت",),
    "military_service": ("وضعیت نظام وظیفه",),
    "education": ("حداقل مدرک تحصیلی",),
    "company_description": ("معرفی شرکت",),
}
_BLOCK_TAGS = {
    "address",
    "article",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "header",
    "li",
    "main",
    "p",
    "section",
    "td",
    "th",
    "tr",
    "ul",
}
_IGNORED_TAGS = {"script", "style", "noscript", "svg"}
_PERSIAN_RE = re.compile(r"[\u0600-\u06ff]")
_LATIN_RE = re.compile(r"[A-Za-z]")


@dataclass(frozen=True, slots=True)
class ParsedJobDetail:
    """Explicit source fields extracted from one Jobinja detail page."""

    title: str | None = None
    company: str | None = None
    job_category: str | None = None
    location: str | None = None
    employment_type: str | None = None
    minimum_experience: str | None = None
    salary: str | None = None
    description: str | None = None
    skills: tuple[str, ...] = ()
    gender: str | None = None
    military_service: str | None = None
    education: str | None = None
    company_description: str | None = None
    date_posted: str | None = None
    valid_through: str | None = None
    language: str = "unknown"
    parser_version: str = PARSER_VERSION

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["skills"] = list(self.skills)
        return result


class _PageCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.json_ld: list[str] = []
        self.h1_parts: list[str] = []
        self.text_parts: list[str] = []
        self._ignored_depth = 0
        self._json_ld_depth = 0
        self._json_ld_parts: list[str] = []
        self._h1_depth = 0

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        lower = tag.lower()
        attributes = {key.lower(): value for key, value in attrs}
        if lower == "meta":
            key = (
                attributes.get("property")
                or attributes.get("name")
                or attributes.get("itemprop")
            )
            content = attributes.get("content")
            if key and content:
                self.meta[key.lower()] = content.strip()

        script_type = (attributes.get("type") or "").lower()
        if lower == "script" and script_type == "application/ld+json":
            self._json_ld_depth = 1
            self._json_ld_parts = []
            return
        if self._json_ld_depth:
            self._json_ld_depth += 1
            return
        if lower in _IGNORED_TAGS:
            self._ignored_depth += 1
            return
        if self._ignored_depth:
            return
        if lower == "h1":
            self._h1_depth += 1
        if lower in _BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        lower = tag.lower()
        if self._json_ld_depth:
            self._json_ld_depth -= 1
            if self._json_ld_depth == 0:
                content = "".join(self._json_ld_parts).strip()
                if content:
                    self.json_ld.append(content)
            return
        if lower in _IGNORED_TAGS and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if lower == "h1" and self._h1_depth:
            self._h1_depth -= 1
        if lower in _BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._json_ld_depth:
            self._json_ld_parts.append(data)
            return
        if self._ignored_depth:
            return
        self.text_parts.extend((data, " "))
        if self._h1_depth:
            self.h1_parts.extend((data, " "))


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = " ".join(unescape(str(value)).split())
    return text or None


def _strip_html(value: str | None) -> str | None:
    if not value:
        return None
    collector = _PageCollector()
    collector.feed(value)
    collector.close()
    return _clean("".join(collector.text_parts))


def _iter_json_objects(value: Any):
    if isinstance(value, dict):
        yield value
        graph = value.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                yield from _iter_json_objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_json_objects(item)


def _jobposting_json(collector: _PageCollector) -> dict[str, Any] | None:
    for raw in collector.json_ld:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in _iter_json_objects(parsed):
            item_type = item.get("@type")
            types = item_type if isinstance(item_type, list) else [item_type]
            if "JobPosting" in types:
                return item
    return None


def _schema_text(value: Any) -> str | None:
    if isinstance(value, list):
        rendered = [_schema_text(item) for item in value]
        return " | ".join(item for item in rendered if item) or None
    if isinstance(value, dict):
        preferred_keys = (
            "name",
            "description",
            "value",
            "monthsOfExperience",
            "yearsOfExperience",
        )
        rendered = [_schema_text(value.get(key)) for key in preferred_keys]
        return " ".join(item for item in rendered if item) or None
    return _clean(value)


def _format_location(value: Any) -> str | None:
    locations = value if isinstance(value, list) else [value]
    rendered: list[str] = []
    for location in locations:
        if not isinstance(location, dict):
            continue
        address = location.get("address", location)
        if not isinstance(address, dict):
            continue
        parts = [
            _clean(address.get("addressLocality")),
            _clean(address.get("addressRegion")),
            _clean(address.get("streetAddress")),
            _clean(address.get("addressCountry")),
        ]
        text = "، ".join(part for part in parts if part)
        if text and text not in rendered:
            rendered.append(text)
    return " | ".join(rendered) or None


def _format_salary(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        return _clean(value)
    currency = _clean(value.get("currency"))
    nested = value.get("value")
    if isinstance(nested, dict):
        parts = [
            _clean(nested.get("minValue")),
            _clean(nested.get("maxValue")),
            _clean(nested.get("unitText")),
            currency,
        ]
        return " ".join(part for part in parts if part) or None
    return _clean(nested) or currency


def _visible_lines(collector: _PageCollector) -> list[str]:
    text = "".join(collector.text_parts).replace("\r", "\n")
    return [
        cleaned
        for line in text.split("\n")
        if (cleaned := _clean(line))
    ]


def _normalize_label(value: str) -> str:
    return (
        value.replace("ي", "ی")
        .replace("ك", "ک")
        .replace(":", "")
        .replace("：", "")
        .strip()
    )


def _label_sections(lines: list[str]) -> dict[str, list[str]]:
    aliases = {
        _normalize_label(alias): field
        for field, field_aliases in _LABELS.items()
        for alias in field_aliases
    }
    markers: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        field = aliases.get(_normalize_label(line))
        if field:
            markers.append((index, field))

    sections: dict[str, list[str]] = {}
    for marker_index, (line_index, field) in enumerate(markers):
        end = (
            markers[marker_index + 1][0]
            if marker_index + 1 < len(markers)
            else len(lines)
        )
        values = lines[line_index + 1 : end]
        if not values:
            continue
        existing = sections.get(field)
        if existing is None or sum(map(len, values)) > sum(map(len, existing)):
            sections[field] = values
    return sections


def _scalar_section(
    sections: dict[str, list[str]],
    field: str,
) -> str | None:
    values = sections.get(field, [])
    return _clean(" | ".join(values[:4]))


def _text_section(
    sections: dict[str, list[str]],
    field: str,
) -> str | None:
    return _clean("\n".join(sections.get(field, [])))


def _skills(value: Any, section_values: list[str]) -> tuple[str, ...]:
    raw_values: list[str] = []
    if isinstance(value, str):
        raw_values.extend(re.split(r"[,،|\n]", value))
    elif isinstance(value, list):
        raw_values.extend(str(item) for item in value)
    raw_values.extend(section_values)

    result: list[str] = []
    for raw in raw_values:
        cleaned = _clean(raw)
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return tuple(result)


def _language(*values: str | None) -> str:
    text = " ".join(value for value in values if value)
    persian = len(_PERSIAN_RE.findall(text))
    latin = len(_LATIN_RE.findall(text))
    if persian and latin:
        return "mixed"
    if persian:
        return "fa"
    if latin:
        return "en"
    return "unknown"


def parse_jobinja_detail(html: str) -> ParsedJobDetail:
    """Extract explicit Jobinja fields without model interpretation."""

    collector = _PageCollector()
    collector.feed(html)
    collector.close()
    structured = _jobposting_json(collector) or {}
    lines = _visible_lines(collector)
    sections = _label_sections(lines)

    organization = structured.get("hiringOrganization")
    company = organization.get("name") if isinstance(organization, dict) else None
    employment = structured.get("employmentType")
    if isinstance(employment, list):
        employment = " | ".join(str(item) for item in employment)

    title = (
        _clean(structured.get("title"))
        or _clean("".join(collector.h1_parts))
        or _clean(collector.meta.get("og:title"))
    )
    description = (
        _strip_html(structured.get("description"))
        or _text_section(sections, "description")
    )
    company_description = _text_section(sections, "company_description")

    return ParsedJobDetail(
        title=title,
        company=_clean(company),
        job_category=_scalar_section(sections, "job_category"),
        location=(
            _format_location(structured.get("jobLocation"))
            or _scalar_section(sections, "location")
        ),
        employment_type=(
            _clean(employment)
            or _scalar_section(sections, "employment_type")
        ),
        minimum_experience=(
            _schema_text(structured.get("experienceRequirements"))
            or _scalar_section(sections, "minimum_experience")
        ),
        salary=(
            _format_salary(structured.get("baseSalary"))
            or _scalar_section(sections, "salary")
        ),
        description=description,
        skills=_skills(
            structured.get("skills"),
            sections.get("skills", []),
        ),
        gender=_scalar_section(sections, "gender"),
        military_service=_scalar_section(sections, "military_service"),
        education=(
            _schema_text(structured.get("educationRequirements"))
            or _scalar_section(sections, "education")
        ),
        company_description=company_description,
        date_posted=_clean(structured.get("datePosted")),
        valid_through=_clean(structured.get("validThrough")),
        language=_language(title, description, company_description),
    )
