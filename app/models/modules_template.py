from sqlalchemy import Column, String, Boolean, Integer
from app.core.db import Base, BaseIdMixin


class ModuleTemplate(Base, BaseIdMixin):
  __tablename__ = "ModuleTemplates"

  name = Column(String, nullable=False)
