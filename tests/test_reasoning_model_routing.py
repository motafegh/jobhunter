from pathlib import Path

from jobhunter.capability_service import build_capability_intelligence_service
from jobhunter.config import Settings
from jobhunter.role_blueprint_service import build_role_blueprint_service


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        database_path=tmp_path / "jobhunter.sqlite3",
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
        blueprint_lm_studio_model="blueprint-model",
    )


def test_capability_builder_uses_dedicated_capability_model(tmp_path: Path) -> None:
    service = build_capability_intelligence_service(_settings(tmp_path))

    assert service._analysis_model == "analysis-model"
    assert service._capability_model == "capability-model"
    assert service._provider._model == "capability-model"


def test_blueprint_builder_keeps_three_model_roles_distinct(tmp_path: Path) -> None:
    service = build_role_blueprint_service(_settings(tmp_path))

    assert service._analysis_model == "analysis-model"
    assert service._capability_model == "capability-model"
    assert service._blueprint_model == "blueprint-model"
    assert service._provider._model == "blueprint-model"
