from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.teachers import TeacherCreate, TeacherRead, TeacherReadPlus
from app.services import teachers_service

router = APIRouter(prefix="/external_connections/teachers", tags=["external_connections"])


@router.get("/", response_model=list[TeacherRead])
def list_teachers(db: Session = Depends(get_db)):
  return teachers_service.list_teachers(db)


@router.get("/{teacher_external_id}", response_model=TeacherReadPlus)
def get_teacher(teacher_external_id: str, db: Session = Depends(get_db)):
  teacher = teachers_service.get_teachers(db, teacher_external_id)
  return teacher


@router.post("/", response_model=TeacherCreate)
def create_teacher(
  teacher: TeacherCreate, db: Session = Depends(get_db)
):
  return teachers_service.create_teachers(db, teacher)

@router.get("/{teacher_external_id}/courses", response_model=TeacherReadPlus)
def get_course(teacher_external_id: str, db: Session = Depends(get_db)):
  return teachers_service.get_teacher_courses(db, teacher_external_id)