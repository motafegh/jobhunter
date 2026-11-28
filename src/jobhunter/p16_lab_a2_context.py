"""A2 source packet: exact structural context, never a semantic classifier."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from jobhunter.analysis_service import _analysis_fields_for_english
from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.p16_lab import canonical, digest
from jobhunter.p16_lab_inputs import BoundCase, verify_projection
from jobhunter.source_item_candidate_b2_v4_dom import exact_dom_groups
from jobhunter.source_span_identity import (
    align_legacy_english_field,
    bind_original_source_span,
    verify_original_source_anchor,
)
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion

CONTRACT = "p16-e3-a2-context-v1"


def _field_ref(fields, name, index=None):
    field = fields[name]
    value = field if index is None else field[index]
    return {
        "field": name,
        "selector": "/" + name + ("" if index is None else f"/{index}"),
        "field_json_sha256": digest(canonical(field)),
        "value_json_sha256": digest(canonical(value)),
    }


def build_packet(
    source: TranslationSourceVersion,
    *,
    raw_html: bytes,
    html_sha256: str,
    language: str,
    projection: TranslationArtifact | None = None,
) -> dict:
    """L2 needs no translation; L0/L3 use only an associated, hashed v2 projection.

    Keep every description character, including separators, and every incumbent
    user-facing field. DOM flags are structural, not semantic categories.
    """
    if _semantic_sha256(source.fields) != source.semantic_sha256:
        raise ValueError("source semantic digest mismatch")
    if language not in {"L0", "L2", "L3"}:
        raise ValueError("unknown representation")
    if language == "L2" and projection is not None:
        raise ValueError("L2 cannot contain translation aid")
    if language != "L2":
        if projection is None:
            raise ValueError("projection required")
        verify_projection(source, projection)
    groups = exact_dom_groups(source, raw_job_page=raw_html, expected_html_sha256=html_sha256)
    description = source.fields["description"]
    anchors = []
    cursor = 0
    for g in groups:
        if g.char_start < cursor or description[cursor : g.char_start].strip():
            raise ValueError("uncovered or overlapping original text")
        anchor = bind_original_source_span(source, char_start=g.char_start, char_end=g.char_end)
        verify_original_source_anchor(anchor, source)
        if anchor.exact_text != g.exact_text:
            raise ValueError("DOM anchor differs")
        anchors.append((anchor, g, description[cursor : g.char_start]))
        cursor = g.char_end
    if not anchors or description[cursor:].strip():
        raise ValueError("uncovered original description tail")

    units: list[dict[str, Any]] = []

    def add(*, representation, kind, value, reference, **extra):
        units.append(
            {
                "handle": f"g{len(units) + 1}",
                "representation": representation,
                "kind": kind,
                "value": value,
                "reference": reference,
                **extra,
            }
        )

    def original():
        for anchor, g, separator in anchors:
            add(
                representation="original",
                kind="description_group",
                value=anchor.exact_text,
                reference=asdict(anchor),
                separator_before=separator,
                structure={
                    "in_list": g.in_list,
                    "in_emphasis": g.in_emphasis,
                    "in_html_heading": g.in_html_heading,
                },
                association="verified_exact_original",
            )
        for name, value in sorted(_analysis_fields_for_english(source.fields).items()):
            if name == "description":
                continue
            for index, selected in (
                enumerate(value) if isinstance(value, list) and value else ((None, value),)
            ):
                add(
                    representation="original",
                    kind="source_field",
                    value=selected,
                    reference=_field_ref(source.fields, name, index),
                    association="verified_exact_original_field",
                )

    def english():
        assert projection is not None
        alignment = align_legacy_english_field(anchors[0][0], source, projection)
        if alignment.state == "native_english_exact":
            for anchor, g, separator in anchors:
                # Derived references remain distinct even when exact native alignment exists.
                a = align_legacy_english_field(anchor, source, projection)
                add(
                    representation="english_projection",
                    kind="description_group",
                    value=a.english_exact_text,
                    reference={**asdict(a), **_field_ref(projection.fields, "description")},
                    separator_before=separator,
                    structure={
                        "in_list": g.in_list,
                        "in_emphasis": g.in_emphasis,
                        "in_html_heading": g.in_html_heading,
                    },
                    association="verified_native_exact",
                )
        else:
            # Preserve full translated context; no fabricated original child anchors.
            add(
                representation="english_projection",
                kind="description_field",
                value=projection.fields["description"],
                reference={
                    **_field_ref(projection.fields, "description"),
                    "translation_artifact_id": projection.id,
                    "translation_sha256": projection.translation_sha256,
                    "original_field_sha256": digest(description.encode()),
                },
                association="verified_field_only_unaligned",
            )
        for name, value in sorted(_analysis_fields_for_english(projection.fields).items()):
            if name == "description":
                continue
            if name not in source.fields:
                raise ValueError("projection field has no original field")
            # Entire array association only; do not assert index-level translation alignment.
            native = (
                not isinstance(value, list)
                and value == source.fields[name]
                and projection.segment_provenance.get(name) == "native"
            )
            add(
                representation="english_projection",
                kind="source_field",
                value=value,
                reference={
                    **_field_ref(projection.fields, name),
                    "translation_artifact_id": projection.id,
                    "translation_sha256": projection.translation_sha256,
                    "original_field_json_sha256": digest(canonical(source.fields[name])),
                },
                association="verified_native_exact_field"
                if native
                else "verified_field_only_unaligned",
            )

    if language in {"L2", "L3"}:
        original()
    if language in {"L0", "L3"}:
        english()
    packet = {
        "contract_version": CONTRACT,
        "language": language,
        "source": {
            "job_detail_version_id": source.job_detail_version_id,
            "source_job_id": source.source_job_id,
            "semantic_sha256": source.semantic_sha256,
            "fields_sha256": digest(canonical(source.fields)),
            "html_sha256": html_sha256,
        },
        "projection": None
        if projection is None
        else {
            "artifact_id": projection.id,
            "sha256": projection.translation_sha256,
        },
        "units": units,
        "original_description_tail": description[cursor:] if language != "L0" else None,
        "english_description_tail": (
            description[cursor:]
            if projection is not None and projection.fields["description"] == description
            else ""
        )
        if projection is not None
        else None,
    }
    packet["packet_sha256"] = digest(canonical(packet))
    return packet


def packet_for_case(bound: BoundCase, language: str) -> dict:
    return build_packet(
        bound.source,
        raw_html=bound.raw_html,
        html_sha256=bound.original_html_sha256,
        language=language,
        projection=None if language == "L2" else bound.projection,
    )


def verify_packet(packet: dict, bound: BoundCase, *, expected_language: str) -> None:
    if packet != packet_for_case(bound, expected_language):
        raise ValueError("packet identity, scope or content mismatch")


def model_context(packet: dict, bound: BoundCase, *, expected_language: str) -> dict:
    """Verify before exposing context; never send host references or answer keys."""
    verify_packet(packet, bound, expected_language=expected_language)
    return {
        "language": packet["language"],
        "units": [
            {
                k: v
                for k, v in unit.items()
                if k
                in {"handle", "representation", "kind", "value", "separator_before", "structure"}
            }
            | (
                {
                    "field": unit["reference"]["field"],
                    "selector": unit["reference"]["selector"],
                    "surface": "structured_skill_tags"
                    if unit["reference"]["field"] == "skills"
                    else "source_metadata_or_context",
                }
                if unit["kind"] == "source_field"
                else {}
            )
            for unit in packet["units"]
        ],
        "original_description_tail": packet["original_description_tail"],
        "english_description_tail": packet["english_description_tail"],
    }
