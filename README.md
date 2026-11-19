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
