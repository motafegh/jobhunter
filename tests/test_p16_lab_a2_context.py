"""Frozen binding and A2 context controls using synthetic source only."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace

import pytest
from test_p16_lab import root  # noqa: F401

from jobhunter.jobinja_detail_service import _semantic_sha256
from jobhunter.jobinja_details import _strip_html
from jobhunter.p16_lab import digest
from jobhunter.p16_lab_a2_context import (
    build_packet,
    model_context,
    packet_for_case,
    verify_packet,
)
from jobhunter.p16_lab_inputs import BoundCase, bind_case, bind_cell, projection_digest
from jobhunter.translation_store import TranslationArtifact, TranslationSourceVersion


def fixture(*, native=False):
    repeated = "Build APIs." if native else "ساخت API."
    markup = (
        "<p>Introduction</p><h2>Responsibilities</h2><ul>"
        f"<li>{repeated}</li><li>{repeated}</li></ul><p>Final context</p>"
    )
    html = (
        '<script type="application/ld+json">'
        + json.dumps({"@type": "JobPosting", "description": markup}, ensure_ascii=False)
        + "</script>"
    ).encode()
    fields = {
        "description": _strip_html(markup),
        "title": "Engineer",
        "company_description": "Company context",
        "skills": ["Go", "Go"],
        "education": None,
        "language": "mixed",
        "parser_version": "jobinja-detail-v2",
    }
    source = TranslationSourceVersion("fixture", 1, _semantic_sha256(fields), "mixed", fields)
    eng = {**fields, "description": fields["description"] if native else "English projection only."}
    translation = TranslationArtifact(
        1,
        "fixture",
        1,
        source.semantic_sha256,
        "mixed",
        "en",
        "fixture",
        "fixture",
        "english-projection-v2",
        eng,
        eng["description"],
        {"description": "native" if native else "translated", "title": "native"},
        int(not native),
        int(native),
        "",
        "fixture",
    )
    translation = replace(translation, translation_sha256=projection_digest(translation))
    return BoundCase("D1", "nov23", "a" * 64, "b" * 64, source, translation, digest(html), html)


@pytest.mark.parametrize("language", ["L0", "L2", "L3"])
@pytest.mark.parametrize("native", [False, True])
def test_exact_context_and_representation(language, native):
    b = fixture(native=native)
    p = packet_for_case(b, language)
    verify_packet(p, b, expected_language=language)
    context = model_context(p, b, expected_language=language)
    assert len({u["handle"] for u in p["units"]}) == len(p["units"])
    assert "reference" not in json.dumps(context)
    assert "semantic_sha256" not in json.dumps(context)
    assert "source_job_id" not in json.dumps(context)
    for representation, expected in (
        ("original", b.source.fields["description"]),
        ("english_projection", b.projection.fields["description"]),
    ):
        units = [
            u
            for u in p["units"]
            if u["representation"] == representation and u["kind"].startswith("description")
        ]
        present = (representation == "original" and language != "L0") or (
            representation == "english_projection" and language != "L2"
        )
        assert bool(units) == present
        if present:
            tail = p[
                "original_description_tail"
                if representation == "original"
                else "english_description_tail"
            ]
            assert (
                "".join(u.get("separator_before", "") + u["value"] for u in units) + tail
                == expected
            )
    if language == "L0" and not native:
        assert "ساخت" not in json.dumps(context, ensure_ascii=False)
        translated = p["units"][0]
        assert translated["association"] == "verified_field_only_unaligned"
        assert "source_anchor_id" not in translated["reference"]
    if language == "L2":
        assert p["projection"] is None
        assert "English projection only." not in json.dumps(context)
    assert all(
        u["surface"] == "structured_skill_tags"
        for u in context["units"]
        if u.get("field") == "skills"
    )


def test_repeat_and_unicode_anchors():
    b = fixture()
    p = packet_for_case(b, "L2")
    repeat = [u for u in p["units"] if u["value"] == "ساخت API."]
    assert len(repeat) == 2
    assert repeat[0]["reference"]["anchor_id"] != repeat[1]["reference"]["anchor_id"]
    for u in repeat:
        r = u["reference"]
        assert (
            b.source.fields["description"].encode()[r["utf8_start"] : r["utf8_end"]]
            == u["value"].encode()
        )
    tags = [u for u in p["units"] if u["reference"].get("field") == "skills"]
    assert [u["reference"]["selector"] for u in tags] == ["/skills/0", "/skills/1"]


@pytest.mark.parametrize("mutation", ["value", "handle", "missing", "association", "foreign"])
def test_packet_rejects_tamper(mutation):
    b = fixture()
    p = deepcopy(packet_for_case(b, "L3"))
    if mutation == "value":
        p["units"][0]["value"] = "changed"
    elif mutation == "handle":
        p["units"][0]["handle"] = p["units"][1]["handle"]
    elif mutation == "missing":
        p["units"].pop(0)
    elif mutation == "association":
        p["units"][-1]["association"] = "verified_native_exact"
    else:
        b = replace(b, source=replace(b.source, job_detail_version_id=2))
    with pytest.raises(ValueError):
        model_context(p, b, expected_language="L3")


def test_wrong_language_refused():
    b = fixture()
    with pytest.raises(ValueError):
        model_context(packet_for_case(b, "L3"), b, expected_language="L0")


@pytest.mark.parametrize("change", ["hash", "version", "fields", "native", "html"])
def test_packet_rejects_bad_input(change):
    b = fixture()
    if change == "hash":
        b = replace(b, projection=replace(b.projection, translation_sha256="f" * 64))
    elif change == "version":
        b = replace(b, projection=replace(b.projection, job_detail_version_id=2))
    elif change == "fields":
        b = replace(b, source=replace(b.source, fields={**b.source.fields, "title": "changed"}))
    elif change == "native":
        t = replace(b.projection, segment_provenance={"description": "native"})
        b = replace(b, projection=replace(t, translation_sha256=projection_digest(t)))
    else:
        b = replace(b, raw_html=b.raw_html + b"x")
    with pytest.raises(ValueError):
        packet_for_case(b, "L0")


def test_l2_independent_of_translation():
    b = fixture()
    p = build_packet(
        b.source, raw_html=b.raw_html, html_sha256=b.original_html_sha256, language="L2"
    )
    assert p["projection"] is None
    with pytest.raises(ValueError):
        build_packet(
            b.source,
            raw_html=b.raw_html,
            html_sha256=b.original_html_sha256,
            language="L2",
            projection=b.projection,
        )


def test_missing_private_manifest_and_unknown_cell(request):
    r = request.getfixturevalue("root")
    with pytest.raises(FileNotFoundError):
        bind_case("D1", r)
    with pytest.raises(ValueError, match="unknown frozen schedule"):
        bind_cell("invented", r)
