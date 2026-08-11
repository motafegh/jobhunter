"""Current Role Capability Blueprint service entrypoint.

Blueprint v3/v2 remains historical structural failure evidence. Blueprint v4/v3
proved deterministic provenance but failed B4 semantic calibration. The active
candidate is v5/v4, which also bounds model-created interpretation as explicit
professional inference and excludes derived Capability prose from model input.
"""

from jobhunter.role_blueprint_service_v5 import (
    BLUEPRINT_PROMPT_VERSION,
    BLUEPRINT_SCHEMA_VERSION,
    RoleBlueprintError,
    RoleBlueprintResult,
    RoleBlueprintService,
    build_role_blueprint_service,
    format_role_blueprint,
)

__all__ = [
    "BLUEPRINT_PROMPT_VERSION",
    "BLUEPRINT_SCHEMA_VERSION",
    "RoleBlueprintError",
    "RoleBlueprintResult",
    "RoleBlueprintService",
    "build_role_blueprint_service",
    "format_role_blueprint",
]
