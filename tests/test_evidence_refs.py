from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    evidence_reference_payload,
)


def test_long_bullet_description_gets_exact_segment_references() -> None:
    fields = {
        "description": (
            "What you'll do ● Build and validate ML models on manufacturing data. "
            "● Work on yield optimization and anomaly detection. "
            "● Design rigorous validation and monitoring for industrial models."
        ),
        "skills": ["Artificial Intelligence", "Python"],
    }

    catalog = build_field_evidence_catalog(fields)

    assert catalog["field:description"].startswith("What you'll do")
    assert catalog["field:description:segment:0"] == (
        "Build and validate ML models on manufacturing data."
    )
    assert catalog["field:description:segment:1"] == (
        "Work on yield optimization and anomaly detection."
    )
    assert catalog["field:description:segment:2"] == (
        "Design rigorous validation and monitoring for industrial models."
    )
    assert catalog["field:skills:0"] == "Artificial Intelligence"
    assert catalog["field:skills:1"] == "Python"
    assert "field:skills:2" not in catalog


def test_section_headings_do_not_leak_into_neighboring_evidence_segments() -> None:
    fields = {
        "description": (
            "What you'll do ● Ensure traceability, reproducibility, and governance of models. "
            "What we're looking for ● Strong industrial ML experience. "
            "Technical skill stack The tools should be strong in. "
            "● Programming: Python (expert) and SQL; MATLAB a plus; some C / C++ helpful"
        )
    }

    catalog = build_field_evidence_catalog(fields)
    segments = {
        value
        for key, value in catalog.items()
        if key.startswith("field:description:segment:") and ":clause:" not in key
    }

    assert "Ensure traceability, reproducibility, and governance of models." in segments
    assert "Strong industrial ML experience." in segments
    assert all("What we're looking for" not in segment for segment in segments)
    assert all("Technical skill stack" not in segment for segment in segments)


def test_mixed_strength_stack_line_gets_clause_references() -> None:
    fields = {
        "description": (
            "Technical skill stack ● Programming: Python (expert) and SQL; "
            "MATLAB a plus; some C / C++ helpful"
        )
    }

    catalog = build_field_evidence_catalog(fields)

    assert catalog["field:description:segment:0"] == (
        "Programming: Python (expert) and SQL; MATLAB a plus; some C / C++ helpful"
    )
    assert catalog["field:description:segment:0:clause:0"] == (
        "Programming: Python (expert) and SQL"
    )
    assert catalog["field:description:segment:0:clause:1"] == "MATLAB a plus"
    assert catalog["field:description:segment:0:clause:2"] == "some C / C++ helpful"


def test_reference_payload_is_sorted_and_includes_exact_text() -> None:
    payload = evidence_reference_payload({"field:z": "Z", "field:a": "A"})

    assert payload == [
        {"id": "field:a", "text": "A"},
        {"id": "field:z", "text": "Z"},
    ]
