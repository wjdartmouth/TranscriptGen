import os
os.environ["DATABASE_URL"]="sqlite+pysqlite:///:memory:"
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get("/api/health").json()=={"status":"ok"}
def test_schools(): assert len(client.get("/api/schools").json())==2
def test_students(): assert client.get("/api/schools/north/students").json()[0]["id"]=="alex"
def test_cross_school_lookup_blocked(): assert client.get("/api/schools/east/students/alex/transcript").status_code==404
def test_transcript_pdf():
    response=client.get("/api/schools/north/students/alex/transcript.pdf")
    assert response.status_code==200
    assert response.content.startswith(b"%PDF")
def test_transcript_preview():
    data=client.get("/api/schools/north/students/alex/transcript").json()
    assert data["status"]=="SAMPLE - NOT OFFICIAL"
    assert len(data["grades"])==2
