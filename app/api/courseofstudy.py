from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.coursesofstudy import (
  CourseofStudyCreate,
  CourseofStudyRead
)
from app.services import course_of_study_service

router = APIRouter(prefix="/courseofstudies", tags=["coursofstudies"])



@router.get("/", response_model=list[CourseofStudyRead])
def list_courses_of_study(db: Session = Depends(get_db)):
  return course_of_study_service.list_course_of_study(db)


@router.get("/{courseofstudy_id}", response_model=CourseofStudyRead)
def get_course_of_study(courseofstudy_id: int, db: Session = Depends(get_db)):
  courseofstudy = course_of_study_service.get_course_of_study(db, courseofstudy_id)
  if not courseofstudy:
    raise HTTPException(status_code=404, detail="Course Of Study not found")
  return courseofstudy


@router.post("/", response_model=CourseofStudyRead)
def create_course_of_study(
  template:   CourseofStudyCreate,
 db: Session = Depends(get_db)
):
  return course_of_study_service.create_course_of_study(db, template)