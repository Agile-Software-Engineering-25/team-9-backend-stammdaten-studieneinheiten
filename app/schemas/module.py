from pydantic import BaseModel, ConfigDict
from app.schemas.module_templates import ModuleTemplateRead


class ModuleBase(BaseModel):
    semester: int
    exam_type: str
    credit_points: float
    total_units: int
    template_id: int


class ModuleCreate(ModuleBase):
    pass


class ModuleRead(ModuleBase):
    id: int
    template: ModuleTemplateRead

    model_config = ConfigDict(from_attributes=True)
