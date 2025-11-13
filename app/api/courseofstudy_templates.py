from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.courseofstudy_template import (
  CourseOfStudyTemplateRead,
  CourseOfStudyTemplateCreate,
)
from app.services import courseofstudy_template_service

router = APIRouter(prefix="/courseofstudies/templates", tags=["coursofstudies"])


@router.get("/", response_model=list[CourseOfStudyTemplateRead])
def list_courseofstudy_templates(db: Session = Depends(get_db)):
  return courseofstudy_template_service.list_courseofstudy_templates(db)


@router.get("/{cos_temp_id}", response_model=CourseOfStudyTemplateRead)
def get_courseofstudy_templates(
  cos_temp_id: int, db: Session = Depends(get_db)
):
  courseofstudy_template = (
    courseofstudy_template_service.get_courseofstudy_template(db, cos_temp_id)
  )
  if not courseofstudy_template:
    raise HTTPException(
      status_code=404, detail="CourseOfStudy Template not found"
    )
  return courseofstudy_template


@router.post("/", response_model=CourseOfStudyTemplateRead)
def create_courseofstudy_templates(
  courseofstudy_template: CourseOfStudyTemplateCreate,
  db: Session = Depends(get_db),
):
  return courseofstudy_template_service.create_courseofstudy_template(
    db, courseofstudy_template
  )


@router.delete("/{cos_temp_id}")
def delete_courseofstudy_template(
  cos_temp_id: int, db: Session = Depends(get_db)
):
  courseofstudy_template_service.delete_courseofstudy_template(db, cos_temp_id)
