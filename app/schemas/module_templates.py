from pydantic import BaseModel, ConfigDict
from app.schemas.course_template import CourseTemplateRead


class ModuleTemplateBase(BaseModel):
  name: str


class ModuleTemplateCreate(ModuleTemplateBase):
  # many-to-many, so accept multiple; if you truly want “at least one”, validate in service
  course_template_ids: list[int]


class ModuleTemplateRead(ModuleTemplateBase):
  id: int
  # reflect the relationship name and cardinality
  course_templates: list[CourseTemplateRead]

  model_config = ConfigDict(from_attributes=True)
