import pytest
from app.security import Principal, Role, AccessDenied, require_permission

@pytest.mark.parametrize("role,permission,allowed",[
    (Role.registrar,"student:read",True),
    (Role.registrar,"transcript:issue",True),
    (Role.counselor,"transcript:issue",False),
    (Role.counselor,"transcript:read",True),
    (Role.viewer,"student:read",False),
    (Role.viewer,"transcript:read",True),
    (Role.registrar,"unknown:action",False),
])
def test_role_policy(role,permission,allowed):
    principal=Principal("staff-1","north",role)
    if allowed:
        require_permission(principal,"north",permission)
    else:
        with pytest.raises(AccessDenied):
            require_permission(principal,"north",permission)

@pytest.mark.parametrize("role",list(Role))
def test_cross_tenant_denied(role):
    with pytest.raises(AccessDenied):
        require_permission(Principal("staff-1","north",role),"east","transcript:read")

def test_missing_identity_denied():
    with pytest.raises(AccessDenied):
        require_permission(Principal("","north",Role.registrar),"north","transcript:read")
