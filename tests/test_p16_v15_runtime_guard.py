from __future__ import annotations

import jobhunter.analysis_runtime_v15 as runtime_v15

from jobhunter.p16_v15_runtime_guard import (
    normalize_ability_wrappers,
    v15_ability_wrapper_guard,
)


def _structured(concept: str) -> dict:
    return {
        "requirements": [
            {
                "concept": concept,
                "concept_type": "skill",
                "evidence": "ability to produce visual content full-time and part-time",
            }
        ]
    }


def test_v15_guard_strips_ability_wrapper_without_changing_evidence() -> None:
    structured = _structured("Ability to produce visual content")
    evidence = structured["requirements"][0]["evidence"]

    changed = normalize_ability_wrappers(structured)

    assert changed == [0]
    assert structured["requirements"][0]["concept"] == "produce visual content"
    assert structured["requirements"][0]["evidence"] == evidence


def test_v15_guard_leaves_wrapper_only_logistics_invalid() -> None:
    structured = _structured("Ability to work")

    changed = normalize_ability_wrappers(structured)

    assert changed == []
    assert structured["requirements"][0]["concept"] == "Ability to work"


def test_v15_guard_restores_runtime_validator_after_scope() -> None:
    original = runtime_v15.validate_v15_candidate_structured

    with v15_ability_wrapper_guard():
        assert runtime_v15.validate_v15_candidate_structured is not original

    assert runtime_v15.validate_v15_candidate_structured is original
