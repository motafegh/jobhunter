"""B2 nested eligibility candidates: source integrity and Boolean design proof.

These are exposed / synthetic development cases, not human-reviewed
employer policies and not applicant matching.
"""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from runpy import run_path

import pytest

from jobhunter.source_eligibility_candidate_b2 import build_candidate_eligibility_logic
from jobhunter.source_item_candidate_b2 import interpret_original_source_candidate
from jobhunter.source_span_identity import verify_original_source_anchor
from jobhunter.translation_store import TranslationSourceVersion, TranslationStore

ROOT = Path(__file__).resolve().parents[1]
B0 = ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen/exposed_original_snapshot.sqlite3"
PROJECTION = run_path(str(ROOT / "scripts/diagnose_stage_b2_candidate.py"))["b1_design_from_b2"]
HELPER = run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))
VALIDATE = HELPER["validate_bundle"]
EVALUATE = HELPER["evaluate_eligibility_truth_table"]


def _source(text: str) -> TranslationSourceVersion:
    return TranslationSourceVersion(
        source_job_id="syntheticEligibility",
        job_detail_version_id=42,
        semantic_sha256="a" * 64,
        source_language="fa",
        fields={"description": text, "parser_version": "jobinja-detail-v2"},
    )


def _frozen(job: str) -> TranslationSourceVersion:
    if not B0.exists():
        pytest.skip("Private frozen source not present on public CI")
    result = TranslationStore(B0).latest_source_version(job)
    assert result is not None
    return result


def _bundle(source: TranslationSourceVersion) -> tuple[dict, object]:
    candidate = interpret_original_source_candidate(source)
    logic = build_candidate_eligibility_logic(source, candidate)
    bundle = PROJECTION(candidate, source)
    VALIDATE(bundle, source=source)
    assert bundle["authority"] == "candidate_only_no_downstream_reuse"
    assert bundle["review_events"] == []
    assert bundle["brief"]["state"] == "candidate_only"
    assert not bundle["brief"]["selected_item_ids"]
    assert bundle["brief"]["downstream_authority"] == "none"
    return bundle, logic


def _labels(bundle: dict) -> dict[str, str]:
    return {
        i["meaning"]["concept_label"]: i["item_id"]
        for i in bundle["items"]
        if i["meaning"].get("concept_label")
    }


def test_two_complete_source_owned_candidate_graphs_on_exposed_jobs() -> None:
    for job, expected, leaf_count in (
        ("tMps", "candidate_middle_or_senior", 9),
        ("tNDx", "candidate_certificate_or_knowledge", 2),
    ):
        source = _frozen(job)
        bundle, logic = _bundle(source)
        assert len(logic.graphs) == 1
        assert logic.unresolved_group_kinds == ()
        graph = logic.graphs[0]
        assert graph.graph_id == expected
        assert graph.interpretation_state == "candidate_unreviewed_not_eligibility_authority"
        assert len([n for n in graph.nodes if n["operator"] == "item"]) == leaf_count
        assert len(bundle["eligibility_graphs"]) == 1
        for leaf in graph.leaves:
            verify_original_source_anchor(leaf.anchor, source)
            assert (
                leaf.anchor.exact_text
                == (source.fields["description"][leaf.anchor.char_start : leaf.anchor.char_end])
            )
            assert (
                leaf.anchor.exact_text.encode()
                == (
                    source.fields["description"].encode()[
                        leaf.anchor.utf8_start : leaf.anchor.utf8_end
                    ]
                )
            )
            assert hashlib.sha256(leaf.anchor.exact_text.encode()).hexdigest() == (
                leaf.anchor.text_sha256
            )
        assert all(x["semantic_review"] == "candidate_unreviewed" for x in bundle["items"])


@pytest.mark.parametrize(
    ("labels", "valid"),
    [
        ((), False),
        (("middle_years", "domain_0", "middle_project"), True),
        (("middle_years", "domain_4", "middle_project"), True),
        (("middle_years", "middle_project"), False),
        (("middle_years", "domain_0"), False),
        (("domain_0", "middle_project"), False),
        (("middle_years", "domain_0", "senior_deployment"), False),
        (("senior_years", "senior_deployment"), True),
        (("senior_years",), False),
        (("senior_deployment",), False),
        (("middle_years", "senior_deployment"), False),
        (("senior_years", "domain_2", "middle_project"), False),
        (("middle_years", "domain_2", "middle_project", "senior_years"), True),
    ],
)
def test_middle_or_senior_truth_table_not_cross_track_mixing(
    labels: tuple[str, ...], valid: bool
) -> None:
    bundle, _ = _bundle(_frozen("tMps"))
    ids = _labels(bundle)
    assert {x for x in labels} <= ids.keys()
    selected = {ids[x] for x in labels}
    assert EVALUATE(bundle["eligibility_graphs"][0], selected) is valid


