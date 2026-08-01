import pytest

from jobhunter.translation.base import TranslationError
from jobhunter.translation.integrity import (
    audit_translation_integrity,
    require_translation_integrity,
)
from jobhunter.translation.projection import build_english_projection


def test_translation_integrity_accepts_sane_projection() -> None:
    source = {
        "company": "رادهوش | Radhoosh",
        "job_category": "وب، برنامه‌نویسی و نرم‌افزار",
        "location": "فارس",
        "employment_type": "تمام وقت",
        "salary": "توافقی",
        "description": "توسعه مدل‌های هوش مصنوعی با Python",
        "date_posted": "2026-06-10",
        "language": "mixed",
        "parser_version": "jobinja-detail-v2",
    }
    projection = build_english_projection(
        source,
        translations={
            "رادهوش | Radhoosh": "Radhoosh | Radhoosh",
            "وب، برنامه‌نویسی و نرم‌افزار": "Web, programming, and software",
            "فارس": "Fars",
            "تمام وقت": "Full-time",
            "توافقی": "Negotiable",
            "توسعه مدل‌های هوش مصنوعی با Python": (
                "Develop artificial intelligence models with Python"
            ),
        },
    )

    report = audit_translation_integrity(source, projection)
    assert report.clean is True
    require_translation_integrity(source, projection)


def test_translation_integrity_rejects_company_description_in_company_field() -> None:
    source = {
        "company": "رادهوش | Radhoosh",
        "job_category": "وب، برنامه‌نویسی و نرم‌افزار",
        "location": "فارس",
        "description": "توسعه نرم‌افزار",
        "language": "fa",
        "parser_version": "jobinja-detail-v2",
    }
    projection = build_english_projection(
        source,
        translations={
            "رادهوش | Radhoosh": (
                "Radhoosh was established in 2015 by a group of specialists and has "
                "continued building many software products for customers across several "
                "markets. The company maintains multiple engineering teams, develops "
                "long-running software systems, supports international work, trains "
                "specialists, and continues expanding its technical organization and "
                "delivery capabilities across many projects."
            ),
            "وب، برنامه‌نویسی و نرم‌افزار": "Fars",
            "فارس": "No preference",
            "توسعه نرم‌افزار": "Develop software",
        },
    )

    report = audit_translation_integrity(source, projection)
    assert report.clean is False
    assert any(
        item.code == "suspicious_scalar_expansion" for item in report.findings
    )
    with pytest.raises(TranslationError, match="integrity checks"):
        require_translation_integrity(source, projection)


def test_translation_integrity_rejects_changed_date() -> None:
    source = {
        "title": "مهندس امنیت",
        "description": "تحلیل امنیت",
        "date_posted": "2026-08-01",
        "language": "fa",
        "parser_version": "jobinja-detail-v2",
    }
    projection = build_english_projection(
        source,
        translations={
            "مهندس امنیت": "Security Engineer",
            "تحلیل امنیت": "Security analysis",
        },
    )
    projection.fields["date_posted"] = "2026-07-01"

    report = audit_translation_integrity(source, projection)
    assert any(item.code == "stable_field_changed" for item in report.findings)
