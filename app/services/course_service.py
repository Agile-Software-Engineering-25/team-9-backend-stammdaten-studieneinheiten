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
    # 1. Extract base course data (no relationship lists)
    if hasattr(payload, "model_dump"):
        data = payload.model_dump(
            exclude={"student_ids", "teacher_ids"},
            exclude_unset=True,
        )
    else:
        data = payload.dict(
            exclude={"student_ids", "teacher_ids"},
            exclude_unset=True,
        )

    # Prepare relationship objects
    ordered_students = None
    added_teachers = None

    # 2. Handle students if provided
    if payload.student_ids:
        # Deduplicate but keep order
        requested_ids = list(dict.fromkeys(payload.student_ids))

        stmt = select(Students).where(Students.external_id.in_(requested_ids))
        existing_students = list(db.scalars(stmt))
        existing_by_external = {s.external_id: s for s in existing_students}

        # Find which external_ids don't exist yet
        missing_ids = [
            eid for eid in requested_ids if eid not in existing_by_external
        ]

        # Create missing Students
        new_students = [Students(external_id=eid) for eid in missing_ids]
        if new_students:
            db.add_all(new_students)
            db.flush()  # assign PKs

            # Add them to the lookup
            for s in new_students:
                existing_by_external[s.external_id] = s

        # Build list in original order
        ordered_students = [
            existing_by_external[eid] for eid in requested_ids
        ]

    # 3. Handle teachers if provided
    if payload.teacher_ids:
        requested_ids = list(dict.fromkeys(payload.teacher_ids))

        stmt = select(Teachers).where(Teachers.external_id.in_(requested_ids))
        existing_teachers = list(db.scalars(stmt))
        existing_by_external = {t.external_id: t for t in existing_teachers}

        missing_ids = [
            eid for eid in requested_ids if eid not in existing_by_external
        ]

        new_teachers = [Teachers(external_id=eid) for eid in missing_ids]
        if new_teachers:
            db.add_all(new_teachers)
            db.flush()
            for tchr in new_teachers:
                existing_by_external[tchr.external_id] = tchr

        added_teachers = [
            existing_by_external[eid] for eid in requested_ids
        ]

    # 4. Create the Course itself
    course = Course(**data)

    if ordered_students is not None:
        course.students = ordered_students

    if added_teachers is not None:
        course.teachers = added_teachers

    db.add(course)
    db.commit()
    db.refresh(course)

    return course