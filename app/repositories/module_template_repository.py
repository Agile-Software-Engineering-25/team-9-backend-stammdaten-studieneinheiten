from app.models.module_templates import ModuleTemplate
from app.schemas.module_templates import ModuleTemplateCreate
from app.repositories.base import CRUDBase

module_template_crud = CRUDBase[ModuleTemplate, ModuleTemplateCreate](
  ModuleTemplate
)
