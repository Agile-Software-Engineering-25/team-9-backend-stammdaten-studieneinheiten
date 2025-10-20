from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.course_template import CourseTemplateRead

class CourseBase(BaseModel):
    semester: int
    exam_type: str
    credit_points: float
    total_units: int
    template_id: int
    teacher_id: int

class CourseCreate(CourseBase):
    student_ids: list[int]

class CourseRead(CourseBase):
    id: int
    template: CourseTemplateRead
    students: list[int]  # desired output: list of external_id ints

    model_config = ConfigDict(from_attributes=True)

    @field_validator("students", mode="before")
    @classmethod
    def students_to_ids(cls, v):
        # v will be whatever the ORM provides, typically list[Students]
        try:
            return [s.external_id for s in v]
        except TypeError:
            # if it's already a list of ints or None, just return as-is
            return v
