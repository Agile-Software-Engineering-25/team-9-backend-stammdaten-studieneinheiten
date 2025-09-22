from sqlalchemy.orm import Session
from sqlalchemy import select
from models.module_templates import ModuleTemplate
from app.models.courseofstudy_templates import CourseOfStudyTemplate
from app.repositories.courseofstudy_template_repository import (
  courseofstudy_template_crud,
)
from app.schemas.courseofstudy_template import CourseOfStudyTemplateCreate
from fastapi import HTTPException


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_courseofstudy_templates(db: Session):
  return courseofstudy_template_crud.get_all(db)


def get_courseofstudy_template(db: Session, template_id: int):
  return courseofstudy_template_crud.get(db, template_id)


def create_courseofstudy_template(
  db: Session, courseofstudy_template: CourseOfStudyTemplateCreate
):
  cos = courseofstudy_template

  # enforce "at least one"
  if not cos.module_template_ids:
    raise HTTPException(
      status_code=400, detail="At least one module_template_id is required"
    )

  # fetch the ModuleTemplate rows
  statement = select(ModuleTemplate).where(
    ModuleTemplate.id.in_(cos.module_template_ids)
  )
  module_templates = list(db.scalars(statement))

  # optional: ensure all IDs existed
  if len(module_templates) != len(set(cos.module_template_ids)):
    missing = set(cos.module_template_ids) - {mt.id for mt in module_templates}
    raise HTTPException(
      status_code=400, detail=f"Unknown module_template_ids: {sorted(missing)}"
    )

  # create and attach relationship
  obj = CourseOfStudyTemplate(name=cos.name, module_templates=module_templates)
  db.add(obj)
  db.commit()
  db.refresh(obj)
  return obj
