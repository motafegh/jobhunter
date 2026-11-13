"""Original-language advisory conflicts between board skill tags and employer prose.

Never silently rewrite structured source skill tags or treat them as guaranteed
mandatory technical qualifications. Every warning anchors an exact source span.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from jobhunter.source_lineage_v1 import OriginalSourceSpine
from jobhunter.translation_store import TranslationSourceVersion

_NOT_MANDATORY_RE = re.compile(
    r"(?:الزامی\s+نیست|اجباری\s+نیست|ضروری\s+نیست|"
    r"not\s+(?:an?\s+)?requirement|not\s+required)",
    re.I,
)


@dataclass(frozen=True, slots=True)
class SourceSkillObligationWarning:
    code: str
    structured_skill: str
    source_span_id: str
    source_span_sha256: str
    source_semantic_sha256: str
    disposition: str = "requires_source_review"


def source_skill_obligation_warnings(
    spine: OriginalSourceSpine,
    source: TranslationSourceVersion,
) -> tuple[SourceSkillObligationWarning, ...]:
    if (
        spine.source_job_id != source.source_job_id
        or spine.detail_version_id != source.job_detail_version_id
        or spine.source_semantic_sha256 != source.semantic_sha256
    ):
        raise ValueError("Source warning inspection requires exact version identity")
    values = source.fields.get("skills")
    if not isinstance(values, list):
        return ()
    results: list[SourceSkillObligationWarning] = []
    seen: set[tuple[str, str]] = set()
    for span in spine.spans:
        if (
            span.kind != "preferred"
            or span.authority_basis != "explicit_item_preference"
            or not _NOT_MANDATORY_RE.search(span.exact_text)
        ):
            continue
        for skill in values:
            if not isinstance(skill, str):
                continue
            name = skill.strip()
            if not 3 <= len(name) <= 64:
                continue
            # The Latin token may have an immediately attached Persian plural
            # suffix (e.g. LLMها), but not an extended Latin identifier.
            if not re.search(
                r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])",
                span.exact_text,
                re.I,
            ):
                continue
            unique = (name.casefold(), span.span_id)
            if unique in seen:
                continue
            seen.add(unique)
            results.append(SourceSkillObligationWarning(
                code="structured_tag_vs_explicit_employer_nonmandatory",
                structured_skill=name,
                source_span_id=span.span_id,
                source_span_sha256=span.text_sha256,
                source_semantic_sha256=spine.source_semantic_sha256,
            ))
    return tuple(results)


__all__ = ["SourceSkillObligationWarning", "source_skill_obligation_warnings"]