@pytest.mark.parametrize(
    ("labels", "valid"),
    [
        ((), False),
        (("certificate",), True),
        (("knowledge",), True),
        (("certificate", "knowledge"), True),
    ],
)
def test_certificate_or_equivalent_truth_table(labels: tuple[str, ...], valid: bool) -> None:
    bundle, _ = _bundle(_frozen("tNDx"))
    ids = _labels(bundle)
    assert (
        EVALUATE(
            bundle["eligibility_graphs"][0],
            {ids[x] for x in labels},
        )
        is valid
    )


def test_partial_track_syntax_is_undecoded_not_invented() -> None:
    text = (
        "شرایط احراز: سطح Middle: دارا بودن یک تا سه سال تجربه کاری مرتبط، "
        "به همراه تجربه عملی در یکی از حوزه‌های Vision، Data یا NLP "
        "و حداقل یک پروژه عملی اجرا شده "
        "سطح Senior: دارا بودن شش تا هشت سال تجربه کاری مرتبط، "
        "تجربه طراحی و Production Deployment حداقل یک سیستم ML"
    )
    source = _source(text)
    candidate = interpret_original_source_candidate(source)
    result = build_candidate_eligibility_logic(source, candidate)
    # Ambiguous comma/OR mix is not one of our admitted, explicit patterns.
    assert not result.graphs
    assert "seniority_tracks" in result.unresolved_group_kinds
    draft = PROJECTION(candidate, source)
    VALIDATE(draft, source=source)
    assert draft["eligibility_graphs"] == []


def test_certificate_and_equivalent_is_not_an_or_graph() -> None:
    source = _source("نیازمندی‌ها • تسلط بر مفاهیم شبکه (دارای گواهینامه و دانش معادل)")
    bundle, result = _bundle(source)
    assert bundle["eligibility_graphs"] == []
    assert result.graphs == ()


def test_modifying_source_invalidates_nested_graph_refs() -> None:
    source = _frozen("tNDx")
    bundle, _ = _bundle(source)
    tampered = copy.deepcopy(bundle)
    conditional = next(
        i for i in tampered["items"] if i["meaning"].get("concept_label") == "certificate"
    )
    conditional["source_ref"]["char_start"] += 1
    with pytest.raises(ValueError, match="Original source anchor|match|B1"):
        VALIDATE(tampered, source=source)


def test_qualifications_from_unresolved_bare_certificates_never_added_as_leaves() -> None:
    source = _frozen("tNDx")
    bundle, _ = _bundle(source)
    leaf_ids = {
        node["item_id"]
        for graph in bundle["eligibility_graphs"]
        for node in graph["nodes"]
        if node["operator"] == "item"
    }
    item_by_id = {item["item_id"]: item for item in bundle["items"]}
    assert len(leaf_ids) == 2
    for id_ in leaf_ids:
        assert item_by_id[id_]["meaning"]["scope"] == "chosen_option"
    assert not any(
        item["meaning"]["employer_strength"] == "required"
        and item["meaning"].get("concept_label", "").startswith("Kaspersky")
        for item in bundle["items"]
    )


def test_nonapplicable_cases_have_no_eligibility_graphs() -> None:
    for job in ("tNhZ", "tMjm"):
        bundle, logic = _bundle(_frozen(job))
        assert logic.graphs == ()
        assert bundle["eligibility_graphs"] == []


def test_generalized_synthetic_supported_nested_tracks_and_domain_options() -> None:
    # Invented role, years and domains; not copied from any retained employer ad.
    source = _source(
        "شرایط احراز: سطح Middle: دارا بودن یک تا سه سال تجربه کاری مرتبط، "
        "به همراه تجربه عملی در یکی از حوزه‌های Vision، Data Science، NLP "
        "و حداقل یک پروژه عملی اجرا شده "
        "سطح Senior: دارا بودن شش تا هشت سال تجربه کاری مرتبط، "
        "تجربه طراحی و Production Deployment حداقل یک سیستم ML"
    )
    bundle, logic = _bundle(source)
    assert logic.unresolved_group_kinds == ()
    assert len(bundle["eligibility_graphs"]) == 1
    graph = bundle["eligibility_graphs"][0]
    assert graph["graph_id"] == "candidate_middle_or_senior"
    assert graph["review_state"] == "candidate"
    ids = _labels(bundle)
    assert {
        x for x in ("domain_0", "domain_1", "domain_2", "middle_project", "senior_years")
    } <= ids.keys()
    yes = {ids[x] for x in ("middle_years", "domain_1", "middle_project")}
    assert EVALUATE(graph, yes)
    no = {ids[x] for x in ("middle_years", "domain_1", "senior_deployment")}
    assert not EVALUATE(graph, no)
