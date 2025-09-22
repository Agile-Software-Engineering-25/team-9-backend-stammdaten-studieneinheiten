from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  module_templates_in_courseofstudy_templates_table,
)


class CourseOfStudyTemplate(Base, BaseIdMixin):
  __tablename__ = "CourseOfStudyTemplates"

  name = Column(String, nullable=False)
  degree_type = Column(String, nullable=False)
  planned_semesters = Column(Integer)
  module_templates = relationship(
    "ModuleTemplate",
    secondary=module_templates_in_courseofstudy_templates_table,
    back_populates="courseofstudy_templates",
  )
