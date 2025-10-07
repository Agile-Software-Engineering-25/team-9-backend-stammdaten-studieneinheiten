from app.models.module import Module
from app.schemas.module import ModuleTemplateRead
from app.repositories.base import CRUDBase

module_crud = CRUDBase[Module, ModuleTemplateRead](Module)
