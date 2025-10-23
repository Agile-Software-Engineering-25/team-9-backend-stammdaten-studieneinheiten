from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin
from app.models.association_tables import (
  courses_in_module_table,
  modules_in_courseofstudy_table
)


class Module(Base, BaseIdMixin):
    __tablename__ = "Module"

    template_id = Column(
        Integer, ForeignKey("ModuleTemplates.id"), nullable=False
    )

    template = relationship("ModuleTemplate", backref="Courses")

    courses = relationship(
        "Course",
        secondary=courses_in_module_table,
        back_populates="module",
    )

    courseofstudy = relationship(
      "CoursesOfStudy", #CLUE Could be table or class, dunno if that matters
      secondary=modules_in_courseofstudy_table,
      back_populates="modules",
  )


