from sqlalchemy.orm import Session
from app.repositories.course_repository import course_crud
from app.schemas.course import CourseCreate

from app.models.course import Course
from sqlalchemy import select
from app.models.students import Students

from app.models.teachers import Teachers
from fastapi import HTTPException
from app.schemas.students import StudentsCreate




# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course(db: Session):
  return course_crud.get_all(db)


def get_course(db: Session, template_id: int):
  return course_crud.get(db, template_id)



def create_course(db: Session, payload: CourseCreate):
    # Turn the payload into a dict, excluding students list (Pydantic v2 shown)
    if hasattr(payload, "model_dump"):
        data = payload.model_dump(exclude={"student_ids, teacher_ids"}, exclude_unset=True)
    else:
        data = payload.dict(exclude={"student_ids, teacher_ids"}, exclude_unset=True)  # Pydantic v1 fallback

    # If no students provided → just create via CRUD
    if not getattr(payload, "student_ids", None):
        if not getattr(payload, "teacher_ids", None):
            return course_crud.create(db, payload)
        
    ordered_students=None
    added_teachers = None
    if getattr(payload, "student_ids", None):
        # 1) Fetch existing Students by external_id
        #    De-duplicate input to avoid extra work
        requested_ids = list(dict.fromkeys(payload.student_ids))  # preserves order, removes dups
        stmt = select(Students).where(Students.external_id.in_(requested_ids))
        existing_students = list(db.scalars(stmt))
        existing_by_external = {s.external_id: s for s in existing_students}

        # 2) Figure out which external_ids are missing
        missing_ids = [eid for eid in requested_ids if eid not in existing_by_external]

        # 3) Create missing Students
        new_students = []
        for eid in missing_ids:
            new_students.append(Students(external_id=eid))

        if new_students:
            db.add_all(new_students)
            # flush to assign primary keys and make them usable in relationship before commit
            db.flush()
            for s in new_students:
                existing_by_external[s.external_id] = s

        # Build the complete, ordered student list matching the requested external_id order
        ordered_students = [existing_by_external[eid] for eid in requested_ids]

    if getattr(payload, "teacher_ids", None):
        # 1) Fetch existing Students by external_id
        #    De-duplicate input to avoid extra work
        requested_ids = list(dict.fromkeys(payload.teacher_ids))  # preserves order, removes dups
        stmt = select(Teachers).where(Teachers.external_id.in_(requested_ids))
        existing_teachers = list(db.scalars(stmt))
        existing_by_external = {s.external_id: s for s in existing_teachers}

        # 2) Figure out which external_ids are missing
        missing_ids = [eid for eid in requested_ids if eid not in existing_by_external]

        # 3) Create missing Students
        new_teachers = []
        for eid in missing_ids:
            new_teachers.append(Teachers(external_id=eid))

        if new_teachers:
            db.add_all(new_teachers)
            # flush to assign primary keys and make them usable in relationship before commit
            db.flush()
            for s in new_teachers:
                existing_by_external[s.external_id] = s

        # Build the complete, ordered student list matching the requested external_id order
        added_teachers = [existing_by_external[eid] for eid in requested_ids]

    print(data)
     # Pull & remove relationship id lists from the data dict
    student_ids = data.pop("student_ids", None)
    teacher_ids = data.pop("teacher_ids", None)

    # 4) Create the Course and attach students
    course = Course(**data)

    if ordered_students!=None:
        course.students = ordered_students

    if added_teachers!= None:
        course.teachers = added_teachers

    db.add(course)
    db.commit()
    db.refresh(course)
    print(course)
    return course
