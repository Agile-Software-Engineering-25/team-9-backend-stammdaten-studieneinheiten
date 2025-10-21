from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.students import StudentsCreate, StudentsRead
from app.services import students_service

router = APIRouter(prefix="/external_connections/students", tags=["external_connections"])


@router.get("/", response_model=list[StudentsRead])
def list_students(db: Session = Depends(get_db)):
  return students_service.list_students(db)


@router.get("/{student_id}", response_model=StudentsRead)
def get_student(student_id: str, db: Session = Depends(get_db)):
  student = students_service.get_students(db, student_id)
  if not student:
    raise HTTPException(status_code=404, detail="Student not found")
  return student


@router.post("/", response_model=StudentsRead)
def create_student(
  student: StudentsCreate, db: Session = Depends(get_db)
):
  return students_service.create_students(db, student)
