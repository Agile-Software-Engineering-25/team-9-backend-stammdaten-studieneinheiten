from sqlalchemy import Column, String, Boolean, Integer
from app.core.db import Base, BaseIdMixin
from sqlalchemy.orm import relationship
from app.models.association_tables import course_template_in_modules_table


class CourseTemplate(Base, BaseIdMixin):
  __tablename__ = "CourseTemplates"

  name = Column(String, nullable=False)
  elective = Column(Boolean, default=False)
  module_templates = relationship(
    "ModuleTemplate",
    secondary=course_template_in_modules_table,
    back_populates="course_templates",
  )
