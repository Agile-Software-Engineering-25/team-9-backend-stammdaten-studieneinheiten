from pydantic import BaseModel, ConfigDict
from app.schemas.course_template import CourseTemplateRead


class CourseBase(BaseModel):
  semester: int
  exam_type: str
  credit_points: float
  total_units: int
  template_id: int
  teaching_instructor: int



class CourseCreate(CourseBase):
  attending_students: list[int] | None


class CourseRead(CourseBase):
  id: int
  template: CourseTemplateRead

  model_config = ConfigDict(from_attributes=True)
