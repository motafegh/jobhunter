"""Candidate-only source-bound translation support for P1.6 Stage B3.

This module does not write to the application database or promote employer facts.
"""

from __future__ import annotations

import hashlib
import re
import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import httpx

from jobhunter.source_item_candidate_b2 import SourceItemCandidate
from jobhunter.translation.projection import contains_persian

B3_CONTRACT_VERSION = "jobhunter-p16-b3-source-bound-item-translation-candidate-v1"
B3_SELECTION_VERSION = "jobhunter-p16-b3-exposed-item-selection-v1"

# These are the two generic application instructions deliberately deferred
# from the Python/AI trading-product ad. They are not employer requirements.
B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS = frozenset(
    {
        "6c38de3053085c6ec5da0a02d5d3ea051701f66c47468aa3fd7baa409a984ff7",
        "a7235680642e3b8dc6c96cc5cdd4ad6a9f62f6540edc19637226ca0a8ba04ac9",
    }
)

# Keep all three EDR exam-related statements in scope, including the
# final-acceptance technical entrance-exam condition.
B3_REQUIRED_TNDX_EXAM_ANCHORS = frozenset(
    {
        "82be628c79c6cb5e3142862154f771945adb809dc318124759984cea8b8eb6e8",
        "17193d59122fbc99d34abfe6b516fb7b0d8d41ac42afe18c29860bc4c0e56d69",
        "580d9b8a4ccb7f042da732b483e97ee953f9272e63c639ea0ddb2a74bcb2ff11",
    }
)

_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789",
)
_PERSIAN_NEGATION = re.compile(
    r"(?<!\w)(?:الزامی\s+نیست|ضروری\s+نیست|نیازی\s+نیست|نیست|نباید|بدون|عدم|ندارد)(?!\w)",
    re.I,
)
_ENGLISH_NEGATION = re.compile(
    r"\b(?:not|without|no|optional|doesn't|do not|isn't|aren't|never|cannot|can't)\b",
    re.I,
)
_PERSIAN_PREFERENCE = re.compile(
    r"(?:مزیت|ترجیح|امتیاز|در\s+اولویت|بهتر\s+است)",
    re.I,
)
_ENGLISH_PREFERENCE = re.compile(
    r"\b(?:preferred|preference|advantage|benefit|bonus|plus|desirable|nice to have)\b",
    re.I,
)
_ENGLISH_MANDATORY = re.compile(
    r"\b(?:required|mandatory|must|required to|proficient|expert)\b",
    re.I,
)
_PERSIAN_ALTERNATIVE = re.compile(
    r"(?<!\w)یا(?!\w)|(?<!\w)معادل(?!\w)|(?<!\w)به\s+جای(?!\w)|در\s+غیر\s+این\s+صورت"
)
_ENGLISH_ALTERNATIVE = re.compile(r"\b(?:or|equivalent|instead of|alternative)\b", re.I)
_ENGLISH_SECTION_HEADING = re.compile(
    r"^\s*(?:responsibilities|requirements|qualifications|advantages|benefits|"
    r"job description|duties|about the role)\s*:\s*",
    re.I,
)
_PERSIAN_EXAM = re.compile(r"(?:آزمون|امتحان)")
_ENGLISH_EXAM = re.compile(r"\b(?:exam|examination|test(?:ing)?|assessment)\b", re.I)
_PERSIAN_WORK_MODE = re.compile(r"(?:دورکاری|تمام\s*وقت|پاره\s*وقت|حضوری|ترکیبی)")
_ENGLISH_WORK_MODE = re.compile(
    r"\b(?:remote|work from home|full[ -]time|part[ -]time|on[ -]site|hybrid)\b",
    re.I,
)
_NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


@dataclass(frozen=True, slots=True)
class B3Selection:
    translate_items: tuple[SourceItemCandidate, ...]
    native_identity_items: tuple[SourceItemCandidate, ...]
    excluded_items: tuple[tuple[SourceItemCandidate, str], ...]


