"""Current Capability Intelligence service entrypoint.

The rejected v6 implementation is preserved in ``capability_service_v6`` for historical
reproducibility. The active B3 candidate is v7.
"""

from jobhunter.capability_service_v7 import (
    CAPABILITY_PROMPT_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    CapabilityIntelligenceError,
    CapabilityIntelligenceResult,
    CapabilityIntelligenceService,
    build_capability_intelligence_service,
    format_capability_intelligence,
)

__all__ = [
    "CAPABILITY_PROMPT_VERSION",
    "CAPABILITY_SCHEMA_VERSION",
    "CapabilityIntelligenceError",
    "CapabilityIntelligenceResult",
    "CapabilityIntelligenceService",
    "build_capability_intelligence_service",
    "format_capability_intelligence",
]
