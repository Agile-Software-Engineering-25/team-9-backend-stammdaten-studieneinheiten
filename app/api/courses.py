from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.course import CourseCreate, CourseRead
from app.services import course_service

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=list[CourseRead])
def list_courses(db: Session = Depends(get_db)):
  return course_service.list_course(db)


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
  course = course_service.get_course(db, course_id)
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")
  return course


@router.post("/", response_model=CourseRead)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
  return course_service.create_course(db, course)


@router.post("/update/{course_id}", response_model=CourseRead)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
  return course_service.create_course(db, course)
