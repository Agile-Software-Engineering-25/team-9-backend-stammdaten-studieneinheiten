from pydantic import BaseModel, ConfigDict
from app.schemas.course import CourseRead


class StudentBase(BaseModel):
  student_id: int


class StudentCreate(StudentBase):
  # many-to-many, so accept multiple; if you truly want “at least one”, validate in service
  courses_ids: list[int]


class StudentsRead(StudentBase):
  id: int
  # reflect the relationship name and cardinality
  courses: list[CourseRead]

  model_config = ConfigDict(from_attributes=True)
