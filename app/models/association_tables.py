from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from app.core.db import Base, BaseIdMixin

course_template_in_modules_table = Table(
  "course_template_in_modules",
  Base.metadata,
  Column(
    "course_template_id", ForeignKey("CourseTemplates.id"), primary_key=True
  ),
  Column(
    "module_template_id", ForeignKey("ModuleTemplates.id"), primary_key=True
  ),
)
