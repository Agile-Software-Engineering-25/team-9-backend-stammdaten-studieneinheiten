from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.module_template_repository import module_template_crud
from app.services.module_service import list_modules
from app.schemas.module_templates import ModuleTemplateCreate
from app.models.module_templates import ModuleTemplate
from app.models.module import Module
from app.models.course_template import CourseTemplate
from fastapi import HTTPException


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_module_template(db: Session):
  return module_template_crud.get_all(db)


def get_module_template(db: Session, template_id: int):
  return module_template_crud.get(db, template_id)


def create_module_template(db: Session, payload: ModuleTemplateCreate):
  # enforce “at least one” if desired
  if not payload.course_template_ids:
    raise HTTPException(
      status_code=400, detail="At least one course_template_id is required"
    )

  # fetch the CourseTemplate rows
  stmt = select(CourseTemplate).where(
    CourseTemplate.id.in_(payload.course_template_ids)
  )
  course_templates = list(db.scalars(stmt))

  # optional: ensure all IDs existed
  if len(course_templates) != len(set(payload.course_template_ids)):
    missing = set(payload.course_template_ids) - {
      ct.id for ct in course_templates
    }
    raise HTTPException(
      status_code=400, detail=f"Unknown course_template_ids: {sorted(missing)}"
    )

  # create and attach relationship
  obj = ModuleTemplate(name=payload.name, course_templates=course_templates)
  db.add(obj)
  db.commit()
  db.refresh(obj)
  return obj


def delete_module_template(db: Session, template_id: int):
  template = module_template_crud.get(db, template_id)
  if not template:
    raise HTTPException(
      status_code=404,
      detail=f"Module Template with the following ID does not exist: {template_id}",
    )

  # Check if no instance used
  instances = [m for m in list_modules(db) if m.template.id == template_id]
  if len(instances) != 0:
    raise HTTPException(
      status_code=400,
      detail=f"Module Template with ID {template_id} is used in {len(instances)} Module instances. Templates may not be deleted with existing instances.",
    )

  # Delete
  module_template_crud.delete(db, template_id)
