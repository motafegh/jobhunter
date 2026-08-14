from __future__ import annotations

import pytest
from pydantic import ValidationError

from jobhunter.analysis_runtime_v20 import (
    _PARTITION_SIZE,
    _assert_partition_scope,
    _merge_partition_structured,
    _v20_requirement_partitions,
)
from jobhunter.analysis_service import AnalysisValidationError
from jobhunter.analysis_service_v20 import (
    _ANALYSIS_SCHEMA_V20,
    _ENGLISH_SYSTEM_PROMPT_V20,
    ANALYSIS_SCHEMA_VERSION,
    ENGLISH_PROMPT_VERSION,
)
from jobhunter.evidence_refs import build_field_evidence_catalog
from jobhunter.inference.instructor_lm_studio_v20 import AnalysisRequirementV20


def _candidate(
    text: str,
    *,
    hint: str | None = "contextual",
    allow_exclusion: bool = True,
    source_kind: str = "description",
) -> dict:
    return {
        "text": text,
        "source_kind": source_kind,
        "obligation_hint": hint,
        "allow_exclusion": allow_exclusion,
    }


def _requirement(
    concept: str,
    evidence: str,
    *,
    requirement_type: str = "contextual",
) -> dict:
    return {
        "concept": concept,
        "depth_signal": None,
        "requirement_type": requirement_type,
        "concept_type": "tool",
        "evidence": evidence,
        "confidence": "high",
        "rationale": "Test requirement.",
    }


def _empty_part() -> dict:
    return {
        "role_purpose": [],
        "responsibilities": [],
        "requirements": [],
        "coverage_exclusions": [],
    }


def _context(fields: dict) -> dict:
    return {
        "analysis_fields": fields,
        "analysis_mode": "english",
        "evidence_catalog": build_field_evidence_catalog(fields),
    }


def test_v20_has_partition_prompt_identity_without_changing_v5_shape() -> None:
    assert ENGLISH_PROMPT_VERSION == "job-analysis-english-v20"
    assert ANALYSIS_SCHEMA_VERSION == "job-analysis-v5"
    assert "SOURCE-LED BOUNDED SEMANTIC PARTITIONING" in _ENGLISH_SYSTEM_PROMPT_V20
    assert "high-level" in _ENGLISH_SYSTEM_PROMPT_V20
    assert '"some"' in _ENGLISH_SYSTEM_PROMPT_V20
    assert "maxItems" not in _ANALYSIS_SCHEMA_V20["properties"]["requirements"]


def test_v20_dense_coverage_is_partitioned_without_losing_any_reference() -> None:
    plan: dict[str, dict] = {}
    for index in range(6):
        plan[f"field:skills:{index}"] = _candidate(
            f"skill-{index}",
            hint="required",
            allow_exclusion=False,
            source_kind="structured_skill",
        )
    for index in range(5):
        plan[f"required:{index}"] = _candidate(
            f"required-{index}",
            hint="required",
            allow_exclusion=False,
        )
    plan["segment13:matlab"] = _candidate("MATLAB a plus", hint="preferred")
    plan["segment13:cpp"] = _candidate("some C / C++ helpful", hint="preferred")
    plan["segment13:python"] = _candidate("Python (expert)")
    plan["segment13:sql"] = _candidate("SQL")
    for index in range(16):
        plan[f"context:{index}"] = _candidate(f"context-{index}")

    partitions = _v20_requirement_partitions(plan)

    flattened = [reference for partition in partitions for reference in partition]
    assert len(flattened) == len(plan)
    assert set(flattened) == set(plan)
    assert len(flattened) == len(set(flattened))
    assert all(1 <= len(partition) <= _PARTITION_SIZE for partition in partitions)

    core_refs = [reference for partition in partitions[:2] for reference in partition]
    assert "segment13:matlab" in core_refs
    assert "segment13:cpp" in core_refs
    assert "segment13:python" not in core_refs
    assert "segment13:sql" not in core_refs


