from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.module import ModuleCreate, ModuleRead
from app.services import module_service

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/", response_model=list[ModuleRead])
def list_modules(db: Session = Depends(get_db)):
  return module_service.list_modules(db)


@router.get("/{module_id}", response_model=ModuleRead)
def get_module(module_id: int, db: Session = Depends(get_db)):
  course = module_service.get_module(db, module_id)
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")
  return course


@router.post("/", response_model=ModuleRead)
def create_course(course: ModuleRead, db: Session = Depends(get_db)):
  return module_service.create_module(db, course)
