from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.module import (
  ModuleCreate,
  ModuleRead,
)
from app.services import module_service

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", response_model=list[ModuleRead])
def list_module_templates(db: Session = Depends(get_db)):
  return module_service.list_modules(db)


@router.get("/{mod_id}", response_model=ModuleRead)
def get_module(mod_id: int, db: Session = Depends(get_db)):
  module = module_service.get_module(db, mod_id)
  if not module:
    raise HTTPException(status_code=404, detail="Module Template not found")
  return module


@router.post("/", response_model=ModuleRead)
def create_module_templates(
  module: ModuleCreate, db: Session = Depends(get_db)
):
  return module_service.create_module(db, module)
