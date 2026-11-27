"""Offline runtime qualification gates and raw provider transport controls."""

from __future__ import annotations

import json
from dataclasses import replace

import httpx
import pytest
from test_p16_lab import Clock, guard, request, root  # noqa: F401

from jobhunter.inference.lm_studio import LMStudioProvider
from jobhunter.p16_lab import LabStopped, OfflineRun, digest
from jobhunter.p16_lab_qualification import (
    ExactFit,
    RuntimeBinding,
    _gpu_info,
    _meminfo,
    binding_blockers,
    fit_blockers,
    guarded_synthetic_fit,
    pinned_artifacts,
    qualification_summary,
    verify_artifact,
)


def test_artifact_bytes_only(tmp_path):
    data = b"GGUFsynthetic artifact"
    p = tmp_path / "model.gguf"
    p.write_bytes(data)
    expected = {
        "role": "M0",
        "key": "model",
        "artifact_catalog_path": p.name,
        "bytes": len(data),
        "sha256": digest(data),
    }
    result = verify_artifact(tmp_path, expected)
    assert result["status"] == "bytes_verified"
    assert not result["rights_verified"]
    assert not result["runtime_binding_verified"]
    assert not result["effective_template_verified"]
    p.write_bytes(data[:-1] + b"x")
    with pytest.raises(ValueError, match="digest"):
        verify_artifact(tmp_path, expected)


@pytest.mark.parametrize("variant", ["size", "magic", "symlink"])
def test_artifact_denied(tmp_path, variant):
    p = tmp_path / "model.gguf"
    data = b"GGUFexample" if variant != "magic" else b"WRONG"
    p.write_bytes(data)
    expected = {
        "role": "M0",
        "key": "model",
        "artifact_catalog_path": p.name,
        "bytes": len(data),
        "sha256": digest(data),
    }
    if variant == "size":
        expected["bytes"] += 1
    elif variant == "symlink":
        alias = tmp_path / "alias.gguf"
        alias.symlink_to(p)
        expected["artifact_catalog_path"] = alias.name
    with pytest.raises(ValueError):
        verify_artifact(tmp_path, expected)


def test_resource_parsing():
    assert (
        _meminfo("MemAvailable: 10485760 kB\nSwapTotal: 100 kB\nSwapFree: 99 kB")["MemAvailable"]
        == 10485760
    )
    assert _gpu_info("GPU, 8192, 4096, 42.8")["free_mib"] == 4096


@pytest.mark.parametrize(
    "text",
    [
        "MemAvailable: 1 kB\nSwapTotal: 0 kB\nSwapFree: 1 kB",
        "MemAvailable: 1 kB\nSwapTotal: 1 kB",
        "MemAvailable: -1 kB\nSwapTotal: 1 kB\nSwapFree: 0 kB",
    ],
)
def test_invalid_meminfo(text):
    with pytest.raises(ValueError):
        _meminfo(text)


@pytest.mark.parametrize(
    "text",
    [
        "GPU, 8192, NaN, 42",
        "GPU, 8192, 9000, 42",
        "GPU, 8192, 4096, 42\nGPU2",
    ],
)
def test_invalid_gpu(text):
    with pytest.raises(ValueError):
        _gpu_info(text)


@pytest.fixture
def qualified(request):
    root_path = request.getfixturevalue("root")
    clock = Clock()
    run = OfflineRun(root_path, "qualification", clock=clock, diagnostic_only=True)
    run.start_session()
    run.start_cell(run.cells[0]["cell_id"])
    expected = pinned_artifacts(root_path)
    a = expected["M0"]
    binding = RuntimeBinding(
        model_key=a["key"],
        artifact_sha256=a["sha256"],
        runtime_sha256="a" * 64,
        tokenizer_sha256="b" * 64,
        effective_template_sha256="c" * 64,
        rights_receipt_sha256="d" * 64,
        instance_id=a["key"],
        allocated_context=16384,
        lease_id=run.path.name,
        idle_confirmed=True,
        synthetic=True,
        observed_at=clock(),
    )
    yield run, clock, expected, binding
    if not run.sealed:
        run.journal.close()


def exact(req, binding, **changes):
    return replace(
        ExactFit(
            request_sha256=digest(req.content),
            runtime_sha256=binding.runtime_sha256,
            tokenizer_sha256=binding.tokenizer_sha256,
            effective_template_sha256=binding.effective_template_sha256,
            artifact_sha256=binding.artifact_sha256,
            input_tokens=100,
            output_tokens=json.loads(req.content)["max_tokens"],
            context_tokens=16384,
            synthetic=True,
        ),
        **changes,
    )


