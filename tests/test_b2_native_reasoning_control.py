"""No-network contract tests for B2 native reasoning-off semantic trials."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def scripts(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    v2 = importlib.import_module("probe_b2_native_reasoning_off")
    v3 = importlib.import_module("probe_b2_native_corrective_v3")
    return v2, v3


def test_native_reasoning_disabled_and_no_remote_or_chat_storage(scripts) -> None:
    v2, _ = scripts
    assert v2.BASE == "http://127.0.0.1:18080"
    assert v2.MODEL == "gemma-4-e4b-it-ud"
    assert v2.CONTRACT.endswith("v2")
    assert v2.MAX_OUTPUT_TOKENS <= 1500
    assert v2.TIMEOUT_SECONDS <= 40
    body = v2._request_for_job(prompt="Evaluate this source.", description="Test")
    assert body == {
        "model": v2.MODEL,
        "system_prompt": "Evaluate this source.",
        "input": "Test",
        "temperature": 0,
        "reasoning": "off",
        "max_output_tokens": 1400,
        "stream": False,
        "store": False,
    }


def test_native_output_excludes_reasoning_and_retains_visible_answer(scripts) -> None:
    v2, _ = scripts
    text, count = v2._answer_parts(
        {
            "output": [
                {"type": "reasoning", "content": "Private analysis not for answer"},
                {"type": "message", "content": '{"duties":["Build Python APIs"]}'},
                {"type": "message", "content": ""},
            ]
        }
    )
    assert count == 2
    assert "Private analysis" not in text
    assert "Build Python APIs" in text
    assert v2._answer_parts({"output": "invalid"}) == ("", 0)


def test_fixed_v1_prompt_retained_in_v2_and_one_bounded_corrective(scripts) -> None:
    v2, v3 = scripts
    assert v2.PROMPT in v3.CORRECTIVE_PROMPT
    assert v3.CONTRACT.endswith("v3")
    assert v3.CORRECTIVE_PROMPT != v2.PROMPT
    assert len(v3.CORRECTIVE_PROMPT) < 750
    assert "duties" in v3.CORRECTIVE_PROMPT
    assert "eligibility paths" in v3.CORRECTIVE_PROMPT
    assert "Explicit advantages" in v3.CORRECTIVE_PROMPT
    assert "LangChain" not in v3.CORRECTIVE_PROMPT
    assert "Kubernetes" not in v3.CORRECTIVE_PROMPT


def test_source_privacy_fence_prevents_public_artifact_output(scripts, tmp_path) -> None:
    v2, _ = scripts
    # Path rejection occurs before any model call or database open.
    with pytest.raises(ValueError, match="ignored local data"):
        v2.run_trial(
            tmp_path / "not-present.sqlite3",
            tmp_path / "public-results",
        )


def test_candidate_semantics_are_not_accepted_by_schema_parser(scripts) -> None:
    v2, _ = scripts
    valid = v2._json_array_counts(
        '{"duties":[],"requirements":["Invented"],"preferences":[],'
        '"alternatives":[],"arrangements":[],"uncertainties":[],'
        '"work_implied_capabilities":[]}'
    )
    assert valid["is_json"] is True
    assert valid["field_lengths"]["requirements"] == 1
    # Valid transport and JSON do not establish source correctness.
    assert v2.CONTRACT == "jobhunter-b2-original-context-native-reasoning-off-v2"


def test_b0_frozen_identity_required(scripts) -> None:
    v2, _ = scripts
    assert v2.EXPECTED_B0_SHA256 == (
        "bef0e876819735cba12a712271b7ae4eef0b397c82edd8ee6c2aec7d1bb91ebe"
    )
    assert "source_database_sha256" not in v2._request_for_job(prompt=v2.PROMPT, description="mock")
