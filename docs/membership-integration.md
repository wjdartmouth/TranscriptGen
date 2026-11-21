# School membership resolver — integration notes

The `SchoolMembership` model and `resolve_membership` function are an
incremental Sprint 2 building block, **not active authentication**.

The authenticated dependency in `auth.py` intentionally continues returning
HTTP 401 for all requests. Do not wire the membership resolver directly to
untrusted headers, query parameters, or unverified JWT claims.

## Safe integration sequence

1. Configure an OIDC provider and validate token signature against a trusted
   JWKS, algorithm allowlist, issuer, audience, expiration and key rotation.
2. Derive `verified_subject` from the verified token, never from client input.
3. Resolve active school memberships in the database for the requested tenant.
4. Apply the role policy and fail closed on missing/invalid memberships.
5. Introduce Alembic migrations before enabling the table in deployments.
   Importing this model alone does not create the table in an existing DB.
6. Apply PostgreSQL FORCE ROW LEVEL SECURITY to tenant-owned records, use
   a restricted DB role and transaction-scoped tenant context.
7. Test all combinations with real PostgreSQL and multiple schools.

All identifiers in tests are synthetic. This code is not production ready.
