from pydantic import BaseModel, ConfigDict


class CourseofStudyBase(BaseModel):
  name: str


class CourseofStudyCreate(CourseofStudyBase):
  pass


class CourseofStudyRead(CourseofStudyBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
