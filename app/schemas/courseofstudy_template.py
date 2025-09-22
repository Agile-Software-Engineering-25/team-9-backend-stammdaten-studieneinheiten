from pydantic import BaseModel, ConfigDict
from app.schemas.module_templates import ModuleTemplateRead


class CourseOfStudyTemplateBase(BaseModel):
  name: str
  degree_type: str
  planned_semester: int


class CourseOfStudyTemplateCreate(CourseOfStudyTemplateBase):
  # many-to-many, so accept multiple; if you truly want “at least one”, validate in service
  module_template_ids: list[int]


class CourseOfStudyTemplateRead(CourseOfStudyTemplateBase):
  id: int
  module_templates: list[ModuleTemplateRead]

  model_config = ConfigDict(from_attributes=True)
