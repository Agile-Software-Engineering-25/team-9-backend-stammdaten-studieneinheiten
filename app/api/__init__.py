from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from . import (
  me,
  health,
  course_templates,
  courses,
  module_templates,
  courseofstudy_templates,
)

# Every route under this router requires the user to be authenticated
api_router = APIRouter(dependencies=[Depends(get_current_user)])
api_router.include_router(me.router)
api_router.include_router(health.router)
api_router.include_router(course_templates.router)
api_router.include_router(courses.router)
api_router.include_router(module_templates.router)
api_router.include_router(courseofstudy_templates.router)
