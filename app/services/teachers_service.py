from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.teachers_repository import teachers_crud
from app.schemas.teachers import TeacherCreate
from app.models.teachers import Teachers
from app.schemas.teachers import TeacherReadPlus
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_teachers(db: Session):
  return teachers_crud.get_all(db)


def get_teachers(db: Session, teacher_external_id: str):
  stmt = select(Teachers).where(Teachers.external_id == teacher_external_id)
  try:
      teacher = db.scalars(stmt).one()
      course_ids = [c.id for c in teacher.courses]
      
      return TeacherReadPlus(
        **teacher.__dict__,  # include all base teacher fields
        course_ids=course_ids
      )
  except NoResultFound:
      raise HTTPException(status_code=404, detail="Teacher not found")


def create_teachers(db: Session, teacher: TeacherCreate):
  return teachers_crud.create(db, teacher)

def get_teacher_courses(db: Session, teacher_id: str):
    """
    Gibt alle Kursinstanzen eines Teachers anhand der Teacher-ID zurück.
    """
    stmt = select(Teachers).where(Teachers.external_id == teacher_id)
    try:
        teacher = db.scalars(stmt).one()
        # Kurse direkt aus Relationship ziehen
        return TeacherReadPlus(
            **teacher.__dict__,
            courses=teacher.courses
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Teacher not found")

