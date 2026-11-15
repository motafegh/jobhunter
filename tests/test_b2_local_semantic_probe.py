"""No-network tests for the bounded optional LM Studio semantic probe."""

from __future__ import annotations

from pathlib import Path
from runpy import run_path
from urllib.request import ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
PROBE = run_path(str(ROOT / "scripts/probe_b2_local_semantics.py"))


def test_local_probe_fixed_loopback_and_no_proxy() -> None:
    assert PROBE["ENDPOINT"] == "http://127.0.0.1:18080"
    assert PROBE["MODEL"] == "gemma-4-e4b-it-ud"
    assert PROBE["JOBS"] == ("tNhZ", "tMps", "tNDx", "tMjm")
    assert 0 < PROBE["MAX_TOKENS"] <= 1000
    assert 0 < PROBE["TIMEOUT_SECONDS"] <= 100
    opener = PROBE["_client"]()
    # An empty ProxyHandler disables the environment default; urllib can omit
    # that empty handler entirely because it registers no proxy methods.
    handlers = [handler for handler in opener.handlers if isinstance(handler, ProxyHandler)]
    assert not handlers or all(handler.proxies == {} for handler in handlers)


def test_simple_model_prompt_preserves_employer_vs_inference() -> None:
    prompt = PROBE["PROMPT"]
    assert len(prompt) < 500
    assert "employer explicitly requires" in prompt
    assert "implied by" in prompt
    assert "Preserve OR alternatives" in prompt
    assert "Do not invent experience" in prompt
    assert "LangChain" not in prompt and "Kubernetes" not in prompt
    assert PROBE["PROBE_CONTRACT"].endswith("v1")


def test_probe_model_output_shape_records_partial_success() -> None:
    parser = PROBE["_json_array_counts"]
    valid = parser('{"duties":["Build APIs"],"requirements":[],"preferences":[]}')
    assert valid["is_json"] is True
    assert valid["valid_top_level"] is True
    assert valid["field_lengths"]["duties"] == 1
    assert "alternatives" in valid["missing_fields"]
    bad = parser("Model output in non-JSON prose")
    assert bad["is_json"] is False
    assert bad["valid_top_level"] is False
    fence = chr(96) * 3
    fenced = parser(fence + 'json\n{"duties":[]}\n' + fence)
    assert fenced["is_json"] is True
    assert fenced["field_lengths"]["duties"] == 0
