from sqlalchemy.orm import Session
from app.repositories.course_repository import course_crud
from app.schemas.course import CourseCreate

from app.models.course import Course
from sqlalchemy import select
from app.models.students import Students

from app.models.teachers import Teachers
from fastapi import HTTPException
from app.schemas.students import StudentsCreate
from sqlalchemy.exc import NoResultFound




# In this case, this file only contains wrappers and could be optional.
# For more commplex models, there might be more business logic
# required. This business logic should go here.


def list_course(db: Session):
  return course_crud.get_all(db)


def get_course(db: Session, template_id: int):
  return course_crud.get(db, template_id)

def delete_course(db: Session, template_id: int):
    return course_crud.delete(db, template_id)

def validate_id_existence(db:Session, table, requested_ids):
    stmt = select(table).where(table.external_id.in_(requested_ids))
    existing = list(db.scalars(stmt))
    existing_by_external = {s.external_id: s for s in existing}

    # Find which external_ids don't exist yet
    missing_ids = [
        eid for eid in requested_ids if eid not in existing_by_external
    ]

    # Create missing Objects
    new_objects = [table(external_id=eid) for eid in missing_ids]
    if new_objects:
        db.add_all(new_objects)
        db.flush()  # assign PKs

        # Add them to the lookup
        for s in new_objects:
            existing_by_external[s.external_id] = s

    # Build list in original order
    ordered_objects = [
        existing_by_external[eid] for eid in requested_ids
    ]
    return ordered_objects


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

        ordered_students=validate_id_existence(db, Students, requested_ids)

    # 3. Handle teachers if provided
    if payload.teacher_ids:
        requested_ids = list(dict.fromkeys(payload.teacher_ids))

        added_teachers=validate_id_existence(db, Teachers, requested_ids)

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


def edit_course(db:Session, id, payload: CourseCreate):
    try:
        course = db.query(Course).filter(Course.id == id).one()
    except NoResultFound:
        raise ValueError(f"Course {id} not found")
    

    update_data = payload.model_dump(exclude_unset=True)
    print(update_data)
    complex_attributes=['student_ids', 'teacher_ids']
    for field, value in update_data.items():
        if field in complex_attributes:
            if field=='teacher_ids':
                requested_ids = list(value)
                added_teachers=validate_id_existence(db, Teachers, requested_ids)
                setattr(course, 'teachers', added_teachers)
            elif field=='student_ids':
                requested_ids = list(value)
                new_students=validate_id_existence(db, Students, requested_ids)
                setattr(course, 'students', new_students)

        else:
            if hasattr(Course, field):
                setattr(course, field, value)

    # committing will flush the mutations as UPDATE
    db.commit()

    # optional: session.refresh(user) to ensure we return DB state
    return course
