"""Current Role Capability Blueprint service entrypoint.

Blueprint v3/v2 remains historical structural failure evidence. Blueprint v4/v3
proved deterministic provenance but failed B4 semantic calibration. Blueprint v5/v4
removed Capability-derived prose but retained a free-form interpretation surface that
still amplified role scope. The active candidate is v6/v5: deterministic source truth
plus explicitly uncertain professional considerations and mandatory unknowns only.
"""

from jobhunter.role_blueprint_service_v6 import (
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