def select_b3_items(
    source_job_id: str,
    items: Sequence[SourceItemCandidate],
) -> B3Selection:
    """Select exact B2 source items under the frozen exposed-cohort rule."""
    item_tuple = tuple(items)
    anchor_ids = {item.anchor.anchor_id for item in item_tuple}

    if source_job_id == "tNhZ":
        observed_application_ids = {
            item.anchor.anchor_id
            for item in item_tuple
            if item.category == "application_instruction"
        }
        if observed_application_ids != B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS:
            raise ValueError(
                "tNhZ application-instruction inventory changed from the frozen B3 selection"
            )

    if source_job_id == "tNDx":
        missing_exam_items = B3_REQUIRED_TNDX_EXAM_ANCHORS - anchor_ids
        if missing_exam_items:
            raise ValueError("Frozen EDR exam-related source items are missing")

    translate: list[SourceItemCandidate] = []
    native: list[SourceItemCandidate] = []
    excluded: list[tuple[SourceItemCandidate, str]] = []

    for item in item_tuple:
        anchor_id = item.anchor.anchor_id
        if item.category == "context":
            excluded.append((item, "context_only"))
        elif source_job_id == "tNhZ" and anchor_id in B3_EXCLUDED_TNHZ_APPLICATION_ANCHORS:
            excluded.append((item, "generic_application_instruction"))
        elif contains_persian(item.anchor.exact_text):
            translate.append(item)
        else:
            native.append(item)

    return B3Selection(
        translate_items=tuple(translate),
        native_identity_items=tuple(native),
        excluded_items=tuple(excluded),
    )


def build_translation_review_flags(source_text: str, target_text: str) -> tuple[str, ...]:
    """Emit non-authoritative lexical warnings; never certify semantic fidelity."""
    source = source_text.translate(_DIGITS)
    target = target_text.translate(_DIGITS)
    flags: list[str] = []

    if _PERSIAN_NEGATION.search(source) and not _ENGLISH_NEGATION.search(target):
        flags.append("negation_cue_not_obvious")
    if _PERSIAN_PREFERENCE.search(source):
        if _ENGLISH_MANDATORY.search(target) and not re.search(
            r"\bnot\s+(?:required|mandatory|necessary)\b", target, re.I
        ):
            flags.append("possible_preference_to_mandatory_shift")
        elif not _ENGLISH_PREFERENCE.search(target):
            flags.append("preference_cue_not_obvious")
    if _PERSIAN_ALTERNATIVE.search(source) and not _ENGLISH_ALTERNATIVE.search(target):
        flags.append("alternative_or_equivalence_cue_not_obvious")

    source_numbers = set(_NUMBER.findall(source))
    target_numbers = set(_NUMBER.findall(target))
    if source_numbers - target_numbers:
        flags.append("numeric_value_not_obvious")

    if _PERSIAN_EXAM.search(source) and not _ENGLISH_EXAM.search(target):
        flags.append("entrance_exam_term_not_obvious")
    if _PERSIAN_WORK_MODE.search(source) and not _ENGLISH_WORK_MODE.search(target):
        flags.append("work_mode_term_not_obvious")
    if re.search(r"وظیفه[\u200c\s]*شناس", source) and not re.search(
        r"\bconscientious", target, re.I
    ):
        flags.append("conscientiousness_translation_needs_review")
    if _ENGLISH_SECTION_HEADING.match(target) and not re.match(
        r"^\s*[A-Za-z][^:]{0,60}:\s*$", source
    ):
        flags.append("possible_added_section_heading")

    # Preserve explicit Latin technical/product tokens as a warning-only check.
    for token in re.findall(r"\b[A-Za-z][A-Za-z0-9.+/#-]{1,}\b", source):
        if token.casefold() not in target.casefold():
            flags.append(f"technical_token_not_obvious:{token}")
    return tuple(dict.fromkeys(flags))


def make_native_identity_record(
    *,
    source_job_id: str,
    source_item_id: str,
    item: SourceItemCandidate,
) -> dict[str, Any]:
    text = item.anchor.exact_text
    if contains_persian(text):
        raise ValueError("Native identity requires a source item without Persian text")
    digest = sha256_text(text)
    if digest != item.anchor.text_sha256:
        raise ValueError("Native identity source digest does not match its anchor")
    return {
        "contract_version": B3_CONTRACT_VERSION,
        "source_job_id": source_job_id,
        "source_item_id": source_item_id,
        "source_anchor_id": item.anchor.anchor_id,
        "source_semantic_sha256": item.anchor.semantic_sha256,
        "source_field_sha256": item.anchor.field_sha256,
        "source_span_sha256": item.anchor.text_sha256,
        "source_char_start": item.anchor.char_start,
        "source_char_end": item.anchor.char_end,
        "source_heading_context": item.heading,
        "source_heading_context_sha256": (
            sha256_text(item.heading) if item.heading is not None else None
        ),
        "input_kind": "native_english_exact_source_item",
        "state": "native_identity",
        "target_language": "en",
        "target_text": text,
        "target_sha256": digest,
        "target_char_start": 0,
        "target_char_end": len(text),
        "meaning_review": "unreviewed",
        "provider_name": None,
        "provider_model": None,
        "prompt_version": None,
        "model_request_count": 0,
        "http_completion_attempt_count": 0,
        "review_flags": [],
    }


