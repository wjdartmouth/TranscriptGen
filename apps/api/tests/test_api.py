import os
os.environ["DATABASE_URL"]="sqlite+pysqlite:///:memory:"
from fastapi.testclient import TestClient
from app.main import app
from app.auth import authenticated_principal
from app.security import Principal, Role

client=TestClient(app)
def login(tenant="north",role=Role.registrar):
    app.dependency_overrides[authenticated_principal]=lambda: Principal("synthetic-staff",tenant,role)
def logout():
    app.dependency_overrides.clear()

def test_health():
    assert client.get("/api/health").json()=={"status":"ok"}

def test_all_student_endpoints_require_auth():
    logout()
    for path in ["/api/schools","/api/schools/north/students","/api/schools/north/students/alex/transcript","/api/schools/north/students/alex/transcript.pdf"]:
        assert client.get(path).status_code==401

def test_schools_are_tenant_scoped():
    login()
    try:
        assert client.get("/api/schools").json()==[{"id":"north","name":"Northbridge International School"}]
    finally: logout()

def test_students():
    login()
    try:
        assert client.get("/api/schools/north/students").json()[0]["id"]=="alex"
    finally: logout()

def test_cross_school_lookup_blocked():
    login()
    try:
        assert client.get("/api/schools/east/students/maya/transcript").status_code==403
        assert client.get("/api/schools/east/students").status_code==403
        assert client.get("/api/schools/east/students/maya/transcript.pdf").status_code==403
    finally: logout()

def test_viewer_cannot_list_students():
    login(role=Role.viewer)
    try:
        assert client.get("/api/schools/north/students").status_code==403
        assert client.get("/api/schools/north/students/alex/transcript").status_code==200
    finally: logout()

def test_transcript_pdf():
    login()
    try:
        response=client.get("/api/schools/north/students/alex/transcript.pdf")
        assert response.status_code==200
        assert response.content.startswith(b"%PDF")
    finally: logout()

def test_transcript_preview():
    login()
    try:
        data=client.get("/api/schools/north/students/alex/transcript").json()
        assert data["status"]=="SAMPLE - NOT OFFICIAL"
        assert len(data["grades"])==2
    finally: logout()
