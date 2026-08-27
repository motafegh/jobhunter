from pathlib import Path

from jobhunter.config import Settings
from jobhunter.work_intelligence_service import build_work_intelligence_service


def test_work_intelligence_prefers_analysis_model_over_capability_model(tmp_path: Path) -> None:
    settings = Settings(
        data_dir=tmp_path,
        database_path=tmp_path / "jobhunter.sqlite3",
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
    )

    service = build_work_intelligence_service(settings)

    assert service._work_model == "analysis-model"
    assert service._provider is not None
    assert service._provider._model == "analysis-model"
