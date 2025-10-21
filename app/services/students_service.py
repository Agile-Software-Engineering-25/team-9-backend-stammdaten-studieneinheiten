from sqlalchemy.orm import Session
from app.repositories.students_repository import student_crud
from app.schemas.students import StudentsCreate


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_students(db: Session):
  return student_crud.get_all(db)


def get_students(db: Session, student_id: str):
  return student_crud.get(db, student_id)


def create_students(db: Session, student: StudentsCreate):
  return student_crud.create(db, student)
