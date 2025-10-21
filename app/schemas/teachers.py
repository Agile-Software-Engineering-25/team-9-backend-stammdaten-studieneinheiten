from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
  """Test Description"""

  external_id: int


class TeacherCreate(TeacherBase):
  pass


class TeacherRead(TeacherBase):
  model_config = ConfigDict(from_attributes=True)
