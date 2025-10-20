from app.models.students import Students
from app.schemas.student import StudentCreate
from app.repositories.base import CRUDBase

students_crud = CRUDBase[Students, StudentCreate](
  Students
)
