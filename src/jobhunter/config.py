"""Typed configuration loading for JobHunter."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, model_validator

from jobhunter.search_registry import (
    ExpandedKeywordSearch,
    SearchCatalog,
    expand_keyword_searches,
    load_search_catalog,
    normalize_search_term,
    resolve_pack_names,
)
from jobhunter.sources import JobinjaUrlError, canonicalize_search_url


class ConfigLoadError(RuntimeError):
    """Raised when a JobHunter configuration file cannot be loaded."""


class JobinjaSearchDefinition(BaseModel):
    """One user-controlled raw Jobinja search URL."""

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


class JobinjaKeywordGroupDefinition(BaseModel):
    """One custom bilingual or domain-specific Jobinja keyword group."""

    model_config = ConfigDict(extra="forbid")

    name: str
    terms: list[str]
    enabled: bool = True
    max_pages: int = Field(default=1, ge=1, le=50)

    @model_validator(mode="after")
    def normalize(self) -> JobinjaKeywordGroupDefinition:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Jobinja keyword group name must not be empty")

        unique_terms: list[str] = []
        seen: set[str] = set()
        for raw_term in self.terms:
            term = " ".join(raw_term.split())
            normalized = normalize_search_term(term)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            unique_terms.append(term)
        if not unique_terms:
            raise ValueError("Jobinja keyword group must contain at least one term")
        if len(unique_terms) > 200:
            raise ValueError("Jobinja keyword group may contain at most 200 unique terms")
        self.terms = unique_terms
        return self


class Settings(BaseModel):
    """Validated application settings loaded from TOML and environment overrides."""

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
    jobinja_search_catalog_path: Path | None = None
    jobinja_searches: list[JobinjaSearchDefinition] = Field(default_factory=list)
    jobinja_search_profiles: list[str] = Field(default_factory=list)
    jobinja_search_packs: list[str] = Field(default_factory=list)
    jobinja_keyword_groups: list[JobinjaKeywordGroupDefinition] = Field(
        default_factory=list
    )
    jobinja_excluded_terms: list[str] = Field(default_factory=list)
    jobinja_default_keyword_max_pages: int = Field(default=1, ge=1, le=50)
    jobinja_search_request_budget: int = Field(default=40, ge=1, le=500)
    jobinja_max_expanded_searches: int = Field(default=40, ge=1, le=500)
    jobinja_sync_missing_limit: int = Field(default=10, ge=0, le=50)
    jobinja_sync_refresh_limit: int = Field(default=5, ge=0, le=50)
    jobinja_refresh_after_hours: float = Field(default=24.0, gt=0, le=8760)

    translation_enabled: bool = False
    translation_auto_after_sync: bool = False
    translation_provider: str = "google-cloud"
    translation_target_language: str = "en"
    translation_batch_limit: int = Field(default=20, ge=1, le=50)
    translation_timeout_seconds: float = Field(default=30.0, gt=0, le=120)
    translation_max_retries: int = Field(default=1, ge=0, le=5)
    translation_request_character_target: int = Field(
        default=5_000,
        ge=1_000,
        le=100_000,
    )
    google_translation_api_key: str | None = None
    google_translation_model: str = "nmt"

    log_level: str = "INFO"

    @model_validator(mode="after")
    def normalize(self) -> Settings:
        self.data_dir = self.data_dir.expanduser()
        self.evidence_dir = (self.evidence_dir or self.data_dir / "evidence").expanduser()
        self.database_path = (
            self.database_path or self.data_dir / "jobhunter.sqlite3"
        ).expanduser()
        if self.jobinja_search_catalog_path is not None:
            self.jobinja_search_catalog_path = self.jobinja_search_catalog_path.expanduser()

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
        if self.google_translation_api_key is not None:
            self.google_translation_api_key = self.google_translation_api_key.strip() or None
        self.google_translation_model = self.google_translation_model.strip() or "nmt"

        self.jobinja_user_agent = self.jobinja_user_agent.strip()
        if not self.jobinja_user_agent:
            raise ValueError("jobinja_user_agent must not be empty")

        if self.translation_provider not in {"google-cloud"}:
            raise ValueError("translation_provider currently supports only 'google-cloud'")
        if self.translation_target_language != "en":
            raise ValueError("translation_target_language currently supports only 'en'")
        if self.translation_auto_after_sync and not self.translation_enabled:
            raise ValueError(
                "translation_auto_after_sync requires translation_enabled = true"
            )

        search_names: set[str] = set()
        for search in self.jobinja_searches:
            normalized_name = search.name.casefold()
            if normalized_name in search_names:
                raise ValueError(f"Duplicate Jobinja search name: {search.name!r}")
            search_names.add(normalized_name)

        group_names: set[str] = set()
        for group in self.jobinja_keyword_groups:
            normalized_name = group.name.casefold()
            if normalized_name in group_names:
                raise ValueError(f"Duplicate Jobinja keyword group name: {group.name!r}")
            group_names.add(normalized_name)

        self.jobinja_search_profiles = list(
            dict.fromkeys(
                name.strip()
                for name in self.jobinja_search_profiles
                if name.strip()
            )
        )
        self.jobinja_search_packs = list(
            dict.fromkeys(
                name.strip()
                for name in self.jobinja_search_packs
                if name.strip()
            )
        )
        catalog = self.search_catalog()
        try:
            resolve_pack_names(
                pack_names=tuple(self.jobinja_search_packs),
                profile_names=tuple(self.jobinja_search_profiles),
                catalog=catalog,
            )
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

        excluded_terms: list[str] = []
        seen_excluded: set[str] = set()
        for raw_term in self.jobinja_excluded_terms:
            term = " ".join(raw_term.split())
            normalized = normalize_search_term(term)
            if not normalized or normalized in seen_excluded:
                continue
            seen_excluded.add(normalized)
            excluded_terms.append(term)
        self.jobinja_excluded_terms = excluded_terms
        return self

    def search_catalog(self) -> SearchCatalog:
        """Load the packaged catalog or a user-supplied replacement TOML catalog."""

        return load_search_catalog(self.jobinja_search_catalog_path)

    def expanded_keyword_searches(self) -> tuple[ExpandedKeywordSearch, ...]:
        """Expand configured profiles, packs, and custom groups."""

        custom_groups = tuple(
            (group.name, tuple(group.terms), group.max_pages)
            for group in self.jobinja_keyword_groups
            if group.enabled
        )
        return expand_keyword_searches(
            pack_names=tuple(self.jobinja_search_packs),
            profile_names=tuple(self.jobinja_search_profiles),
            custom_groups=custom_groups,
            excluded_terms=tuple(self.jobinja_excluded_terms),
            default_max_pages=self.jobinja_default_keyword_max_pages,
            catalog=self.search_catalog(),
        )

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> Settings:
        """Load settings from TOML and environment overrides."""

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
            "JOBHUNTER_JOBINJA_SEARCH_CATALOG_PATH": "jobinja_search_catalog_path",
            "JOBHUNTER_JOBINJA_SEARCH_REQUEST_BUDGET": "jobinja_search_request_budget",
            "JOBHUNTER_JOBINJA_MAX_EXPANDED_SEARCHES": "jobinja_max_expanded_searches",
            "JOBHUNTER_JOBINJA_SYNC_MISSING_LIMIT": "jobinja_sync_missing_limit",
            "JOBHUNTER_JOBINJA_SYNC_REFRESH_LIMIT": "jobinja_sync_refresh_limit",
            "JOBHUNTER_JOBINJA_REFRESH_AFTER_HOURS": "jobinja_refresh_after_hours",
            "JOBHUNTER_TRANSLATION_ENABLED": "translation_enabled",
            "JOBHUNTER_TRANSLATION_AUTO_AFTER_SYNC": "translation_auto_after_sync",
            "JOBHUNTER_TRANSLATION_PROVIDER": "translation_provider",
            "JOBHUNTER_TRANSLATION_BATCH_LIMIT": "translation_batch_limit",
            "JOBHUNTER_TRANSLATION_TIMEOUT_SECONDS": "translation_timeout_seconds",
            "JOBHUNTER_TRANSLATION_MAX_RETRIES": "translation_max_retries",
            "JOBHUNTER_TRANSLATION_REQUEST_CHARACTER_TARGET": (
                "translation_request_character_target"
            ),
            "JOBHUNTER_GOOGLE_TRANSLATION_API_KEY": "google_translation_api_key",
            "JOBHUNTER_GOOGLE_TRANSLATION_MODEL": "google_translation_model",
            "JOBHUNTER_LOG_LEVEL": "log_level",
        }
        for environment_name, field_name in environment_fields.items():
            if environment_name in os.environ:
                values[field_name] = os.environ[environment_name]

        return cls.model_validate(values)
