from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  students_in_courses_table
)


class Students(Base, BaseIdMixin):
  __tablename__ = "Students"

  external_id = Column(Integer, nullable=False, unique=True)

  courses = relationship(
    "Course",
    secondary=students_in_courses_table,
    back_populates="students",
  )