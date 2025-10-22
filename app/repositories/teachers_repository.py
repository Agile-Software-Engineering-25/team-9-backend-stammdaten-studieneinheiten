from sqlalchemy.orm import Session
from app.models.teachers import Teachers
from app.schemas.teachers import TeacherCreate
from app.repositories.base import CRUDBase

teachers_crud = CRUDBase[Teachers, TeacherCreate](Teachers)
