"""Typed configuration loading for JobHunter."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, model_validator

from jobhunter.sources import JobinjaUrlError, canonicalize_search_url


class ConfigLoadError(RuntimeError):
    """Raised when a JobHunter configuration file cannot be loaded."""


class JobinjaSearchDefinition(BaseModel):
    """One user-controlled Jobinja search executed by discovery runs."""

    model_config = ConfigDict(extra="forbid")

    name: str
    url: str
    enabled: bool = True
    max_pages: int = Field(default=1, ge=1, le=50)

    @model_validator(mode="after")
    def normalize(self) -> JobinjaSearchDefinition:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Jobinja search name must not be empty")
        try:
            self.url = canonicalize_search_url(self.url)
        except JobinjaUrlError as exc:
            raise ValueError(str(exc)) from exc
        return self


class Settings(BaseModel):
    """Validated application settings.

    Values are loaded from an optional TOML file and then overridden by
    ``JOBHUNTER_*`` environment variables.
    """

    model_config = ConfigDict(extra="forbid")

    data_dir: Path = Path("data")
    evidence_dir: Path | None = None
    database_path: Path | None = None

    lm_studio_base_url: str = "http://127.0.0.1:1234/v1"
    lm_studio_model: str | None = None
    lm_studio_api_token: str | None = None
    inference_timeout_seconds: float = Field(default=30.0, gt=0)
    inference_max_retries: int = Field(default=1, ge=0, le=5)

    jobinja_user_agent: str = "JobHunter/0.1 (local personal career research)"
    jobinja_request_timeout_seconds: float = Field(default=30.0, gt=0, le=120)
    jobinja_request_delay_seconds: float = Field(default=1.0, ge=0, le=60)
    jobinja_searches: list[JobinjaSearchDefinition] = Field(default_factory=list)

    log_level: str = "INFO"

    @model_validator(mode="after")
    def normalize(self) -> Settings:
        self.data_dir = self.data_dir.expanduser()
        self.evidence_dir = (self.evidence_dir or self.data_dir / "evidence").expanduser()
        self.database_path = (
            self.database_path or self.data_dir / "jobhunter.sqlite3"
        ).expanduser()

        self.lm_studio_base_url = self.lm_studio_base_url.rstrip("/")
        parsed = urlparse(self.lm_studio_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("lm_studio_base_url must be an absolute HTTP(S) URL")

        normalized_level = self.log_level.upper()
        if normalized_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("log_level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
        self.log_level = normalized_level

        if self.lm_studio_model is not None:
            self.lm_studio_model = self.lm_studio_model.strip() or None
        if self.lm_studio_api_token is not None:
            self.lm_studio_api_token = self.lm_studio_api_token.strip() or None

        self.jobinja_user_agent = self.jobinja_user_agent.strip()
        if not self.jobinja_user_agent:
            raise ValueError("jobinja_user_agent must not be empty")

        search_names: set[str] = set()
        for search in self.jobinja_searches:
            normalized_name = search.name.casefold()
            if normalized_name in search_names:
                raise ValueError(f"Duplicate Jobinja search name: {search.name!r}")
            search_names.add(normalized_name)

        return self

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> Settings:
        """Load settings from TOML and environment overrides.

        The default file is ``jobhunter.toml`` in the current directory. A
        missing default file is valid. An explicitly supplied missing file is
        an error.
        """

        explicit_path = config_path is not None
        selected_path = Path(
            config_path or os.environ.get("JOBHUNTER_CONFIG", "jobhunter.toml")
        ).expanduser()

        values: dict[str, Any] = {}
        if selected_path.exists():
            try:
                with selected_path.open("rb") as file_handle:
                    parsed = tomllib.load(file_handle)
            except (OSError, tomllib.TOMLDecodeError) as exc:
                raise ConfigLoadError(
                    f"Could not load configuration from {selected_path}: {exc}"
                ) from exc

            section = parsed.get("jobhunter", parsed)
            if not isinstance(section, dict):
                raise ConfigLoadError(
                    f"Configuration section in {selected_path} must be a table"
                )
            values.update(section)
        elif explicit_path:
            raise ConfigLoadError(f"Configuration file does not exist: {selected_path}")

        environment_fields = {
            "JOBHUNTER_DATA_DIR": "data_dir",
            "JOBHUNTER_EVIDENCE_DIR": "evidence_dir",
            "JOBHUNTER_DATABASE_PATH": "database_path",
            "JOBHUNTER_LM_STUDIO_BASE_URL": "lm_studio_base_url",
            "JOBHUNTER_LM_STUDIO_MODEL": "lm_studio_model",
            "JOBHUNTER_LM_STUDIO_API_TOKEN": "lm_studio_api_token",
            "JOBHUNTER_INFERENCE_TIMEOUT_SECONDS": "inference_timeout_seconds",
            "JOBHUNTER_INFERENCE_MAX_RETRIES": "inference_max_retries",
            "JOBHUNTER_JOBINJA_USER_AGENT": "jobinja_user_agent",
            "JOBHUNTER_JOBINJA_REQUEST_TIMEOUT_SECONDS": (
                "jobinja_request_timeout_seconds"
            ),
            "JOBHUNTER_JOBINJA_REQUEST_DELAY_SECONDS": "jobinja_request_delay_seconds",
            "JOBHUNTER_LOG_LEVEL": "log_level",
        }
        for environment_name, field_name in environment_fields.items():
            if environment_name in os.environ:
                values[field_name] = os.environ[environment_name]

        return cls.model_validate(values)