def make_b1_source_bound_alignment(
    *,
    source_item_id: str,
    target_text: str,
    provider_name: str,
    provider_model: str,
    prompt_version: str,
) -> dict[str, Any]:
    digest = sha256_text(target_text)
    if not target_text.strip() or contains_persian(target_text):
        raise ValueError("A B1 source-bound English target must be nonempty English text")
    return {
        "source_item_id": source_item_id,
        "state": "source_bound_translation_candidate",
        "translation_artifact_id": None,
        "translation_sha256": digest,
        "target": {
            "target_kind": "source_bound_item_output",
            "target_language": "en",
            "translation_sha256": digest,
            "target_span": {
                "char_start": 0,
                "char_end": len(target_text),
                "text_sha256": digest,
            },
            "provider_name": provider_name,
            "provider_model": provider_model,
            "prompt_version": prompt_version,
        },
        "meaning_review": "unreviewed",
    }


def make_b1_unresolved_alignment(source_item_id: str) -> dict[str, Any]:
    """Represent absence of a B1-compatible target without inventing offsets."""
    return {
        "source_item_id": source_item_id,
        "state": "unresolved",
        "translation_artifact_id": None,
        "translation_sha256": None,
        "target": None,
        "meaning_review": "unreviewed",
    }


@dataclass(slots=True)
class CapturedHTTPEvent:
    method: str
    url_path: str
    request_body: bytes
    response_status: int | None
    response_body: bytes | None
    error_type: str | None
    elapsed_seconds: float


class CapturingHTTPTransport(httpx.BaseTransport):
    """Capture local request/response bodies without persisting auth headers."""

    def __init__(self, inner: httpx.BaseTransport | None = None) -> None:
        self._inner = inner or httpx.HTTPTransport(trust_env=False, retries=0)
        self.events: list[CapturedHTTPEvent] = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        started = time.perf_counter()
        request_body = b""
        response_status: int | None = None
        response_body: bytes | None = None
        error_type: str | None = None
        try:
            request_body = request.read()
            response = self._inner.handle_request(request)
            response_body = response.read()
            response_status = response.status_code
            return response
        except Exception as exc:
            error_type = type(exc).__name__
            raise
        finally:
            self.events.append(
                CapturedHTTPEvent(
                    method=request.method,
                    url_path=request.url.path,
                    request_body=request_body,
                    response_status=response_status,
                    response_body=response_body,
                    error_type=error_type,
                    elapsed_seconds=time.perf_counter() - started,
                )
            )

    def close(self) -> None:
        # LMStudioTranslationProvider creates a short-lived httpx.Client for
        # each request. Keep this shared capture transport open until the run ends.
        return None

    def close_inner(self) -> None:
        self._inner.close()


def nested_leaf_parent_relations(
    *,
    candidate_items: Sequence[SourceItemCandidate],
    nested_leaf_anchors: Sequence[Any],
) -> tuple[dict[str, str], ...]:
    """Prove each eligibility leaf is contained by one selected parent source item."""
    relations: list[dict[str, str]] = []
    for leaf in nested_leaf_anchors:
        parents = [
            item
            for item in candidate_items
            if item.anchor.field_path == leaf.field_path
            and item.anchor.char_start <= leaf.char_start
            and item.anchor.char_end >= leaf.char_end
        ]
        if len(parents) != 1:
            raise ValueError("Eligibility leaf is not contained by exactly one parent source item")
        parent = parents[0]
        relations.append(
            {
                "leaf_anchor_id": leaf.anchor_id,
                "leaf_text_sha256": leaf.text_sha256,
                "parent_anchor_id": parent.anchor.anchor_id,
                "parent_text_sha256": parent.anchor.text_sha256,
                "target_subspan_alignment": "not_established",
            }
        )
    return tuple(relations)
