from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  students_in_course
)


class Course(Base, BaseIdMixin):
  __tablename__ = "Courses"

  semester = Column(Integer, nullable=False)
  exam_type = Column(String, nullable=False)
  credit_points = Column(Float, nullable=False)
  total_units = Column(Integer, nullable=False)
  teaching_instructor = Column(Integer, nullable=True) #nullable should remain true for elective and such

  template_id = Column(
    Integer, ForeignKey("CourseTemplates.id"), nullable=False
  )
  template = relationship("CourseTemplate", backref="Courses")

  attending_students = relationship(
    "Students",
    secondary=students_in_course,
    back_populates="attended_courses",
  )

