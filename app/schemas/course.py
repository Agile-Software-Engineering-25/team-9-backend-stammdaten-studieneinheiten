from pydantic import BaseModel, ConfigDict, field_serializer
from app.schemas.course_template import CourseTemplateRead
from app.schemas.teachers import TeacherRead
from app.schemas.students import StudentsRead
from typing import Optional


class CourseBase(BaseModel):
    semester: int
    exam_type: str
    credit_points: float
    total_units: int
    template_id: int

class CourseCreate(CourseBase):
    student_ids: Optional[list[str]] = None
    teacher_ids: Optional[list[str]] = None

class CourseRead(CourseBase):
    id: int
    template: CourseTemplateRead
    students: list[StudentsRead]  # desired output: list of external_id ints
    teachers: list[TeacherRead]

    model_config = ConfigDict(from_attributes=True)
