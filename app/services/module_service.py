from sqlalchemy.orm import Session
from app.repositories.module_repository import module_crud
from app.schemas.module import ModuleCreate


# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course(db: Session):
    return module_crud.get_all(db)


def get_course(db: Session, template_id: int):
    return module_crud.get(db, template_id)


def create_course(db: Session, module: ModuleCreate):
    return module_crud.create(db, module)
