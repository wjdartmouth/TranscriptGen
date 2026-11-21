"""SQLite unit tests for membership policy; PostgreSQL RLS is still untested."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.main import Base, School
from app.memberships import SchoolMembership, resolve_membership
from app.security import Role

def test_membership_lookup_is_scoped_and_fail_closed():
    engine = create_engine("sqlite+pysqlite:///:memory:", poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add_all([School(id="school-a", name="Synthetic A"),
                    School(id="school-b", name="Synthetic B")])
        db.flush()
        db.add_all([
            SchoolMembership(subject="oidc|synthetic-1", school_id="school-a", role="registrar", active=True),
            SchoolMembership(subject="oidc|synthetic-1", school_id="school-b", role="viewer", active=False),
            SchoolMembership(subject="oidc|synthetic-2", school_id="school-b", role="invalid-role", active=True),
        ])
        db.commit()
        p = resolve_membership(db, "oidc|synthetic-1", "school-a")
        assert p is not None and p.role is Role.registrar and p.tenant_id == "school-a"
        assert resolve_membership(db, "oidc|synthetic-1", "school-b") is None
        assert resolve_membership(db, "oidc|synthetic-2", "school-b") is None
        assert resolve_membership(db, "unknown", "school-a") is None
        assert resolve_membership(db, "", "school-a") is None
        assert resolve_membership(db, "oidc|synthetic-1", "") is None

def test_same_subject_can_have_distinct_roles_per_school():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add_all([School(id="a", name="A"), School(id="b", name="B")])
        db.flush()
        db.add_all([SchoolMembership(subject="subject", school_id="a", role="registrar"),
                    SchoolMembership(subject="subject", school_id="b", role="viewer")])
        db.commit()
        assert resolve_membership(db, "subject", "a").role is Role.registrar
        assert resolve_membership(db, "subject", "b").role is Role.viewer
