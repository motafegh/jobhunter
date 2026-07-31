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
