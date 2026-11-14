"""Stage B1 source-grounded contract design tests. No production route or database writes."""

from __future__ import annotations

import copy
import hashlib
import json
import runpy
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION
from jobhunter.source_span_identity import bind_original_source_span
from jobhunter.translation_store import (
    TranslationArtifact,
    TranslationSourceVersion,
    TranslationStore,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs/contracts/p16-stage-b1/fixtures"
SCHEMA = ROOT / "docs/contracts/p16-stage-b1/source_evidence_bundle.schema.json"
_design_helpers = runpy.run_path(str(ROOT / "scripts/validate_stage_b1_design.py"))
validate_bundle = _design_helpers["validate_bundle"]
evaluate_eligibility_truth_table = _design_helpers["evaluate_eligibility_truth_table"]
B0 = (
    ROOT / "data/local-acceptance/p16-stage-b0-2026-11-14/frozen"
    / "exposed_original_snapshot.sqlite3"
)
A1 = ("tNhZ", "tMps", "tNDx", "tMjm")


def _load(job: str) -> dict:
    return json.loads((FIXTURES / f"{job}_source_safe_design.json").read_text())


def _item(bundle: dict, identifier: str) -> dict:
    return next(x for x in bundle["items"] if x["item_id"] == identifier)


def _graph(bundle: dict, identifier: str) -> dict:
    return next(x for x in bundle["eligibility_graphs"] if x["graph_id"] == identifier)


def _node(graph: dict, identifier: str) -> dict:
    return next(x for x in graph["nodes"] if x["id"] == identifier)


def test_draft_json_schema_and_four_exposed_fixtures_are_source_safe() -> None:
    Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
    index = json.loads((FIXTURES / "INDEX.json").read_text())
    assert index["fresh_unseen_cases"] == 0
    assert index["semantically_promoted_claims"] == 0
    assert index["raw_source_text_in_git"] is False
    assert not index.get("independent_human_ground_truth_claimed", False)
    assert len(index["examples"]) == 4
    assert {rec["job_id"] for rec in index["examples"]} == set(A1)

    for record in index["examples"]:
        path = ROOT / record["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["json_sha256"]
        content = path.read_text()
        assert len(content) < 60_000
        assert "C:\\Users\\" not in content and "/home/motafeq/" not in content
        assert '"exact_text"' not in content and '"original_description"' not in content
        # Real A1 original employer source remains private, only references are public.
        assert not any("\u0600" <= ch <= "\u06ff" for ch in content)
        bundle = _load(record["job_id"])
        assert bundle["authority"] == "candidate_only_no_downstream_reuse"
        assert bundle["brief"]["state"] == "candidate_only"
        assert bundle["brief"]["downstream_authority"] == "none"
        assert bundle["brief"]["analysis_outcome"] == "not_run"
        assert bundle["source_version"]["semantic_sha256"] == record["source_semantic_sha256"]
        validate_bundle(bundle)


def test_tNhZ_optional_prior_llm_vs_llm_work_and_board_tag() -> None:
    b = _load("tNhZ")
    optional = _item(b, "llm_familiarity_optional")
    duty = _item(b, "ai_feature_duty")
    tag = _item(b, "board_llm_tag")
    assert optional["meaning"]["employer_strength"] == "preferred"
    assert optional["meaning"]["qualifier_status"] == "negative_explicit"
    assert duty["meaning"]["category"] == "work_duty"
    assert duty["meaning"]["employer_strength"] == "not_applicable"
    assert tag["meaning"]["basis"] == "board_metadata_only"
    assert tag["meaning"]["employer_strength"] == "unresolved"
    assert tag["semantic_review"] == "candidate_unreviewed"
    assert len(b["conflicts"]) == 2
    assert {c["type"] for c in b["conflicts"]} == {
        "board_vs_employer_strength", "board_vs_employer_arrangement"
    }


def test_tMps_middle_or_senior_and_one_of_domain_paths_not_global_requirement() -> None:
    b = _load("tMps")
    g = _graph(b, "middle_or_senior")
    assert _node(g, "tracks")["operator"] == "any_of"
    assert set(_node(g, "tracks")["children"]) == {"middle", "senior"}
    assert _node(g, "middle")["operator"] == "all_of"
    assert _node(g, "senior")["operator"] == "all_of"
    assert _node(g, "domain_options")["operator"] == "any_of"
    assert len(_node(g, "domain_options")["children"]) == 5
    assert set(g["basis_item_ids"]) == {"middle_path", "senior_path", "middle_domain_scope"}
    for iid in ("middle_years", "middle_project", "senior_years", "senior_deployment"):
        assert _item(b, iid)["meaning"]["scope"] == "alternative_path"
    for tech in ("LLM", "RAG", "Generative_AI", "Machine_Learning", "NLP"):
        item = _item(b, "domain_" + tech)
        assert item["meaning"]["scope"] == "chosen_option"
        assert item["semantic_review"] == "candidate_unreviewed"
    assert _item(b, "board_experience")["meaning"]["employer_strength"] == "unresolved"


@pytest.mark.parametrize(
    ("qualifications", "expected"),
    [
        (set(), False),
        ({"middle_years", "middle_project"}, False),
        ({"middle_years", "middle_project", "domain_RAG"}, True),
        ({"middle_years", "middle_project", "domain_NLP"}, True),
        ({"middle_years", "domain_RAG"}, False),
        ({"senior_years", "senior_deployment"}, True),
        ({"senior_years"}, False),
        ({"middle_years", "senior_deployment", "domain_LLM"}, False),
    ],
)
def test_middle_or_senior_eligibility_logic_is_preserved(
    qualifications: set[str], expected: bool
) -> None:
    graph = _graph(_load("tMps"), "middle_or_senior")
    assert evaluate_eligibility_truth_table(graph, qualifications) is expected


@pytest.mark.parametrize(
    ("qualifications", "expected"),
    [
        (set(), False),
        ({"certificate"}, True),
        ({"equivalent_knowledge"}, True),
        ({"certificate", "equivalent_knowledge"}, True),
    ],
)
def test_certificate_or_equivalent_logic_is_not_conjunction(
    qualifications: set[str], expected: bool
) -> None:
    graph = _graph(_load("tNDx"), "certificate_or_equivalent")
    assert evaluate_eligibility_truth_table(graph, qualifications) is expected


def test_tNDx_optional_teamwork_unresolved_certificates_and_credential_equivalence() -> None:
    b = _load("tNDx")
    assert _item(b, "teamwork_optional")["meaning"]["employer_strength"] == "preferred"
    assert _item(b, "edr_implementation")["meaning"]["category"] == "work_duty"
    assert _item(b, "remote_customer_support")["meaning"]["category"] == "work_duty"
    assert _item(b, "kaspersky_cert_unclear")["meaning"]["employer_strength"] == "unresolved"
    assert _item(b, "government_client_unclear")["meaning"]["employer_strength"] == "unresolved"
    assert b["brief"]["unresolved_item_ids"] == [
        "kaspersky_cert_unclear", "government_client_unclear"
    ]
    g = _graph(b, "certificate_or_equivalent")
    assert _node(g, "credential_choice")["operator"] == "any_of"
    assert {x["item_id"] for x in g["nodes"] if x["operator"] == "item"} == {
        "certificate", "equivalent_knowledge"
    }
    assert all(
        _item(b, iid)["meaning"]["scope"] == "chosen_option"
        for iid in ("certificate", "equivalent_knowledge")
    )


def test_tMjm_remote_arrangement_is_not_qualification_and_no_fabricated_duties() -> None:
    b = _load("tMjm")
    assert _item(b, "remote_option")["meaning"]["category"] == "work_arrangement"
    assert _item(b, "remote_option")["meaning"]["employer_strength"] == "not_applicable"
    assert _item(b, "conscientiousness")["meaning"]["category"] == "behavioral_expectation"
    assert _item(b, "pentest_capability")["meaning"]["category"] == "candidate_qualification"
    assert not any(i["meaning"]["category"] == "work_duty" for i in b["items"])
    assert _item(b, "education_board")["meaning"]["employer_strength"] == "unresolved"


@pytest.mark.parametrize(
    ("job", "mutate", "message"),
    [
        (
            "tNhZ",
            lambda b: _item(b, "board_llm_tag")["meaning"].update(
                employer_strength="required"
            ),
            "Board metadata",
        ),
        (
            "tNhZ",
            lambda b: _item(b, "llm_familiarity_optional")["meaning"].update(
                employer_strength="required"
            ),
            "Negative explicit",
        ),
        (
            "tNhZ",
            lambda b: b["brief"]["selected_item_ids"].append("board_llm_tag"),
            "Brief cannot promote board metadata",
        ),
        (
            "tNDx",
            lambda b: b["brief"]["selected_item_ids"].append("kaspersky_cert_unclear"),
            "Selected factual items",
        ),
        (
            "tMps",
            lambda b: _item(b, "middle_years")["meaning"].update(scope="standalone"),
            "Alternative graph leaf",
        ),
        (
            "tMps",
            lambda b: _node(_graph(b, "middle_or_senior"), "middle")["children"].append(
                "middle"
            ),
            "Cycle",
        ),
        (
            "tNhZ",
            lambda b: b["alignments"][0].update(
                target={
                    "target_kind": "source_bound_item_output",
                    "target_language": "en",
                    "translation_sha256": "a" * 64,
                    "target_span": {"char_start": 0, "char_end": 2, "text_sha256": "a" * 64},
                    "provider_name": "fixture",
                    "provider_model": "fixture",
                    "prompt_version": "fiction",
                }
            ),
            "Unaligned evidence",
        ),
        (
            "tNhZ",
            lambda b: b["review_events"][0].update(evidence_digest="0" * 64),
            "evidence digest",
        ),
        (
            "tNDx",
            lambda b: _item(b, "teamwork_optional").update(
                semantic_review="independent_source_checked"
            ),
            "Independent item",
        ),
        (
            "tNhZ",
            lambda b: b["review_events"][1].update(finding="independently_checked"),
            "Assistant review",
        ),
        (
            "tNhZ",
            lambda b: b["review_events"][1].update(
                dimension="downstream_authorization"
            ),
            "cannot promote",
        ),
        (
            "tNhZ",
            lambda b: _item(b, "board_llm_tag")["source_ref"].update(
                selector="/skills_fake/0"
            ),
            "Board field reference",
        ),
    ],
)
def test_invariant_breaks_are_rejected(job, mutate, message) -> None:
    altered = copy.deepcopy(_load(job))
    mutate(altered)
    with pytest.raises(ValueError, match=message):
        validate_bundle(altered)


def test_structural_violations_never_become_accepted() -> None:
    b = _load("tMps")
    b["authority"] = "accepted_for_market"
    with pytest.raises(ValueError, match="schema violation"):
        validate_bundle(b)
    b["authority"] = "candidate_only_no_downstream_reuse"
    b["eligibility_graphs"][0]["nodes"].append(
        {"id": "garbage", "operator": "item", "item_id": "middle_years"}
    )
    with pytest.raises(ValueError, match="Unreachable"):
        validate_bundle(b)


def test_optional_private_B0_source_and_v2_translation_validate_exactly(tmp_path: Path) -> None:
    if not B0.exists():
        pytest.skip("Private B0 source evidence is intentionally not available in clean CI")
    # TranslationStore.initialize may configure WAL, so operate on isolated copy
    # and assert the frozen source snapshot remains unchanged.
    sha_before = hashlib.sha256(B0.read_bytes()).hexdigest()
    isolated = tmp_path / "isolated_exposed.sqlite3"
    shutil.copy2(B0, isolated)
    store = TranslationStore(isolated)
    for job in A1:
        source = store.latest_source_version(job)
        translation = store.latest_artifact(job)
        assert source is not None and translation is not None
        validate_bundle(_load(job), source=source, translation=translation)
    assert hashlib.sha256(B0.read_bytes()).hexdigest() == sha_before


def _native_toy() -> tuple[dict, TranslationSourceVersion, TranslationArtifact]:
    desc = "Python backend work."
    source = TranslationSourceVersion(
        source_job_id="syntheticNative",
        job_detail_version_id=999,
        semantic_sha256="a" * 64,
        source_language="en",
        fields={"description": desc},
    )
    translation = TranslationArtifact(
        id=999,
        source_job_id=source.source_job_id,
        job_detail_version_id=source.job_detail_version_id,
        source_semantic_sha256=source.semantic_sha256,
        source_language="en",
        target_language="en",
        provider_name="synthetic",
        provider_model="synthetic",
        translation_schema_version="english-projection-v2",
        fields={"description": desc},
        english_document=desc,
        segment_provenance={"description": "native"},
        translated_segment_count=0,
        native_segment_count=1,
        translation_sha256="b" * 64,
        created_at="2026-11-14T00:00:00+00:00",
    )
    a = bind_original_source_span(source, char_start=0, char_end=6)
    example = {
        "contract_version": "jobhunter-stage-b1-source-evidence-bundle-draft-v1",
        "authority": "candidate_only_no_downstream_reuse",
        "source_version": {
            "source_job_id": source.source_job_id,
            "job_detail_version_id": source.job_detail_version_id,
            "semantic_sha256": source.semantic_sha256,
            "parser_version": "jobinja-detail-v2",
        },
        "items": [
            {
                "item_id": "python_fact",
                "source_ref": {
                    "kind": "original_description_span",
                    "anchor_id": a.anchor_id,
                    "field_path": "description",
                    "field_sha256": a.field_sha256,
                    "text_sha256": a.text_sha256,
                    "char_start": a.char_start,
                    "char_end": a.char_end,
                },
                "meaning": {
                    "category": "candidate_qualification",
                    "employer_strength": "unresolved",
                    "basis": "unresolved",
                    "qualifier_status": "unresolved",
                    "scope": "not_applicable",
                },
                "semantic_review": "candidate_unreviewed",
            }
        ],
        "alignments": [
            {
                "source_item_id": "python_fact",
                "state": "native_english_exact",
                "translation_artifact_id": translation.id,
                "translation_sha256": translation.translation_sha256,
                "target": {
                    "target_kind": "native_exact_v2",
                    "target_language": "en",
                    "translation_artifact_id": translation.id,
                    "translation_schema_version": "english-projection-v2",
                    "translation_sha256": translation.translation_sha256,
                    "target_span": {
                        "char_start": 0,
                        "char_end": 6,
                        "text_sha256": a.text_sha256,
                    },
                },
                "meaning_review": "unreviewed",
            }
        ],
        "eligibility_graphs": [],
        "conflicts": [],
        "review_events": [],
        "brief": {
            "state": "candidate_only",
            "selected_item_ids": [],
            "unresolved_item_ids": ["python_fact"],
            "analysis_outcome": "not_run",
            "downstream_authority": "none",
        },
    }
    return example, source, translation


def test_synthetic_native_english_identity_and_stale_source_are_checked() -> None:
    from dataclasses import replace

    bundle, source, translation = _native_toy()
    validate_bundle(bundle, source=source, translation=translation)
    modified = replace(translation, fields={"description": "Altered"})
    with pytest.raises(ValueError, match="Native-English"):
        validate_bundle(bundle, source=source, translation=modified)
    other_source = replace(source, semantic_sha256="c" * 64)
    with pytest.raises(ValueError, match="Stale original source"):
        validate_bundle(bundle, source=other_source, translation=translation)


def test_synthetic_source_bound_association_and_one_to_many_do_not_imply_fidelity() -> None:
    bundle, source, _ = _native_toy()
    bundle["alignments"] = []
    for sha in ("c" * 64, "d" * 64):
        bundle["alignments"].append({
            "source_item_id": "python_fact",
            "state": "source_bound_translation_candidate",
            "translation_artifact_id": None,
            "translation_sha256": sha,
            "target": {
                "target_kind": "source_bound_item_output",
                "target_language": "en",
                "provider_name": "synthetic-local-provider",
                "provider_model": "synthetic",
                "prompt_version": "b1-design-only",
                "translation_sha256": sha,
                "target_span": {
                    "char_start": 0,
                    "char_end": 6,
                    "text_sha256": "e" * 64,
                },
            },
            "meaning_review": "unreviewed",
        })
    validate_bundle(bundle, source=source)
    assert bundle["brief"]["downstream_authority"] == "none"
    assert all(x["meaning_review"] == "unreviewed" for x in bundle["alignments"])
    rejected = copy.deepcopy(bundle)
    rejected["alignments"][1]["translation_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="SHA mismatch"):
        validate_bundle(rejected, source=source)


def test_design_only_does_not_change_accepted_analysis_route() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v30"
    assert not (ROOT / "src/jobhunter/source_bound_translation_v1.py").exists()


def test_review_dimension_cannot_impersonate_semantic_classification() -> None:
    assistant = _load("tNhZ")
    event = next(
        e for e in assistant["review_events"]
        if e["item_id"] == "llm_familiarity_optional"
        and e["dimension"] == "semantic_classification"
    )
    event["dimension"] = "translation_association"
    with pytest.raises(ValueError, match="Assistant-checked item"):
        validate_bundle(assistant)

    independent = _load("tNDx")
    item = _item(independent, "teamwork_optional")
    item["semantic_review"] = "independent_source_checked"
    event = next(
        e for e in independent["review_events"]
        if e["item_id"] == "teamwork_optional"
        and e["dimension"] == "semantic_classification"
    )
    event["reviewer_kind"] = "owner"
    event["finding"] = "independently_checked"
    event["dimension"] = "translation_association"
    with pytest.raises(ValueError, match="Independent item"):
        validate_bundle(independent)


@pytest.mark.parametrize("selector", ["/skills/03", "/skills/~2", "/skills/٤", "/skills/-1"])
def test_draft_board_json_pointer_rejects_noncanonical_list_selection(
    selector: str,
) -> None:
    from jobhunter.translation_store import TranslationSourceVersion

    source = TranslationSourceVersion(
        source_job_id="pointerFixture",
        job_detail_version_id=1,
        semantic_sha256="a" * 64,
        source_language="fa",
        fields={"skills": ["one", "two", "three", "four"]},
    )
    pointer = _design_helpers["_selected_value"]
    with pytest.raises(ValueError, match="selector|Pointer"):
        pointer(source, selector)
