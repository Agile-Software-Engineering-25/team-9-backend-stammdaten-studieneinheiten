from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  modules_in_courseofstudy_table
)


class CoursesOfStudy(Base, BaseIdMixin):
  __tablename__ = "CoursesOfStudy"

  name = Column(String, nullable=False)
  startDate = Column(DateTime, nullable=False)
  endDate = Column(DateTime, nullable=False)
  cohort = Column(String, nullable=False)

  template_id = Column(
        Integer, ForeignKey("CourseOfStudyTemplates.id"), nullable=False
    )

  template = relationship("CourseOfStudyTemplate", backref="Courses")

  modules = relationship(
      "Module",
      secondary=modules_in_courseofstudy_table,
      back_populates="courseofstudy",
  )