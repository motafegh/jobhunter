"""Evidence-only local runtime qualification for the frozen P1.6 experiment.

No model load, HTTP request, tokenizer approximation or authority promotion.
A complete evidence shape is a prerequisite, never dispatch authorization.
"""

from __future__ import annotations

import json
import math
import re
import stat
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import httpx

from jobhunter.p16_lab import (
    ROOT,
    Fit,
    OfflineRun,
    checked_path,
    digest,
    file_digest,
    load_requirements,
)

ARTIFACTS = "docs/working-memory/2026-11-26_p16_e2/MODEL_ARTIFACT_IDENTITIES.json"
ROLES = ("M0", "M1", "M2")


def pinned_artifacts(root: Path = ROOT) -> dict[str, dict]:
    load_requirements(root)
    rows = json.loads(checked_path(root, ARTIFACTS).read_bytes())["artifacts"]
    models = {row["role"]: row for row in rows}
    if set(models) != set(ROLES) or len(rows) != 3:
        raise ValueError("unexpected frozen model identities")
    return models


def _file_identity(path: Path) -> tuple:
    s = path.stat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError("not a regular artifact")
    return s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns


def verify_artifact(model_root: Path, expected: dict) -> dict:
    """Rehash exact frozen bytes, not catalog alias or weight-size approximation."""
    p = checked_path(model_root, expected["artifact_catalog_path"])
    before = _file_identity(p)
    if before[2] != expected["bytes"]:
        raise ValueError("artifact size mismatch")
    with p.open("rb") as f:
        if f.read(4) != b"GGUF":
            raise ValueError("not GGUF")
    sha = file_digest(p)
    if _file_identity(p) != before or sha != expected["sha256"]:
        raise ValueError("artifact changed or digest mismatch")
    return {
        "role": expected["role"],
        "model_key": expected["key"],
        "bytes": before[2],
        "sha256": sha,
        "status": "bytes_verified",
        "effective_template_verified": False,
        "runtime_binding_verified": False,
        "rights_verified": False,
    }


def _meminfo(text: str) -> dict[str, int]:
    required = {"MemAvailable", "SwapTotal", "SwapFree"}
    values = {}
    for line in text.splitlines():
        key, _, rest = line.partition(":")
        if key in required:
            parts = rest.split()
            if key in values or len(parts) != 2 or parts[1] != "kB":
                raise ValueError("invalid memory field")
            values[key] = int(parts[0])
    if (
        set(values) != required
        or min(values.values()) < 0
        or values["SwapFree"] > values["SwapTotal"]
    ):
        raise ValueError("invalid memory snapshot")
    return values


def _gpu_info(text: str) -> dict:
    rows = text.strip().splitlines()
    if len(rows) != 1:
        raise ValueError("single designated GPU required")
    fields = [v.strip() for v in rows[0].split(",")]
    if len(fields) != 4:
        raise ValueError("invalid GPU snapshot")
    total, free, temperature = map(float, fields[1:])
    if (
        not all(math.isfinite(n) for n in (total, free, temperature))
        or total <= 0
        or not 0 <= free <= total
    ):
        raise ValueError("invalid GPU values")
    return {"gpu": fields[0], "total_mib": total, "free_mib": free, "temperature_c": temperature}


def observe_local_resources() -> dict:
    """Bounded read-only WSL and GPU observation. Missing host/thermal proof stays unknown."""
    start = time.monotonic()
    errors = []
    gpu = mem = None
    try:
        raw = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.free,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=3,
        )
        gpu = _gpu_info(raw)
    except (OSError, ValueError, subprocess.SubprocessError):
        errors.append("gpu_unavailable")
    try:
        mem = _meminfo(Path("/proc/meminfo").read_text())
    except (OSError, ValueError):
        errors.append("wsl_memory_unavailable")
    return {
        "gpu": gpu,
        "wsl": mem,
        "windows_available_gib": None,
        "thermal_or_oom": None,
        "swap_growth_mib": None,
        "duration_seconds": time.monotonic() - start,
        "errors": errors
        + ["windows_memory_unverified", "thermal_oom_unverified", "swap_baseline_unverified"],
        "qualified": False,
    }


def _sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


@dataclass(frozen=True, slots=True)
class RuntimeBinding:
    """An observation, not a runtime attestation; all hashes reference reviewable evidence."""

    model_key: str
    artifact_sha256: str
    runtime_sha256: str | None
    tokenizer_sha256: str | None
    effective_template_sha256: str | None
    rights_receipt_sha256: str | None
    instance_id: str | None
    allocated_context: int | None
    lease_id: str | None
    idle_confirmed: bool | None
    synthetic: bool
    observed_at: float | None = None


@dataclass(frozen=True, slots=True)
class ExactFit:
    request_sha256: str
    runtime_sha256: str
    tokenizer_sha256: str
    effective_template_sha256: str
    artifact_sha256: str
    input_tokens: int
    output_tokens: int
    context_tokens: int
    synthetic: bool


