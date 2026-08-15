import jobhunter.capability_service as current_capability
import jobhunter.capability_service_v7 as capability_v7
import jobhunter.capability_service_v9 as capability_v9
import jobhunter.role_blueprint_service_v6 as blueprint_v6


def test_current_capability_facade_is_promoted_to_v9() -> None:
    assert current_capability.CAPABILITY_PROMPT_VERSION == "job-capability-intelligence-v9"
    assert current_capability.CAPABILITY_SCHEMA_VERSION == "job-capability-intelligence-v5"
    assert current_capability.CAPABILITY_PROMPT_VERSION == capability_v9.CAPABILITY_PROMPT_VERSION
    assert current_capability.CAPABILITY_SCHEMA_VERSION == capability_v9.CAPABILITY_SCHEMA_VERSION
    assert issubclass(
        current_capability.CapabilityIntelligenceService,
        capability_v9.CapabilityIntelligenceServiceV9,
    )
    assert current_capability.format_capability_intelligence is capability_v9.format_capability_v9


def test_deferred_blueprint_v6_remains_pinned_to_historical_capability_v7() -> None:
    assert blueprint_v6.CAPABILITY_PROMPT_VERSION == capability_v7.CAPABILITY_PROMPT_VERSION
    assert blueprint_v6.CAPABILITY_SCHEMA_VERSION == capability_v7.CAPABILITY_SCHEMA_VERSION
    assert blueprint_v6.CAPABILITY_PROMPT_VERSION != current_capability.CAPABILITY_PROMPT_VERSION
    assert blueprint_v6.CAPABILITY_SCHEMA_VERSION != current_capability.CAPABILITY_SCHEMA_VERSION
