from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
  """Test Description"""

  external_id: str


class StudentsCreate(StudentBase):
  pass


class StudentsRead(StudentBase):
  model_config = ConfigDict(from_attributes=True)

class StudentsReadPlus(StudentBase):
  course_ids: list[int]
  model_config = ConfigDict(from_attributes=True)
