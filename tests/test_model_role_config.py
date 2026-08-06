from jobhunter.config import Settings


def test_capability_and_blueprint_models_fall_back_through_analysis() -> None:
    settings = Settings(analysis_lm_studio_model="analysis-model")

    assert settings.effective_capability_lm_studio_model() == "analysis-model"
    assert settings.effective_blueprint_lm_studio_model() == "analysis-model"


def test_dedicated_capability_and_blueprint_models_override_fallbacks() -> None:
    settings = Settings(
        lm_studio_model="general-model",
        analysis_lm_studio_model="analysis-model",
        capability_lm_studio_model="capability-model",
        blueprint_lm_studio_model="blueprint-model",
    )

    assert settings.effective_analysis_lm_studio_model() == "analysis-model"
    assert settings.effective_capability_lm_studio_model() == "capability-model"
    assert settings.effective_blueprint_lm_studio_model() == "blueprint-model"
