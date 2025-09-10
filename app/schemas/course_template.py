from pydantic import BaseModel, ConfigDict


class CourseTemplateBase(BaseModel):
  """Test Description"""

  name: str
  elective: bool


class CourseTemplateCreate(CourseTemplateBase):
  pass


class CourseTemplateRead(CourseTemplateBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
