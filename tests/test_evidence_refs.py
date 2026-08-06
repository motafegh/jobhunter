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
    assert catalog["field:description:segment:0"] == "What you'll do"
    assert catalog["field:description:segment:1"] == (
        "Build and validate ML models on manufacturing data."
    )
    assert catalog["field:description:segment:2"] == (
        "Work on yield optimization and anomaly detection."
    )
    assert catalog["field:skills:0"] == "Artificial Intelligence"
    assert catalog["field:skills:1"] == "Python"
    assert "field:skills:2" not in catalog


def test_reference_payload_is_sorted_and_includes_exact_text() -> None:
    payload = evidence_reference_payload({"field:z": "Z", "field:a": "A"})

    assert payload == [
        {"id": "field:a", "text": "A"},
        {"id": "field:z", "text": "Z"},
    ]
