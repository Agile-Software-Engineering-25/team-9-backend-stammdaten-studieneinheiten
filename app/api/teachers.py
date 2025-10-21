from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.teachers import TeacherCreate, TeacherRead
from app.services import teachers_service

router = APIRouter(prefix="/external_connections/teachers", tags=["external_connections"])


@router.get("/", response_model=list[TeacherCreate])
def list_teachers(db: Session = Depends(get_db)):
  return teachers_service.list_teachers(db)


@router.get("/{teacher_id}", response_model=TeacherCreate)
def get_teacher(teacher_id: str, db: Session = Depends(get_db)):
  teacher = teachers_service.get_teachers(db, teacher_id)
  if not teacher:
    raise HTTPException(status_code=404, detail="Teacher not found")
  return teacher


@router.post("/", response_model=TeacherCreate)
def create_teacher(
  teacher: TeacherCreate, db: Session = Depends(get_db)
):
  return teachers_service.create_teachers(db, teacher)
