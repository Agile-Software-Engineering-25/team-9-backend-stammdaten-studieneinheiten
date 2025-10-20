from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin


class Course(Base, BaseIdMixin):
  __tablename__ = "Courses"

  semester = Column(Integer, nullable=False)
  exam_type = Column(String, nullable=False)
  credit_points = Column(Float, nullable=False)
  total_units = Column(Integer, nullable=False)
  teacher_id = Column(Integer, nullable=False)

  template_id = Column(
    Integer, ForeignKey("CourseTemplates.id"), nullable=False
  )
  template = relationship("CourseTemplate", backref="Courses")
