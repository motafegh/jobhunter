from jobhunter.translation.projection import (
    build_english_projection,
    collect_translatable_texts,
    translation_required,
)


def test_mixed_source_projection_translates_only_persian_segments() -> None:
    fields = {
        "title": "مهندس هوش مصنوعی",
        "location": "تهران",
        "skills": ["Python", "Docker", "یادگیری ماشین"],
        "description": "تسلط بر Python و آشنایی با Docker",
        "date_posted": "2026-08-01",
        "language": "mixed",
        "parser_version": "jobinja-detail-v2",
    }

    assert collect_translatable_texts(fields) == (
        "مهندس هوش مصنوعی",
        "تهران",
        "یادگیری ماشین",
        "تسلط بر Python و آشنایی با Docker",
    )
    projection = build_english_projection(
        fields,
        translations={
            "مهندس هوش مصنوعی": "Artificial Intelligence Engineer",
            "تهران": "Tehran",
            "یادگیری ماشین": "Machine Learning",
            "تسلط بر Python و آشنایی با Docker": (
                "Proficiency in Python and familiarity with Docker"
            ),
        },
    )

    assert projection.fields["title"] == "Artificial Intelligence Engineer"
    assert projection.fields["skills"] == ["Python", "Docker", "Machine Learning"]
    assert projection.segment_provenance["skills[0]"] == "native"
    assert projection.segment_provenance["skills[2]"] == "translated"
    assert projection.translated_segment_count == 4
    assert projection.native_segment_count == 3
    assert "Job description:" in projection.document
    assert "parser_version" not in projection.fields
    assert "language" not in projection.fields


def test_native_english_projection_requires_no_translation() -> None:
    fields = {
        "title": "Security Engineer",
        "skills": ["Python", "SIEM"],
        "description": "Build detection automation.",
        "language": "en",
        "parser_version": "jobinja-detail-v2",
    }

    assert translation_required(fields) is False
    projection = build_english_projection(fields, translations={})

    assert projection.fields["title"] == "Security Engineer"
    assert projection.translated_segment_count == 0
    assert projection.native_segment_count == 4
