"""Tenant authorization primitives for Sprint 2.

No demo credentials are provided. Production deployment must use an OIDC
identity provider; this module is a pure policy layer, not authentication.
"""
from dataclasses import dataclass
from enum import Enum

class Role(str, Enum):
    registrar = "registrar"
    counselor = "counselor"
    viewer = "viewer"

@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str
    role: Role

class AccessDenied(PermissionError):
    pass

PERMISSIONS = {
    Role.registrar: frozenset({"student:read", "transcript:read", "transcript:issue"}),
    Role.counselor: frozenset({"student:read", "transcript:read"}),
    Role.viewer: frozenset({"transcript:read"}),
}

def require_permission(principal: Principal, tenant_id: str, permission: str) -> None:
    """Deny unknown actions and all cross-tenant access."""
    if not principal.user_id or not principal.tenant_id:
        raise AccessDenied("Unauthenticated principal")
    if principal.tenant_id != tenant_id:
        raise AccessDenied("Tenant access denied")
    if permission not in PERMISSIONS[principal.role]:
        raise AccessDenied("Insufficient role permissions")
