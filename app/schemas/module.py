from pydantic import BaseModel, ConfigDict
from app.schemas.module_templates import ModuleTemplateRead
from app.schemas.course import CourseRead



class ModuleBase(BaseModel):
    pass

class ModuleCreate(ModuleBase):
    course_ids: list[int]
    template_id: int



class ModuleRead(ModuleBase):
    id: int
    template: ModuleTemplateRead
    courses: list[CourseRead]

    model_config = ConfigDict(from_attributes=True)
