from sqlalchemy.orm import Session
from app.models.module_template import ModuleTemplate
from app.schemas.module_template import ModuleTemplateCreate
from app.repositories.base import CRUDBase

module_template_crud = CRUDBase[ModuleTemplate, ModuleTemplateCreate](
  ModuleTemplate
)
