from sqlalchemy.orm import Session
from app.models.students import Students
from app.schemas.students import StudentsCreate
from app.repositories.base import CRUDBase

student_crud = CRUDBase[Students, StudentsCreate](Students)
