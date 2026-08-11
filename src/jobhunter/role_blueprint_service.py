"""Current Role Capability Blueprint service entrypoint.

Blueprint v2 remains historical in Git history. The active B4 candidate is v3/v2.
"""

from jobhunter.role_blueprint_service_v3 import (
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
