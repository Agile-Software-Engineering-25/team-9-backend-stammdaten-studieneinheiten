from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.students_repository import student_crud
from app.schemas.students import StudentsCreate
from app.models.students import Students
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_students(db: Session):
  return student_crud.get_all(db)


def get_students(db: Session, student_external_id: str):
    stmt = select(Students).where(Students.external_id == student_external_id)
    try:
        student = db.scalars(stmt).one()
        return student
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student not found")


def create_students(db: Session, student: StudentsCreate):
  return student_crud.create(db, student)
