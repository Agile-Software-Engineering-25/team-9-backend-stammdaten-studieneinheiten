from app.models.courseofstudy_templates import CourseOfStudyTemplate
from app.schemas.courseofstudy_template import CourseOfStudyTemplateCreate
from app.repositories.base import CRUDBase

courseofstudy_template_crud = CRUDBase[
  CourseOfStudyTemplate, CourseOfStudyTemplateCreate
](CourseOfStudyTemplate)
