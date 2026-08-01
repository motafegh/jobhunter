from pathlib import Path

import pytest
from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings


def test_loads_toml_and_applies_environment_override(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
data_dir = "custom-data"
lm_studio_base_url = "http://127.0.0.1:1234/v1/"
inference_max_retries = 2
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("JOBHUNTER_LOG_LEVEL", "debug")

    settings = Settings.load(config_path)

    assert settings.data_dir == Path("custom-data")
    assert settings.evidence_dir == Path("custom-data/evidence")
    assert settings.database_path == Path("custom-data/jobhunter.sqlite3")
    assert settings.lm_studio_base_url == "http://127.0.0.1:1234/v1"
    assert settings.inference_max_retries == 2
    assert settings.log_level == "DEBUG"


def test_loads_and_canonicalizes_jobinja_searches(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
jobinja_request_delay_seconds = 2.5

[[jobhunter.jobinja_searches]]
name = "AI roles"
url = "https://www.jobinja.ir/jobs/?filters%5Bkeywords%5D%5B0%5D=ai&page=4"
enabled = true
max_pages = 3
""".strip(),
        encoding="utf-8",
    )

    settings = Settings.load(config_path)

    assert settings.jobinja_request_delay_seconds == 2.5
    assert len(settings.jobinja_searches) == 1
    assert settings.jobinja_searches[0].name == "AI roles"
    assert settings.jobinja_searches[0].url == (
        "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=ai"
    )
    assert settings.jobinja_searches[0].max_pages == 3


def test_loads_profiles_packs_custom_groups_and_exclusions(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
jobinja_search_profiles = ["ai-focused"]
jobinja_search_packs = ["python-data"]
jobinja_excluded_terms = ["Python", "  PYTHON  "]
jobinja_search_request_budget = 25

[[jobhunter.jobinja_keyword_groups]]
name = "My security roles"
terms = ["امنیت‌سایبری", "امنيت سایبری", "Security Automation"]
max_pages = 2
""".strip(),
        encoding="utf-8",
    )

    settings = Settings.load(config_path)
    searches = settings.expanded_keyword_searches()
    terms = {search.term for search in searches}

    assert settings.jobinja_search_request_budget == 25
    assert settings.jobinja_keyword_groups[0].terms == [
        "امنیت‌سایبری",
        "Security Automation",
    ]
    assert "Python" not in terms
    assert "هوش مصنوعی" in terms
    assert "Security Automation" in terms


def test_loads_external_search_catalog_from_configuration(tmp_path: Path) -> None:
    catalog_path = tmp_path / "catalog.toml"
    catalog_path.write_text(
        """
catalog_version = "personal-v1"
[profiles]
personal = ["hybrid"]
[packs.hybrid]
description = "Personal"
terms = ["AI Security Engineer", "مهندس امنیت هوش مصنوعی"]
""".strip(),
        encoding="utf-8",
    )
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        f"""
[jobhunter]
jobinja_search_catalog_path = "{catalog_path}"
jobinja_search_profiles = ["personal"]
""".strip(),
        encoding="utf-8",
    )

    settings = Settings.load(config_path)

    assert settings.search_catalog().version == "personal-v1"
    assert {item.term for item in settings.expanded_keyword_searches()} == {
        "AI Security Engineer",
        "مهندس امنیت هوش مصنوعی",
    }


def test_translation_settings_accept_google_key_from_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
translation_enabled = true
translation_auto_after_sync = true
translation_provider = "google-cloud"
google_translation_model = "nmt"
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("JOBHUNTER_GOOGLE_TRANSLATION_API_KEY", "  secret-key  ")

    settings = Settings.load(config_path)

    assert settings.translation_enabled is True
    assert settings.translation_auto_after_sync is True
    assert settings.google_translation_api_key == "secret-key"


def test_translation_auto_sync_requires_translation_enabled(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
translation_enabled = false
translation_auto_after_sync = true
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="translation_auto_after_sync"):
        Settings.load(config_path)


def test_missing_explicit_configuration_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigLoadError, match="does not exist"):
        Settings.load(tmp_path / "missing.toml")


def test_unknown_configuration_field_is_rejected(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
unknown_setting = true
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        Settings.load(config_path)


def test_duplicate_jobinja_search_names_are_rejected(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]

[[jobhunter.jobinja_searches]]
name = "AI roles"
url = "https://jobinja.ir/jobs?q=ai"

[[jobhunter.jobinja_searches]]
name = "ai ROLES"
url = "https://jobinja.ir/jobs?q=python"
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="Duplicate Jobinja search name"):
        Settings.load(config_path)


def test_duplicate_keyword_group_names_are_rejected(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]

[[jobhunter.jobinja_keyword_groups]]
name = "Security"
terms = ["Security Engineer"]

[[jobhunter.jobinja_keyword_groups]]
name = "SECURITY"
terms = ["مهندس امنیت"]
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="Duplicate Jobinja keyword group name"):
        Settings.load(config_path)


def test_unknown_search_profile_is_rejected(tmp_path: Path) -> None:
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text(
        """
[jobhunter]
jobinja_search_profiles = ["does-not-exist"]
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="Unknown Jobinja search profile"):
        Settings.load(config_path)
