"""Owner manual source-only review packet is blind, offline and source-safe."""

from __future__ import annotations

import html
from pathlib import Path
from runpy import run_path

import pytest

PACKET_SCRIPT = run_path(
    str(Path(__file__).resolve().parents[1] / "scripts/build_owner_source_review_packet.py")
)
_case_html = PACKET_SCRIPT["_case_html"]


def _entry(url: str = "https://jobinja.ir/companies/example/jobs/tNhZ/sample") -> dict:
    return {
        "job_id": "tNhZ",
        "canonical_url": url,
        "title_observed": "Example vacancy",
        "semantic_sha256": "a" * 64,
        "fetched_at": "2026-11-12T12:00:00+00:00",
    }


def test_source_only_packet_no_model_answers_and_escape() -> None:
    malicious = '<script>alert("bad")</script>'
    source = {
        "title": malicious,
        "description": "امتیاز محسوب می‌شود " + malicious,
        "skills": ["<img src=x onerror=alert(0)>", "Python"],
        "minimum_experience": "2-4 years",
        "employment_type": "full-time",
    }
    body = _case_html(_entry(), source, 1, 1)
    assert malicious not in body
    assert html.escape(malicious) in body
    assert '<img src=x onerror=alert(0)>' not in body
    assert "<pre" in body and "lang=\"fa\"" in body
    assert "data-answer=\"mandatory_requirements\"" in body
    assert "data-answer=\"preferred_optional\"" in body
    assert "data-answer=\"confidence\"" in body
    assert "JobHunter candidate" not in body
    assert "expected answer" not in body


@pytest.mark.parametrize(
    "url",
    (
        "javascript:alert(1)",
        "http://jobinja.ir/companies/example/jobs/tNhZ",
        "https://jobinja.ir.evil.example/jobs/x",
        "https://someone:secret@jobinja.ir/jobs/x",
        "https://example.com/jobs/tNhZ",
    ),
)
def test_source_only_packet_rejects_untrusted_external_links(url: str) -> None:
    with pytest.raises(ValueError, match="approved Jobinja"):
        _case_html(_entry(url), {"description": "Original job"}, 1, 1)


def test_model_content_never_present_as_input_to_renderer() -> None:
    entry = _entry()
    assert "model" not in entry
    source = {
        "title": "Technical engineer",
        "description": "این کار شامل Python است.",
        "skills": ["Python"],
    }
    body = _case_html(entry, source, 1, 4)
    assert "Original employer description" in body
    assert "Separate job-board skill tags" in body
    assert "Source evidence supporting" in body
    assert "SOURCE CASE 1/4" in body
    assert "English candidate" not in body
