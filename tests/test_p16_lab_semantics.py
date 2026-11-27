"""A0 persistence rehearsal and bounded R1 repair controls; no private inputs in CI."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError
from test_p16_lab import root  # noqa: F401

from jobhunter.inference.instructor_lm_studio_v30 import AnalysisRequirementV30
from jobhunter.p16_lab_a0 import FrozenProjection
from jobhunter.p16_lab_a1_r1 import AnalysisRequirementR1
from jobhunter.p16_lab_provider_worker import rehearse_provider

COMPOUND = "Strong proficiency in Rust or Kotlin, with a solid understanding of distributed design."
PARENT = COMPOUND + " Additional text about the workplace."


def _raw(concept="Rust or Kotlin", signal="Strong proficiency", item=COMPOUND):
    return {
        "concept": concept,
        "depth_signal": signal,
        "requirement_type": "required",
        "concept_type": "skill",
        "evidence": "field:description:0",
        "confidence": "high",
        "rationale": "Source backed.",
        "item_excerpt": item,
    }


def _ctx(parent=PARENT):
    return {
        "analysis_mode": "english",
        "analysis_fields": {"description": parent},
        "evidence_catalog": {"field:description:0": parent},
    }


def test_r1_preserves_two_exact_scopes_and_parent():
    items = [_raw(), _raw("distributed design", "solid understanding")]
    for q in items:
        with pytest.raises(ValidationError):
            AnalysisRequirementV30.model_validate(q, context=_ctx())
    a, b = [AnalysisRequirementR1.model_validate(q, context=_ctx()) for q in items]
    assert a.concept == "Rust or Kotlin" and a.depth_signal == "Strong proficiency"
    assert b.concept == "distributed design" and b.depth_signal == "solid understanding"
    assert a.item_excerpt == "Strong proficiency in Rust or Kotlin"
    assert b.item_excerpt == "solid understanding of distributed design"
    assert a.evidence == b.evidence == PARENT
    assert all(x.requirement_type == "required" for x in (a, b))


@pytest.mark.parametrize(
    "concept,signal,item",
    [
        ("Proficiency in Rust or Kotlin", "proficiency", COMPOUND),
        ("Rust or Kotlin", None, COMPOUND),
        ("Rust or Kotlin", "Strong proficiency", "Strong proficiency in Rust or Kotlin"),
    ],
)
def test_r1_exact_wrapper_and_narrowed_child(concept, signal, item):
    result = AnalysisRequirementR1.model_validate(_raw(concept, signal, item), context=_ctx())
    assert result.concept == "Rust or Kotlin"
    assert result.depth_signal == "Strong proficiency"


@pytest.mark.parametrize(
    "changes",
    [
        {"concept": "Rust"},
        {"concept": "unrelated capability"},
        {"depth_signal": "solid"},
        {"depth_signal": "expertise"},
        {"evidence": "field:nonexistent:77"},
        {"item_excerpt": "Strong proficiency in invented tool"},
    ],
)
def test_r1_rejects_loss_or_borrowing(changes):
    with pytest.raises(ValidationError):
        AnalysisRequirementR1.model_validate({**_raw(), **changes}, context=_ctx())


def test_r1_rejects_duplicate_scope():
    with pytest.raises(ValidationError):
        AnalysisRequirementR1.model_validate(_raw(), context=_ctx(COMPOUND + " " + COMPOUND))


def test_r1_does_not_modify_incumbent_unrelated_case():
    text = "Practical experience in designing distributed systems"
    raw = {**_raw(text, None, text), "evidence": text, "concept_type": "experience"}
    ctx = _ctx(text)
    assert (
        AnalysisRequirementR1.model_validate(raw, context=ctx).model_dump()
        == AnalysisRequirementV30.model_validate(raw, context=ctx).model_dump()
    )


def test_frozen_projection_association_and_stale_denial():
    expected = {
        "translation_id": 7,
        "source_version": 2,
        "source_semantic_sha256": "s",
        "translation_sha256": "t",
        "translation_model": "m",
    }
    a = SimpleNamespace(
        id=7,
        source_job_id="job",
        job_detail_version_id=2,
        source_semantic_sha256="s",
        translation_sha256="t",
        provider_model="m",
        translation_schema_version="english-projection-v2",
        target_language="en",
    )
    s = SimpleNamespace(job_detail_version_id=2, semantic_sha256="s")
    store = SimpleNamespace(artifact_by_id=lambda _: a, latest_source_version=lambda _: s)
    p = FrozenProjection(store, expected)
    assert p.current_artifact("job") is a
    s.job_detail_version_id = 3
    with pytest.raises(ValueError, match="association"):
        p.current_artifact("job")


def test_a0_actual_service_fresh_pending(request):
    root_path = request.getfixturevalue("root")
    evidence = rehearse_provider(root_path, "a0-synthetic-test", "a0-synthetic")
    assert evidence["status"] == "child_completed" and evidence["journal"]["sealed"]
    child = evidence["child"]
    assert child["a0_result"] == {
        "artifact_id": 2,
        "outcome": "completed",
        "semantic_review_status": "pending",
    }
    assert child["a0_storage"]["latest_attempt"] == ["completed", 2]
    assert child["a0_storage"]["history_preserved"]
    assert child["a0_storage"]["integrity"] and child["a0_storage"]["foreign_keys"]
    assert child["generation_reservations"] == child["control_reservations"] == 1
    assert child["real_dispatches"] == 0 and child["denied_operations"] == 0
    path = root_path / "data/local-acceptance/p16-evolution-e3/a0-synthetic-test"
    events = [json.loads(line) for line in (path / "dispatch.jsonl").read_text().splitlines()]
    assert any(
        e["event"] == "a0_rehearsal_scope" and not e["actual_experiment_cell"] for e in events
    )


def test_a0_retained_missing_source_manifest_denied(request):
    root_path = request.getfixturevalue("root")
    evidence = rehearse_provider(root_path, "a0-missing", "a0-retained")
    assert evidence["status"] == "child_failed"
    path = root_path / "data/local-acceptance/p16-evolution-e3/a0-missing"
    assert not (path / "working.sqlite3").exists()
    events = [json.loads(line) for line in (path / "dispatch.jsonl").read_text().splitlines()]
    assert not any(e["event"] == "reserved" for e in events)
