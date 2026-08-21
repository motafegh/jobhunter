from jobhunter.evidence_refs import (
    build_field_evidence_catalog,
    build_requirement_coverage_plan,
    build_responsibility_coverage_plan,
    evidence_reference_payload,
    requirement_coverage_payload,
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
    assert catalog["field:description:segment:0:clause:0:item:0"] == "Python (expert)"
    assert catalog["field:description:segment:0:clause:0:item:1"] == "SQL"
    assert catalog["field:description:segment:0:clause:1"] == "MATLAB a plus"
    assert catalog["field:description:segment:0:clause:2"] == "some C / C++ helpful"


def test_reference_payload_is_sorted_and_includes_exact_text() -> None:
    payload = evidence_reference_payload({"field:z": "Z", "field:a": "A"})

    assert payload == [
        {"id": "field:a", "text": "A"},
        {"id": "field:z", "text": "Z"},
    ]


def test_requirement_coverage_plan_tracks_sections_optionality_and_structured_fields() -> None:
    fields = {
        "minimum_experience": "three to six years",
        "education": "Master's degree",
        "description": (
            "What we're looking for ● Strong industrial ML experience. "
            "Technical skill stack The tools you should be strong in. We don't expect every "
            "single item — depth in the core stack matters most. "
            "● Programming: Python (expert) and SQL; MATLAB a plus; some C / C++ helpful "
            "● Data & statistics: pandas, NumPy, SciPy, statsmodels; "
            "multivariate analysis (PCA / PLS) "
            "● Cloud & edge: AWS, GCP, or Azure; industrial / edge deployment a plus"
        ),
    }

    plan = build_requirement_coverage_plan(fields)

    assert plan["field:minimum_experience"]["obligation_hint"] == "required"
    assert plan["field:education"]["allow_exclusion"] is False
    assert plan["field:description:segment:0"]["obligation_hint"] == "required"
    assert plan["field:description:segment:1"]["obligation_hint"] == "context_only"
    assert plan["field:description:segment:2:clause:0:item:0"]["obligation_hint"] == (
        "contextual"
    )
    assert plan["field:description:segment:2:clause:0:item:1"]["obligation_hint"] == (
        "contextual"
    )
    assert plan["field:description:segment:2:clause:1"]["obligation_hint"] == (
        "preferred"
    )
    assert plan["field:description:segment:2:clause:2"]["obligation_hint"] == (
        "preferred"
    )
    assert plan["field:description:segment:3:clause:0"]["obligation_hint"] == (
        "contextual"
    )
    assert plan["field:description:segment:3:clause:1"]["obligation_hint"] == (
        "contextual"
    )
    assert plan["field:description:segment:4:clause:0"]["obligation_hint"] == (
        "contextual"
    )
    assert plan["field:description:segment:4:clause:1"]["obligation_hint"] == (
        "preferred"
    )
    assert requirement_coverage_payload(plan)[0]["id"] == "field:description:segment:0"
    assert "text" not in requirement_coverage_payload(plan)[0]


def test_preferred_qualification_heading_stays_with_exact_requirement_evidence() -> None:
    fields = {
        "description": (
            "Responsibilities include designing VPNs and preparing documentation. "
            "Preferred qualifications include Cisco ISE, CCNP Security, or PCNSE."
        )
    }

    catalog = build_field_evidence_catalog(fields)
    requirement_plan = build_requirement_coverage_plan(fields)
    responsibility_plan = build_responsibility_coverage_plan(fields)

    assert catalog["field:description:segment:1"] == (
        "Preferred qualifications include Cisco ISE, CCNP Security, or PCNSE."
    )
    assert requirement_plan["field:description:segment:1"]["obligation_hint"] == (
        "preferred"
    )
    assert responsibility_plan == {
        "field:description:segment:0": (
            "include designing VPNs and preparing documentation."
        )
    }


def test_explicit_position_responsibility_clause_enters_duty_coverage() -> None:
    fields = {
        "description": (
            "We are seeking a senior engineer. This position will be responsible for "
            "designing security solutions, managing firewalls, and implementing security "
            "policies. Responsibilities include designing VPNs and troubleshooting issues."
        )
    }

    plan = build_responsibility_coverage_plan(fields)

    assert plan == {
        "field:description:segment:1": (
            "designing security solutions, managing firewalls, and implementing security "
            "policies."
        ),
        "field:description:segment:2": (
            "include designing VPNs and troubleshooting issues."
        ),
    }


def test_pre_heading_candidate_experience_enters_requirement_coverage() -> None:
    evidence = (
        "We are looking for a Senior Network Security Engineer with experience in "
        "designing, implementing, and managing enterprise network security infrastructure."
    )
    fields = {
        "description": (
            evidence
            + " This position will be responsible for implementing security policies."
        )
    }

    plan = build_requirement_coverage_plan(fields)

    assert plan == {
        "field:description:segment:0": {
            "text": evidence,
            "source_kind": "candidate_experience",
            "obligation_hint": "required",
            "allow_exclusion": False,
        }
    }


def test_pre_heading_candidate_duties_enter_responsibility_coverage() -> None:
    evidence = (
        "We are looking for an infrastructure specialist to assess server security posture "
        "and develop hardening requirements."
    )
    fields = {"description": evidence + " Key Responsibilities: Review security tickets."}

    plan = build_responsibility_coverage_plan(fields)

    assert plan == {
        "field:description:segment:0": evidence,
        "field:description:segment:1": "Review security tickets.",
    }


def test_requirement_word_inside_qualification_is_not_treated_as_heading() -> None:
    fields = {
        "description": (
            "Specialized Competencies: Mastery of Windows Server hardening; "
            "Ability to prepare documentation and communicate security requirements "
            "to technical teams."
        )
    }

    catalog = build_field_evidence_catalog(fields)
    plan = build_requirement_coverage_plan(fields)

    assert catalog["field:description:segment:0:clause:1"] == (
        "Ability to prepare documentation and communicate security requirements "
        "to technical teams."
    )
    assert "field:description:segment:1" not in catalog
    assert plan["field:description:segment:0:clause:1"]["text"].endswith(
        "to technical teams."
    )


def test_responsibility_coverage_plan_tracks_exact_duty_clauses() -> None:
    fields = {
        "description": (
            "What you'll do ● Build models. "
            "● Handle sensor data; build robust pipelines. "
            "What we're looking for ● Python"
        )
    }

    plan = build_responsibility_coverage_plan(fields)

    assert plan == {
        "field:description:segment:0": "Build models.",
        "field:description:segment:1:clause:0": "Handle sensor data",
        "field:description:segment:1:clause:1": "build robust pipelines.",
    }
