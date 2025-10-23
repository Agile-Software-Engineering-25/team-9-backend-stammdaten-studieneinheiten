from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.students import StudentsCreate, StudentsRead, StudentsReadPlus, StudentsReadPlus2
from app.services import students_service

router = APIRouter(prefix="/external_connections/students", tags=["external_connections"])


@router.get("/", response_model=list[StudentsRead])
def list_students(db: Session = Depends(get_db)):
  return students_service.list_students(db)


@router.get("/{student_external_id}", response_model=StudentsReadPlus)
def get_student(student_external_id: str, db: Session = Depends(get_db)):
  student = students_service.get_students(db, student_external_id)
  return student


@router.post("/", response_model=StudentsRead)
def create_student(
  student: StudentsCreate, db: Session = Depends(get_db)
):
  return students_service.create_students(db, student)

@router.get("/courses/{student_external_id}", response_model=StudentsReadPlus2)
def get_course(student_external_id: str, db: Session = Depends(get_db)):
  return students_service.get_student_courses(db, student_external_id)