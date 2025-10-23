from sqlalchemy.orm import Session
from app.repositories.course_of_study_repository import course_of_study_crud
from app.schemas.coursesofstudy import CourseofStudyCreate


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course_of_study(db: Session):
  return course_of_study_crud.get_all(db)


def get_course_of_study(db: Session, template_id: int):
  return course_of_study_crud.get(db, template_id)


def create_course_of_study(db: Session, course: CourseofStudyCreate):
  return course_of_study_crud.create(db, course)
