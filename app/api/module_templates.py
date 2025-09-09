from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.module_templates import ModuleTemplateCreate, ModuleTemplateRead
from app.services import module_template_service

router = APIRouter(prefix="/modules/templates", tags=["modules"])


@router.get("/", response_model=list[ModuleTemplateRead])
def list_module_templates(db: Session = Depends(get_db)):
  return module_template_service.list_module_template(db)


@router.get("/{mod_temp_id}", response_model=ModuleTemplateRead)
def get_module_templates(mod_temp_id: int, db: Session = Depends(get_db)):
  module_template = module_template_service.get_module_template(db, mod_temp_id)
  if not module_template:
    raise HTTPException(status_code=404, detail="Module Template not found")
  return module_template


@router.post("/", response_model=ModuleTemplateRead)
def create_module_templates(module_template: ModuleTemplateCreate, db: Session = Depends(get_db)):
  return module_template_service.create_module_template(db, module_template)
