from pydantic import BaseModel, ConfigDict


class ModuleTemplateBase(BaseModel):
  name: str

class ModuleTemplateCreate(ModuleTemplateBase):
  pass


class ModuleTemplateRead(ModuleTemplateBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
