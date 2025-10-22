from sqlalchemy.orm import Session
from app.repositories.module_repository import module_crud
from app.schemas.module import ModuleCreate
from fastapi import HTTPException
from sqlalchemy import select
from app.models.course import Course
from app.models.module import Module
from app.models.module_templates import ModuleTemplate





# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_modules(db: Session):
    return module_crud.get_all(db)


def get_module(db: Session, module_id: int):
    return module_crud.get(db, module_id)


def create_module(db: Session, payload: ModuleCreate):
    # enforce “at least one” if desired
  if not payload.course_ids:
    raise HTTPException(
      status_code=400, detail="At least one course_id is required"
    )

  # fetch the CourseTemplate rows
  stmt = select(Course).where(
    Course.id.in_(payload.course_ids)
  )
  courses = list(db.scalars(stmt))

  # optional: ensure all IDs existed
  if len(courses) != len(set(payload.course_ids)):
    missing = set(payload.course_ids) - {
      ct.id for ct in courses
    }
    raise HTTPException(
      status_code=400, detail=f"Unknown course_template_ids: {sorted(missing)}"
    )
  
#check module template________________________________________________________________

  if not payload.template_id:
    raise HTTPException(
      status_code=400, detail="A template is required"
    )

  # fetch the CourseTemplate rows
  stmt = select(ModuleTemplate).where(
    ModuleTemplate.id==payload.template_id
  )
  template = db.scalars(stmt).one()

  # optional: ensure all IDs existed
  if not template:
    raise HTTPException(
      status_code=400, detail=f"Bad template: {payload.template_id}"
    )

  # create and attach relationship
  obj = Module(template=template, courses=courses)
  db.add(obj)
  db.commit()
  db.refresh(obj)
  return obj
