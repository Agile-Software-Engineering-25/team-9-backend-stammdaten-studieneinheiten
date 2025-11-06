from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.repositories.course_template_repository import course_template_crud
from app.schemas.course_template import CourseTemplateCreate
from app.services.course_service import list_course


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course_templates(db: Session):
  return course_template_crud.get_all(db)


def get_course_template(db: Session, template_id: int):
  return course_template_crud.get(db, template_id)


def create_course_template(db: Session, course: CourseTemplateCreate):
  return course_template_crud.create(db, course)


def delete_course_template(db: Session, template_id: int):
  instances = [m for m in list_course(db) if m.template.id == template_id]
  if instances:
    raise HTTPException(
      status_code=404,
      detail="There is at least one course instance using the template",
    )
  return course_template_crud.delete(db, template_id)
