"""Current Role Capability Blueprint service entrypoint.

Blueprint v3/v2 remains historical negative B4 evidence. The active B4 candidate
is v4/v3, which keeps semantic interpretation in the model while attaching
Capability/P1.6 provenance deterministically in JobHunter.
"""

from jobhunter.role_blueprint_service_v4 import (
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
