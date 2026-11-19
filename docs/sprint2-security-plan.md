# Sprint 2: authentication and tenant isolation

## Status
A pure role/tenant authorization policy and tests are implemented. **This is
not yet connected to API endpoints** and does not make the demo secure.

## Required before any real student data
1. Integrate managed OIDC login and verify JWT issuer, audience, signature,
   expiry and JWKS key rotation server-side.
2. Resolve tenant membership from the database, not user-controlled headers,
   path parameters or unverified JWT tenant claims.
3. Enforce policy at every school-scoped API endpoint and background job.
4. Add school_id to every tenant-owned table, including grades; use composite
   foreign keys to prevent cross-school references.
5. Enable PostgreSQL row-level security with FORCE ROW LEVEL SECURITY,
   scoped DB roles and transaction-local tenant context. Test with two tenants.
6. Introduce Alembic migrations and remove import-time create_all and
   synthetic seeding from the production startup path.
7. Audit all transcript reads, exports and issuance attempts without storing
   sensitive transcript payloads in logs.
8. Add integration tests with real PostgreSQL, negative authorization tests,
   and explicit test coverage for unauthenticated access.
9. Restrict CORS, configure TLS, rate limits and secrets management.
10. Conduct a security review before connecting ManageBac.

## CI-minutes workaround
Run locally:
```bash
cd apps/api
python -m pip install -r requirements.txt
python -m pytest -q
cd ../web
npm install && npm run build
```
Do not assume CI success while GitHub Actions minutes are exhausted.
