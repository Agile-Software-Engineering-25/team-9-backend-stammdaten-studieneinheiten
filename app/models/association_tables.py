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

module_templates_in_courseofstudy_templates_table = Table(
  "module_template_in_courseofstudy_templates",
  Base.metadata,
  Column(
    "module_template_id", ForeignKey("ModuleTemplates.id"), primary_key=True
  ),
  Column(
    "courseofstudy_template_id",
    ForeignKey("CourseOfStudyTemplates.id"),
    primary_key=True,
  ),
)

students_in_course = Table(
  "students_in_course",
  Base.metadata,
  Column(
    "course_id", 
    ForeignKey("Courses.id"), 
    primary_key=True
  ),
  Column(
    "student_id",
    ForeignKey("Students.id"),
    primary_key=True,
  ),
)
