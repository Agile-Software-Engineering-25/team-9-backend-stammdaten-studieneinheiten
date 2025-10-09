from sqlalchemy.orm import Session
from app.repositories.course_template_repository import course_template_crud
from app.schemas.course_template import CourseTemplateCreate


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
    return course_template_crud.delete(db, template_id)
