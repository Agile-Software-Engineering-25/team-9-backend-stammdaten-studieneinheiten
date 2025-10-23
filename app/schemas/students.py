from pydantic import BaseModel, ConfigDict
from app.schemas.course_template import CourseTemplateRead



class StudentBase(BaseModel):
  """Test Description"""

  external_id: str


class StudentsCreate(StudentBase):
  pass


class StudentsRead(StudentBase):
  model_config = ConfigDict(from_attributes=True)



class CourseReadShallow(BaseModel):
    id: int
    semester: int
    exam_type: str
    credit_points: float
    total_units: int
    template_id: int
    template: CourseTemplateRead

    model_config = ConfigDict(from_attributes=True)


class StudentsReadPlus(StudentBase):
  courses: list[CourseReadShallow]
  model_config = ConfigDict(from_attributes=True)