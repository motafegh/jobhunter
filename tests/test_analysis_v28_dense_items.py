"""Source-exact dense residual and trait ownership in isolated v28."""

import json
from pathlib import Path

from jobhunter.analysis_current import ENGLISH_PROMPT_VERSION as CURRENT_PROMPT
from jobhunter.analysis_runtime_v15 import _v15_candidate_evidence_view
from jobhunter.analysis_runtime_v28 import V28CandidateAnalysisProvider
from jobhunter.analysis_service_v13 import decomposed_requirement_references
from jobhunter.analysis_service_v28 import ENGLISH_PROMPT_VERSION
from jobhunter.evidence_refs_v28 import persisted_qualification_plan_v28

_ROOT = Path(__file__).resolve().parents[1]


def _fields(job: str) -> dict:
    return json.loads(
        (_ROOT / f"corpus/jobs/{job}/english-projection.json").read_text(
            encoding="utf-8"
        )
    )["fields"]


def test_t7Ay_dense_required_residual_has_eight_exact_items() -> None:
    fields = _fields("t7Ay")
    plan = persisted_qualification_plan_v28(fields)
    residual = plan["field:__candidate_residual_requirement_evidence:0"]
    items = residual["required_item_excerpts"]
    assert len(items) == 8
    assert not residual["allow_exclusion"]
    assert all(item["text"] in residual["text"] for item in items)
    assert any("Prompt Engineering" in item["text"] for item in items)
    assert any("Python programming" in item["text"] for item in items)
    assert any("APIs and Backend" in item["text"] for item in items)
    effective, _, _, additional = _v15_candidate_evidence_view(fields)
    provider = object.__new__(V28CandidateAnalysisProvider)
    generation = provider._inherited_additional_plan(
        effective, additional, decomposed_requirement_references(fields)
    )
    assert generation["field:__candidate_residual_requirement_evidence:0"] == residual


def test_tmvA_trait_statement_is_one_exact_source_fact() -> None:
    provider = object.__new__(V28CandidateAnalysisProvider)
    plan = persisted_qualification_plan_v28(_fields("tmvA"))
    refs, claims = provider._source_quoted_requirements(plan)
    reference = "field:description:segment:3:sentence:0"
    assert reference in refs
    claim = claims[refs.index(reference)]
    assert claim["concept"] == claim["evidence"] == plan[reference]["text"]
    assert claim["concept_type"] == "other"
    assert "Young" in claim["concept"]


def test_v28_keeps_public_v23_current() -> None:
    assert CURRENT_PROMPT == "job-analysis-english-v23"
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v28"