def test_v20_merge_preserves_valid_facts_from_separate_retry_like_slices() -> None:
    first = _empty_part()
    first["requirements"] = [
        _requirement("Python", "Python (expert)"),
        _requirement("SQL", "SQL"),
        _requirement("MATLAB", "MATLAB a plus", requirement_type="preferred"),
        _requirement("C / C++", "some C / C++ helpful", requirement_type="preferred"),
    ]
    second = _empty_part()
    second["requirements"] = [
        _requirement("ML frameworks", "ML & deep learning: scikit-learn, PyTorch"),
        _requirement("Data platforms", "Data platforms: Spark, Kafka"),
    ]

    merged = _merge_partition_structured([first, second])

    evidence = {item["evidence"] for item in merged["requirements"]}
    assert evidence == {
        "Python (expert)",
        "SQL",
        "MATLAB a plus",
        "some C / C++ helpful",
        "ML & deep learning: scikit-learn, PyTorch",
        "Data platforms: Spark, Kafka",
    }


def test_v20_clears_some_from_preferred_cpp_depth_without_changing_evidence() -> None:
    fields = {"description": "some C / C++ helpful"}
    result = AnalysisRequirementV20.model_validate(
        {
            "concept": "C / C++",
            "depth_signal": "some",
            "requirement_type": "preferred",
            "concept_type": "tool",
            "evidence": "some C / C++ helpful",
            "confidence": "high",
            "rationale": "Explicitly helpful; some is a vague quantifier, not accepted depth.",
        },
        context=_context(fields),
    )

    assert result.requirement_type == "preferred"
    assert result.depth_signal is None
    assert result.evidence == "some C / C++ helpful"


def test_v20_preserves_real_depth_even_when_requirement_is_preferred() -> None:
    fields = {"description": "Strong C / C++ preferred"}
    result = AnalysisRequirementV20.model_validate(
        {
            "concept": "C / C++",
            "depth_signal": "Strong",
            "requirement_type": "preferred",
            "concept_type": "tool",
            "evidence": "Strong C / C++ preferred",
            "confidence": "high",
            "rationale": "Source explicitly states both preference and technical depth.",
        },
        context=_context(fields),
    )

    assert result.requirement_type == "preferred"
    assert result.depth_signal == "Strong"


def test_v20_does_not_clear_some_without_explicit_preference_evidence() -> None:
    fields = {"description": "some C / C++"}

    with pytest.raises(ValidationError, match="explicit employer depth"):
        AnalysisRequirementV20.model_validate(
            {
                "concept": "C / C++",
                "depth_signal": "some",
                "requirement_type": "contextual",
                "concept_type": "tool",
                "evidence": "some C / C++",
                "confidence": "high",
                "rationale": "No explicit preference marker.",
            },
            context=_context(fields),
        )


def test_v20_merge_deduplicates_only_exact_requirement_identity() -> None:
    first = _empty_part()
    first["requirements"] = [_requirement("Python", "Python")]
    second = _empty_part()
    second["requirements"] = [
        _requirement("Python", "Python"),
        _requirement("Python", "Python (expert)"),
    ]

    merged = _merge_partition_structured([first, second])

    assert len(merged["requirements"]) == 2
    assert {item["evidence"] for item in merged["requirements"]} == {
        "Python",
        "Python (expert)",
    }


def test_v20_partition_scope_rejects_requirement_leakage() -> None:
    part = _empty_part()
    part["requirements"] = [_requirement("SQL", "SQL")]

    with pytest.raises(AnalysisValidationError, match="outside its assigned ledger"):
        _assert_partition_scope(
            part,
            requirement_plan={"python": _candidate("Python (expert)")},
            responsibility_plan={},
        )


def test_v20_partition_scope_rejects_duties_when_partition_has_none() -> None:
    part = _empty_part()
    part["responsibilities"] = [
        {
            "statement": "Build models.",
            "evidence": "Build models.",
            "confidence": "high",
        }
    ]

    with pytest.raises(AnalysisValidationError, match="duty evidence outside"):
        _assert_partition_scope(
            part,
            requirement_plan={},
            responsibility_plan={},
        )


def test_v20_partition_scope_accepts_only_assigned_evidence() -> None:
    part = _empty_part()
    part["requirements"] = [_requirement("Python", "Python (expert)")]
    part["responsibilities"] = [
        {
            "statement": "Build models.",
            "evidence": "Build and validate models.",
            "confidence": "high",
        }
    ]

    _assert_partition_scope(
        part,
        requirement_plan={"python": _candidate("Python (expert)")},
        responsibility_plan={"duty": "Build and validate models."},
    )
