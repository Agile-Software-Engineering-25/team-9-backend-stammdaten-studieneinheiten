from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  teachers_in_courses_table
)


class Teachers(Base, BaseIdMixin):
  __tablename__ = "Teachers"

  external_id = Column(String, nullable=False, unique=True)

  courses = relationship(
    "Course",
    secondary=teachers_in_courses_table,
    back_populates="teachers",
  )