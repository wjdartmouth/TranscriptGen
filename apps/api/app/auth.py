"""Fail-closed identity dependency.

Production OIDC verification is deliberately not implemented. This dependency
cannot be satisfied by user-supplied headers or request parameters.
"""
from fastapi import HTTPException
from .security import Principal, AccessDenied, require_permission

def authenticated_principal() -> Principal:
    raise HTTPException(status_code=401, detail="Authentication provider not configured")

def authorize(principal: Principal, tenant_id: str, permission: str) -> None:
    try:
        require_permission(principal, tenant_id, permission)
    except (AccessDenied, KeyError):
        raise HTTPException(status_code=403, detail="Access denied") from None
