from pydantic import BaseModel, ConfigDict


class CourseTemplateBase(BaseModel):
  """Test Description"""

  name: str
  code: str
  elective: bool
  planned_semester: int


class CourseTemplateCreate(CourseTemplateBase):
  pass


class CourseTemplateRead(CourseTemplateBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
