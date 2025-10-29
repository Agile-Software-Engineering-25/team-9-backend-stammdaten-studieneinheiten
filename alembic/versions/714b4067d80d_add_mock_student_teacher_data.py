"""add_mock_student_data

Revision ID: 714b4067d80d
Revises: 68fd60694c89
Create Date: 2025-10-28 22:33:54.841115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '714b4067d80d'
down_revision: Union[str, Sequence[str], None] = '68fd60694c89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    # WARNING: destructive cleanup to avoid inserting mock data on top of
    # existing (possibly production) rows. This will remove all rows from
    # the association tables and the tables that this migration inserts into.
    # Keep the delete order: associations -> child tables to avoid FK errors.
    conn.execute(sa.text('DELETE FROM teachers_in_courses'))
    conn.execute(sa.text('DELETE FROM students_in_courses'))
    # Remove existing courses (child of CourseTemplates)
    # Table names defined in models use CamelCase and are created as
    # case-sensitive identifiers in migrations; quote them here to match.
    conn.execute(sa.text('DELETE FROM "Courses"'))
    # Remove course templates
    conn.execute(sa.text('DELETE FROM "CourseTemplates"'))
    # Remove teachers and students
    conn.execute(sa.text('DELETE FROM "Teachers"'))
    conn.execute(sa.text('DELETE FROM "Students"'))
    
    # Create CourseTemplates based on the frontend mock data
    course_templates = [
        # Semester 1
        {'name': 'Mathematik 1', 'code': 'MATH1', 'elective': False, 'planned_semester': 1},
        {'name': 'Sprachkompetenz Englisch', 'code': 'ENG1', 'elective': False, 'planned_semester': 1},
        {'name': 'Grundlagen der Informatik', 'code': 'INFO1', 'elective': False, 'planned_semester': 1},
        {'name': 'Lerntechniken und wissenschaftliches Arbeiten', 'code': 'LWA', 'elective': False, 'planned_semester': 1},
        {'name': 'Programmierung', 'code': 'PROG1', 'elective': False, 'planned_semester': 1},
        # Semester 2
        {'name': 'Algorithmen und Datenstrukturen', 'code': 'ADS', 'elective': False, 'planned_semester': 2},
        {'name': 'Fortgeschrittene Programmierung', 'code': 'PROG2', 'elective': False, 'planned_semester': 2},
        {'name': 'Kommunikationskompetenz', 'code': 'KOMM', 'elective': False, 'planned_semester': 2},
        {'name': 'Mathematik 2', 'code': 'MATH2', 'elective': False, 'planned_semester': 2},
        {'name': 'Theoretische Informatik', 'code': 'TI', 'elective': False, 'planned_semester': 2},
        # Semester 3
        {'name': 'Betriebssysteme', 'code': 'OS', 'elective': False, 'planned_semester': 3},
        {'name': 'Datenmodellierung und Datenbanken', 'code': 'DB', 'elective': False, 'planned_semester': 3},
        {'name': 'Informationssicherheit', 'code': 'SEC', 'elective': False, 'planned_semester': 3},
        {'name': 'Netze und verteilte Systeme', 'code': 'NET', 'elective': False, 'planned_semester': 3},
        {'name': 'Projektmanagement', 'code': 'PM', 'elective': False, 'planned_semester': 3},
        # Semester 4
        {'name': 'Agile Software Engineering und Softwaretechnik', 'code': 'ASE', 'elective': False, 'planned_semester': 4},
        {'name': 'Data Analytics & Big Data', 'code': 'DABD', 'elective': False, 'planned_semester': 4},
        {'name': 'Human-Computer-Interaction', 'code': 'HCI', 'elective': False, 'planned_semester': 4},
        {'name': 'Interkulturelle Kommunikation und heterogene Teams', 'code': 'IKHT', 'elective': False, 'planned_semester': 4},
        {'name': 'Technische Informatik und Rechnerarchitekturen und XAAS', 'code': 'TIRA', 'elective': False, 'planned_semester': 4},
    ]
    
    for template in course_templates:
        conn.execute(
            sa.text(
                'INSERT INTO "CourseTemplates" (name, code, elective, planned_semester) '
                'VALUES (:name, :code, :elective, :planned_semester)'
            ),
            template
        )
    
    # Create Courses based on templates
    courses = [
        # Semester 1
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 1},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 2},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 3},
        {'semester': 1, 'exam_type': 'Portfolio', 'credit_points': 5, 'total_units': 60, 'template_id': 4},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 10, 'total_units': 120, 'template_id': 5},
        # Semester 2
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 10, 'total_units': 120, 'template_id': 6},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 7},
        {'semester': 2, 'exam_type': 'Präsentation', 'credit_points': 5, 'total_units': 60, 'template_id': 8},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 9},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 10},
        # Semester 3
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 11},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 12},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 13},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 14},
        {'semester': 3, 'exam_type': 'Portfolio', 'credit_points': 5, 'total_units': 60, 'template_id': 15},
        # Semester 4
        {'semester': 4, 'exam_type': 'Kombiniert', 'credit_points': 10, 'total_units': 120, 'template_id': 16},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 17},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 18},
        {'semester': 4, 'exam_type': 'Präsentation', 'credit_points': 5, 'total_units': 60, 'template_id': 19},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_id': 20},
    ]
    
    for course in courses:
        conn.execute(
            sa.text(
                'INSERT INTO "Courses" (semester, exam_type, credit_points, total_units, template_id) '
                'VALUES (:semester, :exam_type, :credit_points, :total_units, :template_id)'
            ),
            course
        )
    
    # Create Student with the specified external_id
    conn.execute(
        sa.text(
            'INSERT INTO "Students" (external_id) VALUES (:external_id)'
        ),
        {'external_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509'}
    )
    
    # Link student to all courses (course_id 1-20, student_id 1)
    for course_id in range(1, 21):
        conn.execute(
            sa.text(
                "INSERT INTO students_in_courses (course_id, student_id) "
                "VALUES (:course_id, :student_id)"
            ),
            {'course_id': course_id, 'student_id': 1}
        )

    # Create Teacher with the specified external_id
    conn.execute(
        sa.text(
            'INSERT INTO "Teachers" (external_id) VALUES (:external_id)'
        ),
        {'external_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1'}
    )

    # Link teacher to all courses (course_id 1-20, teacher_id 1)
    for course_id in range(1, 21):
            conn.execute(
                sa.text(
                    "INSERT INTO teachers_in_courses (course_id, teacher_id) "
                    "VALUES (:course_id, :teacher_id)"
                ),
                {'course_id': course_id, 'teacher_id': 1}
            )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    
    # Remove associations
    conn.execute(
    sa.text('DELETE FROM students_in_courses WHERE student_id = 1')
    )
    
    # Remove student
    conn.execute(
    sa.text('DELETE FROM "Students" WHERE external_id = :external_id'),
    {'external_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509'}
    )

    # Remove associations with teacher
    conn.execute(
    sa.text('DELETE FROM teachers_in_courses WHERE teacher_id = 1')
    )

    # Remove teacher
    conn.execute(
    sa.text('DELETE FROM "Teachers" WHERE external_id = :external_id'),
    {'external_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1'}
    )
    
    # Remove courses
    conn.execute(
    sa.text('DELETE FROM "Courses" WHERE id BETWEEN 1 AND 20')
    )
    
    # Remove course templates
    conn.execute(
    sa.text('DELETE FROM "CourseTemplates" WHERE id BETWEEN 1 AND 20')
    )
