from pydantic import BaseModel, ConfigDict
from app.schemas.students import CourseReadShallow

class TeacherBase(BaseModel):
  """Test Description"""

  external_id: str


class TeacherCreate(TeacherBase):
  pass


class TeacherRead(TeacherBase):
  model_config = ConfigDict(from_attributes=True)

class TeacherReadPlus(TeacherBase):
    courses: list[CourseReadShallow]
    model_config = ConfigDict(from_attributes=True)