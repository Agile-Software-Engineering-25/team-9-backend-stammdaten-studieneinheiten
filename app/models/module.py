from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base, BaseIdMixin


class Module(Base, BaseIdMixin):
    __tablename__ = "Module"

    template_id = Column(
        Integer, ForeignKey("ModuleTemplate.id"), nullable=False
    )

    #dozent_id = Column(
    #    Integer, ForeignKey("Dozent.id"), nullable=False
    #)

    #studiengang_id = Column(
    #    Integer, ForeignKey("Studiengang.id"), nullable=False
    #)
    template = relationship("ModuleTemplate", backref="Courses")
