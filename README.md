# TranscriptGen

Multi-school transcript generator — Sprint 1 prototype using **synthetic student records only**.

## Stack
React + TypeScript SPA, FastAPI, SQLAlchemy, PostgreSQL, Docker Compose, ReportLab PDF export, pytest.

## Run
```bash
docker compose up --build
```
Web: http://localhost:5173 · API: http://localhost:8000/docs

## Security
**NOT PRODUCTION READY.** No authentication or tenant authorization. Never load real student data, credentials, or sign official transcripts until security work is complete.

## Tests
```bash
cd apps/api && pip install -r requirements.txt && pytest -q
```

## Sprint 2 security gate (2026-11-20)

All student and transcript endpoints now **deny requests by default (HTTP 401)** until a real identity provider is configured. The demo SPA cannot retrieve students or PDFs yet; this is intentional to avoid shipping an unsecured student-record API. The health endpoint remains public. The authorization dependency may be overridden **only in automated tests** with synthetic principals. Do not implement a production shortcut via arbitrary request headers.

The next increment is validated OIDC identity, database-backed school memberships, and PostgreSQL row-level security. Tests are committed but have **not been executed in this run** because GitHub Actions minutes are exhausted and no local runtime verification was performed.
