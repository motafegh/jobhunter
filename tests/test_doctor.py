from pathlib import Path

from jobhunter.config import Settings
from jobhunter.doctor import CheckStatus, run_doctor
from jobhunter.inference import InferenceConnectionError


class HealthyProvider:
    def list_models(self) -> list[str]:
        return ["model-a"]

    def structured_smoke_test(self, model: str | None = None) -> str:
        return model or "model-a"


class FailingProvider:
    def list_models(self) -> list[str]:
        raise InferenceConnectionError("connection refused")

    def structured_smoke_test(self, model: str | None = None) -> str:
        raise AssertionError("smoke test should not run after connection failure")


def test_doctor_initializes_storage_and_passes_with_healthy_provider(tmp_path: Path) -> None:
    settings = Settings(
        data_dir=tmp_path / "data",
        lm_studio_model="model-a",
    )

    report = run_doctor(settings, HealthyProvider(), perform_smoke_test=True)

    assert report.has_failures is False
    assert settings.data_dir.is_dir()
    assert settings.evidence_dir.is_dir()
    assert settings.database_path.is_file()
    assert all(check.status is CheckStatus.PASS for check in report.checks)


def test_doctor_reports_provider_connection_failure(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path / "data")

    report = run_doctor(settings, FailingProvider())

    assert report.has_failures is True
    lm_studio_check = report.checks[-1]
    assert lm_studio_check.name == "LM Studio"
    assert lm_studio_check.status is CheckStatus.FAILURE
    assert "connection refused" in lm_studio_check.detail
