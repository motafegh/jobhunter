"""A2 whole-first planning and guarded private execution controls."""

from __future__ import annotations

import json
from dataclasses import replace

import pytest
from test_p16_lab import root  # noqa: F401
from test_p16_lab_a2_context import fixture

from jobhunter.p16_lab import digest, read_events
from jobhunter.p16_lab_a2_context import packet_for_case
from jobhunter.p16_lab_a2_execution import plan_context, synthetic_case, verify_manifest
from jobhunter.p16_lab_provider_worker import rehearse_provider
from jobhunter.p16_lab_qualification import ExactFit, RuntimeBinding

EXPECTED = {"key": "model", "sha256": "e" * 64}
BINDING = RuntimeBinding(
    "model",
    "e" * 64,
    "a" * 64,
    "b" * 64,
    "c" * 64,
    "d" * 64,
    "model",
    16384,
    "test",
    True,
    True,
    0.0,
)


def body_context(body):
    return json.loads(json.loads(body)["messages"][1]["content"])


def measure(body, tokens=100):
    return ExactFit(
        digest(body),
        "a" * 64,
        "b" * 64,
        "c" * 64,
        "e" * 64,
        tokens,
        json.loads(body)["max_tokens"],
        16384,
        True,
    )


def plan(b=None, language="L2", probe=measure, **kwargs):
    b = b or synthetic_case()
    p = packet_for_case(b, language)
    return p, plan_context(
        p,
        b,
        language=language,
        run_id="test",
        binding=BINDING,
        expected=EXPECTED,
        measure=probe,
        **kwargs,
    )


def section_probe(body):
    return measure(body, 9000 if body_context(body)["whole_context"] else 100)


@pytest.mark.parametrize("language", ["L0", "L2", "L3"])
def test_whole_first_exact_bytes(language):
    packet, result = plan(language=language)
    assert result.strategy == "whole" and len(result.requests) == 1 and not result.unplanned
    request = result.requests[0]
    assert request.fit.request_sha256 == digest(request.body)
    assert request.scope["handles"] == [u["handle"] for u in packet["units"]]
    assert body_context(request.body)["whole_context"]
    assert len(result.measurements) == 1
    body = json.loads(request.body)
    assert body["response_format"]["json_schema"]["schema"]["$defs"]["Proposal"]["required"] == [
        "ref",
        "meaning",
        "evidence",
        "basis",
    ]
    assert body["stream"] is False


@pytest.mark.parametrize("language", ["L0", "L2", "L3"])
def test_section_plan_keeps_context_and_exact_primary_inventory(language):
    packet, result = plan(language=language, probe=section_probe)
    assert result.strategy == "sections" and len(result.requests) == 2 and not result.unplanned
    primary = [h for r in result.requests for h in r.primary]
    expected = [
        u["handle"]
        for u in packet["units"]
        if u["kind"].startswith("description")
        and not (language == "L3" and u["representation"] == "english_projection")
    ]
    assert primary == expected
    shared = set(u["handle"] for u in packet["units"]) - set(primary)
    for r in result.requests:
        assert set(r.scope["handles"]) == shared | set(r.primary)
        assert r.fit.request_sha256 == digest(r.body)
        assert body_context(r.body)["primary_handles"] == list(r.primary)


@pytest.mark.parametrize("bad", ["missing", "hash", "template", "runtime", "synthetic", "output"])
def test_unverified_fit_is_not_context_overflow(bad):
    def invalid(body):
        proof = measure(body, 9000)
        changes = {
            "hash": {"request_sha256": "0" * 64},
            "template": {"effective_template_sha256": "0" * 64},
            "runtime": {"runtime_sha256": "0" * 64},
            "synthetic": {"synthetic": False},
            "output": {"output_tokens": 1},
        }
        return None if bad == "missing" else replace(proof, **changes[bad])

    with pytest.raises(ValueError, match="fit evidence"):
        plan(probe=invalid)


def test_unfit_translated_field_not_split():
    packet, result = plan(fixture(), language="L0", probe=lambda b: measure(b, 9000))
    assert not result.requests
    assert result.unplanned == tuple(u["handle"] for u in packet["units"])


def test_cap_records_unplanned_section():
    packet, result = plan(probe=section_probe, max_requests=1)
    assert len(result.requests) == 1 and result.unplanned
    assert set(result.unplanned).isdisjoint(result.requests[0].primary)
    assert set(result.unplanned) | set(result.requests[0].scope["handles"]) == {
        u["handle"] for u in packet["units"]
    }


def test_plan_rejects_nonsynthetic_binding():
    b = synthetic_case()
    with pytest.raises(ValueError, match="synthetic planning"):
        plan_context(
            packet_for_case(b, "L2"),
            b,
            language="L2",
            run_id="test",
            binding=replace(BINDING, synthetic=False),
            expected=EXPECTED,
            measure=measure,
        )


@pytest.mark.parametrize(
    "scenario,gen,ctrl,failed,visible",
    [
        ("a2-whole", 1, 1, False, 1),
        ("a2-sections", 2, 1, False, 2),
        ("a2-malformed", 1, 1, True, 0),
        ("a2-overflow", 0, 0, True, 0),
        ("a2-second-fails", 2, 1, True, 1),
    ],
)
def test_worker_durable_lineage(request, scenario, gen, ctrl, failed, visible):
    root_path = request.getfixturevalue("root")
    result = rehearse_provider(root_path, scenario, scenario)
    assert result["status"] == "child_completed" and result["journal"]["sealed"]
    child = result["child"]
    summary = child["a2_result"]
    assert child["generation_reservations"] == gen and child["control_reservations"] == ctrl
    assert child["stopped"] is failed and summary["failed"] is failed
    assert child["real_dispatches"] == child["denied_operations"] == 0
    assert summary["visible_proposals"] == visible and summary["recorded"] == gen
    path = root_path / "data/local-acceptance/p16-evolution-e3" / scenario
    rows = read_events(path / "dispatch.jsonl")
    assert verify_manifest(path, summary, rows)
    manifest = json.loads((path / "a2-manifest.json").read_bytes())
    assert not manifest["whole_candidate_established"]
    assert manifest["authority"] == "candidate_only"
    assert manifest["actual_experiment_cell"] is False
    if gen:
        candidate = json.loads((path / f"a2-{gen:02d}-candidate.json").read_bytes())
        assert candidate["execution"] == ("failed" if failed else "completed")
        raw = path / "a2-01-http-response.bin"
        raw.write_bytes(raw.read_bytes() + b" ")
        assert not verify_manifest(path, summary, rows)
    else:
        assert manifest["unplanned"] and manifest["delivery"] == "source_only"
