"""Source-exact, conservative English vacancy section boundaries.

This is a diagnostic interpretation of an already translated employer source.
It does not create employer facts, alter source bytes, or replace the original
P1.6 validation/acceptance boundary. An unknown heading remains unknown.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

SectionKind = Literal[
    "responsibilities", "requirements", "preferred", "eligibility_middle",
    "eligibility_senior", "arrangement", "application", "context",
]

# Require explicit, syntactically bounded headings: never match incidental
# mentions of an "advantage" or "responsibility" inside a normal sentence.
_HEADINGS = (
    ("responsibilities", (
        r"(?:Main|Key|Primary)\s+Responsibilities\s*:",
        r"Responsibilities\s*:",
        r"What\s+(?:do\s+you\s+do\s+in\s+this\s+role|you(?:'|’)ll\s+do)\s*\?",
        r"Job\s+Description\s*(?=\s*(?:[:：•●]|\n))\s*[:：]?",
        r"Your\s+(?:Tasks|Duties)\s*:",
    )),
    ("requirements", (
        r"Required\s+(?:skills|qualifications|requirements)\s*:",
        r"(?:Required|Minimum)\s+Qualifications\s*:",
        r"(?<!Eligibility\s)Requirements\s*:",
        r"Skills\s+Required\s*:",
        r"(?:Specialized|Technical|General)\s+Conditions\s*:",
        r"Eligibility\s+(?:Criteria|Requirements)\s*:",
        r"What\s+is\s+important\s+to\s+us\s*\?",
    )),
    ("preferred", (
        r"What\s+are\s+considered\s+advantages\s*:",
        r"(?:Advantages|Nice\s+to\s+have|Preferred\s+skills|Preferred\s+qualifications)\s*(?=[:：•●]|\n)",
        r"(?:are\s+scored\s+based\s+on|is\s+considered\s+a\s+score|is\s+considered\s+an\s+advantage)\s*:",
    )),
    ("eligibility_middle", (
        r"(?:Level\s+Middle|Middle\s+Level|Mid(?:dle)?\s+level)\s*:",
    )),
    ("eligibility_senior", (
        r"(?:Level\s+Senior|Senior\s+Level)\s*:",
    )),
    ("arrangement", (
        r"Working\s+Conditions\s*:",
        r"(?:Work\s+)?Location\s*:",
        r"Salary\s*:",
        r"Benefits\s*(?=[:：•●]|\n)",
    )),
    ("context", (
        r"Why\s+collaborate\s+with\s+us\s*\?",
        r"About\s+(?:us|the\s+company)\s*:",
    )),
    ("application", (
        r"How\s+to\s+apply\s*:",
        r"Please\s+send\s+us\s+your\s+resume\s*\.",
    )),
)
_HEADING_RE = re.compile(
    "|".join(
        f"(?P<heading_{kind}>" + "(?:" + "|".join(parts) + "))"
        for kind, parts in _HEADINGS
    ),
    re.IGNORECASE,
)
_BULLET_RE = re.compile(r"[•●]\s*")
# Some translators flatten "requirements" into the end of the preceding
# duty. Only an unambiguous candidate-qualification prefix causes a derived
# transition; there is no source-explicit section inference here.
_QUALIFICATION_BULLET_RE = re.compile(
    r"^(?:Minimum\s+\d+|At\s+least\s+\d+|"
    r"(?:Professional|Practical)\s+experience\b|"
    r"Mastery\s+of\b|Practical\s+familiarity\s+with\b|"
    r"Ability\s+to\s+work\s+independently\b|"
    r"Teamwork\s+spirit\b)",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class SourceSection:
    kind: SectionKind
    text: str
    start: int
    end: int
    heading: str
    heading_start: int
    inferred_boundary: bool = False


def _trimmed_span(value: str, start: int, end: int) -> tuple[int, int]:
    while start < end and value[start].isspace():
        start += 1
    while end > start and value[end - 1].isspace():
        end -= 1
    return start, end


def _bullet_spans(value: str, begin: int, end: int) -> list[tuple[int, int]]:
    bullets = list(_BULLET_RE.finditer(value, begin, end))
    if not bullets:
        start, stop = _trimmed_span(value, begin, end)
        return [(start, stop)] if start < stop else []
    parts = []
    leading = _trimmed_span(value, begin, bullets[0].start())
    if leading[0] < leading[1]:
        parts.append(leading)
    for idx, bullet in enumerate(bullets):
        stop = bullets[idx + 1].start() if idx + 1 < len(bullets) else end
        part = _trimmed_span(value, bullet.end(), stop)
        if part[0] < part[1]:
            parts.append(part)
    return parts


def source_sections(description: str) -> tuple[SourceSection, ...]:
    """Classify only explicit, source-exact English heading spans.

    A sentence outside recognized headings is not silently labeled a duty or
    qualification. A limited, labeled fallback separates an otherwise
    flattened EDR-style bullet sequence at a clear qualification prefix.
    """
    if not isinstance(description, str) or not description.strip():
        return ()
    matches = list(_HEADING_RE.finditer(description))
    if not matches:
        return ()
    result = []
    for index, match in enumerate(matches):
        kind = next(
            k for k, _ in _HEADINGS if match.group(f"heading_{k}") is not None
        )
        heading = match.group()
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(description)
        bullets = _bullet_spans(description, match.end(), stop)
        derived = False
        for start, end in bullets:
            text = description[start:end]
            if kind == "responsibilities" and _QUALIFICATION_BULLET_RE.match(text):
                kind = "requirements"
                derived = True
            result.append(
                SourceSection(
                    kind=kind, text=text, start=start, end=end,
                    heading=heading, heading_start=match.start(),
                    inferred_boundary=derived,
                )
            )
    assert all(description[s.start:s.end] == s.text for s in result)
    return tuple(result)
