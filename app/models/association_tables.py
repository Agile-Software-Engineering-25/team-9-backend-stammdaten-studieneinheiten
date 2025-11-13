from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from app.core.db import Base, BaseIdMixin

course_template_in_modules_table = Table(
  "course_template_in_modules",
  Base.metadata,
  Column(
    "course_template_id",
    ForeignKey(
      "CourseTemplates.id",
      ondelete="CASCADE",
      name="course_template_in_modules_course_template_id_fkey",
    ),
    primary_key=True,
  ),
  Column(
    "module_template_id",
    ForeignKey(
      "ModuleTemplates.id",
      ondelete="CASCADE",
      name="course_template_in_modules_module_template_id_fkey",
    ),
    primary_key=True,
  ),
)

module_templates_in_courseofstudy_templates_table = Table(
  "module_template_in_courseofstudy_templates",
  Base.metadata,
  Column(
    "module_template_id",
    ForeignKey(
      "ModuleTemplates.id",
      ondelete="CASCADE",
      name="module_template_in_courseofstudy_templates_module_template_id_fkey",
    ),
    primary_key=True,
  ),
  Column(
    "courseofstudy_template_id",
    ForeignKey(
      "CourseOfStudyTemplates.id",
      ondelete="CASCADE",
      name="module_template_in_courseofstudy_templates_courseofstudy_template_id_fkey",
    ),
    primary_key=True,
  ),
)


students_in_courses_table = Table(
  "students_in_courses",
  Base.metadata,
  Column("course_id", ForeignKey("Courses.id"), primary_key=True),
  Column("student_id", ForeignKey("Students.id"), primary_key=True),
)

teachers_in_courses_table = Table(
  "teachers_in_courses",
  Base.metadata,
  Column("course_id", ForeignKey("Courses.id"), primary_key=True),
  Column("teacher_id", ForeignKey("Teachers.id"), primary_key=True),
)


courses_in_module_table = Table(
  "courses_in_module",
  Base.metadata,
  Column(
    "course_id",
    ForeignKey("Courses.id", name="courses_in_module_course_id_fkey"),
    primary_key=True,
  ),
  Column(
    "module_id",
    ForeignKey("Module.id", name="courses_in_module_module_id_fkey"),
    primary_key=True,
  ),
)

modules_in_courseofstudy_table = Table(
  "modules_in_coursesofstudy",
  Base.metadata,
  Column("courseofstudy_id", ForeignKey("CoursesOfStudy.id"), primary_key=True),
  Column("module_id", ForeignKey("Module.id"), primary_key=True),
)
