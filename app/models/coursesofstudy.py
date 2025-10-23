from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  course_template_in_modules_table,
  module_templates_in_courseofstudy_templates_table,
)


class CoursesOfStudy(Base, BaseIdMixin):
  __tablename__ = "CoursesOfStudy"

  name = Column(String, nullable=False)