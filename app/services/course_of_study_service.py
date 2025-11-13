from sqlalchemy.orm import Session
from datetime import date, datetime
from app.repositories.course_of_study_repository import course_of_study_crud
from app.schemas.coursesofstudy import CourseofStudyCreate
from app.models.module import Module
from app.models.courseofstudy_templates import CourseOfStudyTemplate
from app.models.coursesofstudy import CoursesOfStudy
from fastapi import HTTPException
from sqlalchemy import select


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course_of_study(db: Session):
  return course_of_study_crud.get_all(db)


def get_course_of_study(db: Session, template_id: int):
  return course_of_study_crud.get(db, template_id)


def delete_course_of_study(db: Session, cos_id: int):
  today_start = datetime.now().replace(
    hour=0, minute=0, second=0, microsecond=0
  )
  today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=0)

  cos = (
    db.query(CoursesOfStudy)
    .filter(
      CoursesOfStudy.id == cos_id,
      CoursesOfStudy.startDate <= today_end,
      CoursesOfStudy.endDate >= today_start,
    )
    .first()
  )

  if cos:
    raise HTTPException(
      status_code=409, detail="Course of Study is currently running"
    )
  return course_of_study_crud.delete(db, cos_id)


def create_course_of_study(db: Session, payload: CourseofStudyCreate):
  if hasattr(payload, "model_dump"):
    data = payload.model_dump(exclude={"module_ids"}, exclude_unset=True)
  else:
    data = payload.dict(
      exclude={"module_ids"}, exclude_unset=True
    )  # Pydantic v1 fallback

  if not payload.module_ids:
    raise HTTPException(
      status_code=400, detail="At least one module_id is required"
    )

  # fetch the CourseTemplate rows
  stmt = select(Module).where(Module.id.in_(payload.module_ids))
  modules = list(db.scalars(stmt))

  # optional: ensure all IDs existed
  if len(modules) != len(set(payload.module_ids)):
    missing = set(payload.module_ids) - {ct.id for ct in modules}
    raise HTTPException(
      status_code=400, detail=f"Unknown module ids: {sorted(missing)}"
    )

  # check module template________________________________________________________________

  if not payload.template_id:
    raise HTTPException(status_code=400, detail="A template is required")

  # fetch the CourseTemplate rows
  stmt = select(CourseOfStudyTemplate).where(
    CourseOfStudyTemplate.id == payload.template_id
  )
  template = db.scalars(stmt).one()

  # optional: ensure all IDs existed
  if not template:
    raise HTTPException(
      status_code=400, detail=f"Bad template: {payload.template_id}"
    )
  print(template)

  student_ids = data.pop("module_ids", None)
  # create and attach relationship
  obj = CoursesOfStudy(**data, modules=modules, template=template)
  db.add(obj)
  db.commit()
  db.refresh(obj)
  return obj