def binding_blockers(
    expected: dict,
    binding: RuntimeBinding,
    *,
    context: int,
    owned_lease: str,
    allow_synthetic: bool = False,
) -> tuple[str, ...]:
    """Fail closed for missing or contradictory evidence fields.

    A digest's presence does not validate the underlying rights/runtime/ownership
    receipt. This function deliberately cannot authorize real transport.
    """
    missing = []
    if binding.synthetic is not False and not (allow_synthetic and binding.synthetic is True):
        missing.append("synthetic_binding")
    if binding.model_key != expected["key"] or binding.artifact_sha256 != expected["sha256"]:
        missing.append("artifact_identity")
    for label, value in (
        ("runtime", binding.runtime_sha256),
        ("tokenizer", binding.tokenizer_sha256),
        ("template", binding.effective_template_sha256),
        ("rights", binding.rights_receipt_sha256),
    ):
        if not _sha(value):
            missing.append(label + "_unverified")
    if type(binding.allocated_context) is not int or binding.allocated_context != context:
        missing.append("context_unverified")
    if binding.instance_id != expected["key"] or not owned_lease or binding.lease_id != owned_lease:
        missing.append("ownership_unverified")
    if binding.idle_confirmed is not True:
        missing.append("idle_unverified")
    return tuple(missing)


def fit_blockers(
    request_bytes: bytes,
    proof: ExactFit | None,
    binding: RuntimeBinding,
    *,
    output_limit: int,
) -> tuple[str, ...]:
    """Bind exact prepared HTTP request bytes to effective tokenizer/template and context."""
    if not isinstance(proof, ExactFit):
        return ("fit_missing",)
    if (
        proof.request_sha256 != digest(request_bytes)
        or proof.runtime_sha256 != binding.runtime_sha256
        or proof.tokenizer_sha256 != binding.tokenizer_sha256
        or proof.effective_template_sha256 != binding.effective_template_sha256
        or proof.artifact_sha256 != binding.artifact_sha256
        or any(
            not _sha(v)
            for v in (
                proof.runtime_sha256,
                proof.tokenizer_sha256,
                proof.effective_template_sha256,
                proof.artifact_sha256,
            )
        )
        or proof.synthetic is not binding.synthetic
    ):
        return ("fit_identity_mismatch",)
    try:
        body = json.loads(request_bytes)
    except ValueError:
        return ("fit_invalid_request",)
    if (
        not isinstance(body, dict)
        or body.get("model") != binding.model_key
        or body.get("stream", False) is not False
        or type(body.get("max_tokens")) is not int
        or any(
            type(n) is not int
            for n in (proof.input_tokens, proof.output_tokens, proof.context_tokens)
        )
        or body["max_tokens"] != proof.output_tokens
        or not 0 < proof.output_tokens <= output_limit
        or proof.context_tokens != binding.allocated_context
        or not 0 < proof.input_tokens <= proof.context_tokens - proof.output_tokens
    ):
        return ("fit_capacity_unverified",)
    return ()


def qualification_summary(
    expected: dict,
    artifact: dict,
    binding: RuntimeBinding,
    *,
    context: int,
    owned_lease: str,
) -> dict:
    """Evidence summary only, never grants dispatch; no synthetic promotion."""
    blockers = list(binding_blockers(expected, binding, context=context, owned_lease=owned_lease))
    if (
        artifact.get("status") != "bytes_verified"
        or artifact.get("role") != expected["role"]
        or artifact.get("model_key") != expected["key"]
        or artifact.get("bytes") != expected["bytes"]
        or artifact.get("sha256") != expected["sha256"]
    ):
        blockers.append("artifact_bytes_unverified")
    return {
        "role": expected["role"],
        "binding_blockers": blockers,
        "evidence_fields_complete": not blockers,
        "actual_qualification_established": False,
        "real_dispatch_enabled": False,
    }


def guarded_synthetic_fit(
    run: OfflineRun,
    expected: dict[str, dict],
    *,
    binding: Callable[[], RuntimeBinding | None],
    proof: Callable[[httpx.Request], ExactFit | None],
) -> Callable[[httpx.Request], Fit]:
    """Exercise the exact-evidence boundary in an offline transport.

    Only explicitly synthetic evidence is accepted here. Production evidence
    collection, rights review, runtime mapping and dispatch are separate gates.
    The lease identifies this synthetic run, not an actual LM Studio lease.
    """

    def check(request: httpx.Request) -> Fit:
        run.check_time()
        if run.cell is None:
            run.stop("qualification_no_active_cell")
        role = run.cell["model_role"]
        if role == "challenger":
            role = "M2" if run.preflight_results.get("M2") == "qualified" else "M1"
        observed = binding()
        if not isinstance(observed, RuntimeBinding) or observed.synthetic is not True:
            run.stop("qualification_binding_missing")
        now = run.clock()
        if (
            observed.observed_at is None
            or not math.isfinite(observed.observed_at)
            or not 0 <= now - observed.observed_at <= run.budget["memory_poll_target_seconds"]
        ):
            run.stop("qualification_binding_stale")
        blockers = binding_blockers(
            expected[role],
            observed,
            context=run.budget["requested_context_tokens"],
            owned_lease=run.path.name,
            allow_synthetic=True,
        )
        if blockers:
            run.stop("qualification_" + blockers[0])
        exact = proof(request)
        output_limit = run.budget[
            "preflight_output_cap_per_post"
            if run.is_preflight
            else "requested_output_tokens_per_call"
        ]
        blockers = fit_blockers(request.content, exact, observed, output_limit=output_limit)
        if blockers:
            run.stop("qualification_" + blockers[0])
        if not 0 <= run.clock() - observed.observed_at <= run.budget["memory_poll_target_seconds"]:
            run.stop("qualification_binding_stale")
        assert exact is not None
        return Fit(
            exact.request_sha256, exact.input_tokens, exact.output_tokens, exact.context_tokens
        )

    return check
