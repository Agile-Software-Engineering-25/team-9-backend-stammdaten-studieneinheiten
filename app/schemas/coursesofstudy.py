from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.courseofstudy_template import CourseOfStudyTemplateRead
from app.schemas.module import ModuleRead


class CourseofStudyBase(BaseModel):
  name: str
  startDate: datetime
  endDate: datetime
  cohort: str

class CourseofStudyCreate(CourseofStudyBase):
  module_ids: list[int]
  template_id: int


class CourseofStudyRead(CourseofStudyBase):
  id: int

  modules: list[ModuleRead]
  template: CourseOfStudyTemplateRead

  model_config = ConfigDict(from_attributes=True)
