from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  course_template_in_modules_table,
  module_templates_in_courseofstudy_templates_table,
)


class ModuleTemplate(Base, BaseIdMixin):
  __tablename__ = "ModuleTemplates"

  name = Column(String, nullable=False)
  course_templates = relationship(
    "CourseTemplate",
    secondary=course_template_in_modules_table,
    back_populates="module_templates",
    passive_deletes=True,
  )
  courseofstudy_templates = relationship(
    "CourseOfStudyTemplate",
    secondary=module_templates_in_courseofstudy_templates_table,
    back_populates="module_templates",
  )
