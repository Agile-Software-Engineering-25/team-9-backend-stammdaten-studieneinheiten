from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
  """Test Description"""

  external_id: str


class TeacherCreate(TeacherBase):
  pass


class TeacherRead(TeacherBase):
  model_config = ConfigDict(from_attributes=True)

class TeacherReadPlus(TeacherBase):
  course_ids: list[int]
  model_config = ConfigDict(from_attributes=True)
