from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  students_in_course
)


class Students(Base, BaseIdMixin):
  __tablename__ = "Students"

  student_id = Column(Integer, nullable=False)

  attended_courses = relationship(
    "Courses",
    secondary=students_in_course,
    back_populates="attending_students",
  )
