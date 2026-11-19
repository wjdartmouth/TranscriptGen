"""Sprint 1 synthetic-data API; not for real student records."""
import io
import os
from html import escape
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class Base(DeclarativeBase): pass
class School(Base):
    __tablename__ = "schools"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
class Student(Base):
    __tablename__ = "students"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    school_id: Mapped[str] = mapped_column(ForeignKey("schools.id"))
    name: Mapped[str] = mapped_column(String)
    grade_level: Mapped[str] = mapped_column(String)
class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"))
    course: Mapped[str] = mapped_column(String)
    academic_year: Mapped[str] = mapped_column(String)
    grade: Mapped[str] = mapped_column(String)

db_url = os.getenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
engine = create_engine(db_url, **({"connect_args":{"check_same_thread":False},"poolclass":StaticPool} if db_url.startswith("sqlite") else {}))
Base.metadata.create_all(engine)
with Session(engine) as session:
    if not session.get(School, "north"):
        session.add_all([School(id="north",name="Northbridge International School"),School(id="east",name="Eastwood Global Academy")])
        session.add_all([Student(id="alex",school_id="north",name="Alex Chen",grade_level="12"),Student(id="maya",school_id="east",name="Maya Patel",grade_level="11")])
        session.add_all([Grade(student_id="alex",course="English A: Literature HL",academic_year="2026-2027",grade="6"),Grade(student_id="alex",course="Mathematics AA SL",academic_year="2026-2027",grade="7"),Grade(student_id="maya",course="English Language",academic_year="2026-2027",grade="A"),Grade(student_id="maya",course="Biology",academic_year="2026-2027",grade="A-")])
        session.commit()

app = FastAPI(title="TranscriptGen Sprint 1")
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.get("/api/schools")
def schools():
    with Session(engine) as db:
        return [{"id":s.id,"name":s.name} for s in db.scalars(select(School)).all()]
@app.get("/api/schools/{school_id}/students")
def students(school_id: str):
    with Session(engine) as db:
        if not db.get(School,school_id): raise HTTPException(404,"School not found")
        return [{"id":s.id,"name":s.name,"grade_level":s.grade_level} for s in db.scalars(select(Student).where(Student.school_id==school_id)).all()]
def transcript_data(school_id: str,student_id: str):
    with Session(engine) as db:
        school,student=db.get(School,school_id),db.get(Student,student_id)
        if not school or not student or student.school_id != school_id: raise HTTPException(404,"Student not found in school")
        grades=db.scalars(select(Grade).where(Grade.student_id==student_id)).all()
        return {"school":school.name,"student":student.name,"grade_level":student.grade_level,"status":"SAMPLE - NOT OFFICIAL","grades":[{"course":g.course,"academic_year":g.academic_year,"grade":g.grade} for g in grades]}
@app.get("/api/schools/{school_id}/students/{student_id}/transcript")
def transcript(school_id:str,student_id:str): return transcript_data(school_id,student_id)
@app.get("/api/schools/{school_id}/students/{student_id}/transcript.pdf")
def transcript_pdf(school_id:str,student_id:str):
    data=transcript_data(school_id,student_id)
    buf=io.BytesIO()
    styles=getSampleStyleSheet()
    story=[Paragraph(escape(data["school"]),styles["Title"]),Paragraph("SAMPLE ACADEMIC TRANSCRIPT - NOT OFFICIAL",styles["Heading2"]),Spacer(1,18),Paragraph("Student: "+escape(data["student"])+" | Grade: "+escape(data["grade_level"]),styles["Normal"]),Spacer(1,18)]
    rows=[["Academic year","Course","Grade"]]+[[g["academic_year"],g["course"],g["grade"]] for g in data["grades"]]
    table=Table(rows,repeatRows=1)
    table.setStyle([("BACKGROUND",(0,0),(-1,0),colors.lightgrey),("GRID",(0,0),(-1,-1),0.4,colors.grey),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8)])
    story.append(table)
    SimpleDocTemplate(buf).build(story)
    buf.seek(0)
    return StreamingResponse(buf,media_type="application/pdf",headers={"Content-Disposition":'attachment; filename="sample-transcript.pdf"'})
