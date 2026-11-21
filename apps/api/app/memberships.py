"""Database-backed school membership lookup (Sprint 2 building block).

The caller MUST supply a subject from a cryptographically verified identity
provider token. Never accept subject or school from request headers directly.
This module does not authenticate users and is not yet wired into the API.
"""
from sqlalchemy import ForeignKey, String, UniqueConstraint, select
from sqlalchemy.orm import Mapped, Session, mapped_column
from .main import Base
from .security import Principal, Role

class SchoolMembership(Base):
    __tablename__ = "school_memberships"
    __table_args__ = (UniqueConstraint("subject", "school_id", name="uq_membership_subject_school"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    school_id: Mapped[str] = mapped_column(ForeignKey("schools.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

def resolve_membership(session: Session, verified_subject: str, school_id: str) -> Principal | None:
    """Return active membership only; fail closed on unknown roles or missing data."""
    if not verified_subject or not school_id:
        return None
    membership = session.scalar(
        select(SchoolMembership).where(
            SchoolMembership.subject == verified_subject,
            SchoolMembership.school_id == school_id,
            SchoolMembership.active.is_(True),
        )
    )
    if membership is None:
        return None
    try:
        role = Role(membership.role)
    except ValueError:
        return None
    return Principal(user_id=verified_subject, tenant_id=school_id, role=role)
