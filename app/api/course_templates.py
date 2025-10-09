from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.course_template import CourseTemplateCreate, CourseTemplateRead
from app.services import course_template_service

router = APIRouter(prefix="/courses/templates", tags=["courses"])


@router.get("/", response_model=list[CourseTemplateRead])
def list_course_templates(db: Session = Depends(get_db)):
  return course_template_service.list_course_templates(db)


@router.get("/{template_id}", response_model=CourseTemplateRead)
def get_course_template(template_id: int, db: Session = Depends(get_db)):
  template = course_template_service.get_course_template(db, template_id)
  if not template:
    raise HTTPException(status_code=404, detail="Course Template not found")
  return template


@router.post("/", response_model=CourseTemplateRead)
def create_course_template(
  template: CourseTemplateCreate, db: Session = Depends(get_db)
):
  return course_template_service.create_course_template(db, template)

@router.delete("/")
def delete_course_template(template_id: int, db: Session = Depends(get_db)):
    course_template_service.delete_course_template(db, template_id)
