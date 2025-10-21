from sqlalchemy.orm import Session
from app.repositories.teachers_repository import teachers_crud
from app.schemas.teachers import TeacherCreate


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_teachers(db: Session):
  return teachers_crud.get_all(db)


def get_teachers(db: Session, teacher_id: str):
  return teachers_crud.get(db, teacher_id)


def create_teachers(db: Session, teacher: TeacherCreate):
  return teachers_crud.create(db, teacher)
