from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
  """Test Description"""

  external_id: int


class StudentsCreate(StudentBase):
  pass


class StudentsRead(StudentBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