def test_synthetic_binding_never_qualifies_actual(qualified):
    _, _, models, b = qualified
    expected = models["M0"]
    artifact = {**expected, "status": "bytes_verified", "model_key": expected["key"]}
    r = qualification_summary(expected, artifact, b, context=16384, owned_lease=b.lease_id)
    assert "synthetic_binding" in r["binding_blockers"]
    assert not r["actual_qualification_established"]
    assert not r["real_dispatch_enabled"]
    assert not binding_blockers(
        expected, b, context=16384, owned_lease=b.lease_id, allow_synthetic=True
    )


@pytest.mark.parametrize(
    ("changes", "blocker"),
    [
        ({"artifact_sha256": "e" * 64}, "artifact_identity"),
        ({"runtime_sha256": None}, "runtime_unverified"),
        ({"tokenizer_sha256": None}, "tokenizer_unverified"),
        ({"effective_template_sha256": None}, "template_unverified"),
        ({"rights_receipt_sha256": None}, "rights_unverified"),
        ({"allocated_context": 8192}, "context_unverified"),
        ({"instance_id": "other"}, "ownership_unverified"),
        ({"lease_id": "other-run"}, "ownership_unverified"),
        ({"idle_confirmed": None}, "idle_unverified"),
        ({"observed_at": 98.0}, "binding_stale"),
    ],
)
def test_binding_blocks_physical_reservation(qualified, changes, blocker):
    run, clock, models, b = qualified
    fit = guarded_synthetic_fit(
        run, models, binding=lambda: replace(b, **changes), proof=lambda req: exact(req, b)
    )
    g = guard((run, clock), handler=lambda req: pytest.fail("dispatch"), fit=fit)
    with pytest.raises(LabStopped, match=blocker):
        g.handle_request(request())
    assert run.gen == 0
    assert run.seal()["stopped"]


@pytest.mark.parametrize(
    "changes",
    [
        {"request_sha256": "e" * 64},
        {"tokenizer_sha256": "e" * 64},
        {"effective_template_sha256": "e" * 64},
        {"input_tokens": 9000},
        {"output_tokens": True},
        {"synthetic": False},
    ],
)
def test_exact_fit_blocks_physical_reservation(qualified, changes):
    run, clock, models, b = qualified
    fit = guarded_synthetic_fit(
        run, models, binding=lambda: b, proof=lambda req: exact(req, b, **changes)
    )
    g = guard((run, clock), handler=lambda req: pytest.fail("dispatch"), fit=fit)
    with pytest.raises(LabStopped, match="qualification_fit"):
        g.handle_request(request())
    assert run.gen == 0
    assert run.seal()["stopped"]


def test_exact_fit_bound_to_actual_request(qualified):
    run, clock, models, b = qualified
    fit = guarded_synthetic_fit(run, models, binding=lambda: b, proof=lambda req: exact(req, b))
    g = guard((run, clock), fit=fit)
    assert g.handle_request(request()).status_code == 200
    assert run.gen == 1
    req = request()
    changed = request(messages=[{"role": "user", "content": "changed"}])
    assert fit_blockers(changed.content, exact(req, b), b, output_limit=8192) == (
        "fit_identity_mismatch",
    )
    run.finish_cell(idle_confirmed=True)
    run.seal()


def test_direct_provider_physical_retry_and_fit(qualified):
    run, clock, models, b = qualified
    fit = guarded_synthetic_fit(run, models, binding=lambda: b, proof=lambda req: exact(req, b))
    seen = []

    def handler(req):
        seen.append(req)
        if len(seen) == 1:
            return httpx.Response(503)
        return httpx.Response(
            200,
            json={
                "choices": [{"finish_reason": "stop", "message": {"content": '{"value":"ok"}'}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 2},
            },
        )

    g = guard((run, clock), handler=handler, fit=fit)
    provider = LMStudioProvider(
        base_url="http://127.0.0.1:18080/v1",
        configured_model=b.model_key,
        max_retries=1,
        transport=g,
    )
    result = provider.complete_structured(
        system_prompt="synthetic",
        user_payload={"test": True},
        schema_name="lab-synthetic",
        schema={
            "type": "object",
            "properties": {"value": {"type": "string"}},
            "required": ["value"],
        },
        max_tokens=512,
        max_recovery_tokens=512,
    )
    assert result.structured == {"value": "ok"}
    assert len(seen) == run.gen == 2
    run.finish_cell(idle_confirmed=True)
    run.seal()


def test_resource_observation_missing_is_not_qualified(monkeypatch):
    from jobhunter import p16_lab_qualification as q

    def fail(*args, **kwargs):
        raise OSError("test")

    monkeypatch.setattr(q.subprocess, "check_output", fail)
    r = q.observe_local_resources()
    assert r["gpu"] is None
    assert r["windows_available_gib"] is None
    assert r["thermal_or_oom"] is None
    assert not r["qualified"]
