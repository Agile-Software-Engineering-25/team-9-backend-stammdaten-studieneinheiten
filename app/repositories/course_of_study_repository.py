from app.models.coursesofstudy import CoursesOfStudy
from app.schemas.coursesofstudy import CourseofStudyCreate
from app.repositories.base import CRUDBase

course_of_study_crud = CRUDBase[CoursesOfStudy, CourseofStudyCreate](
  CoursesOfStudy
)
