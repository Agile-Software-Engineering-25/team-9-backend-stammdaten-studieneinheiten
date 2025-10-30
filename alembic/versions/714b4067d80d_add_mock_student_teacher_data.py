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
    
    # Step 1: Delete all association table rows that reference the specific mock data
    # we're about to insert (to make this migration idempotent)
    # Note: We only delete rows related to our mock student/teacher, not all data
    
    # First, check if our mock student/teacher already exist and clean up their associations
    result = conn.execute(sa.text('SELECT id FROM "Students" WHERE external_id = :external_id'), 
                         {'external_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509'})
    student_row = result.fetchone()
    if student_row:
        student_id = student_row[0]
        conn.execute(sa.text('DELETE FROM students_in_courses WHERE student_id = :student_id'), 
                    {'student_id': student_id})
        conn.execute(sa.text('DELETE FROM "Students" WHERE id = :student_id'), 
                    {'student_id': student_id})
    
    result = conn.execute(sa.text('SELECT id FROM "Teachers" WHERE external_id = :external_id'), 
                         {'external_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1'})
    teacher_row = result.fetchone()
    if teacher_row:
        teacher_id = teacher_row[0]
        conn.execute(sa.text('DELETE FROM teachers_in_courses WHERE teacher_id = :teacher_id'), 
                    {'teacher_id': teacher_id})
        conn.execute(sa.text('DELETE FROM "Teachers" WHERE id = :teacher_id'), 
                    {'teacher_id': teacher_id})
    
    # Clean up any existing mock course templates and their courses by code
    # (assuming MATH1, ENG1, etc. are unique to this mock data)
    mock_codes = ['MATH1', 'ENG1', 'INFO1', 'LWA', 'PROG1', 'ADS', 'PROG2', 'KOMM', 
                  'MATH2', 'TI', 'OS', 'DB', 'SEC', 'NET', 'PM', 'ASE', 'DABD', 
                  'HCI', 'IKHT', 'TIRA']
    
    # Build IN clause for SQL (works on both SQLite and PostgreSQL)
    codes_placeholder = ','.join([f':code{i}' for i in range(len(mock_codes))])
    codes_params = {f'code{i}': code for i, code in enumerate(mock_codes)}
    
    # Get IDs of existing mock templates
    result = conn.execute(
        sa.text(f'SELECT id FROM "CourseTemplates" WHERE code IN ({codes_placeholder})'), 
        codes_params
    )
    template_ids = [row[0] for row in result.fetchall()]
    
    if template_ids:
        # Build IN clause for template_ids
        template_ids_placeholder = ','.join([f':tid{i}' for i in range(len(template_ids))])
        template_ids_params = {f'tid{i}': tid for i, tid in enumerate(template_ids)}
        
        # Get course IDs that reference these templates
        result = conn.execute(
            sa.text(f'SELECT id FROM "Courses" WHERE template_id IN ({template_ids_placeholder})'), 
            template_ids_params
        )
        course_ids = [row[0] for row in result.fetchall()]
        
        if course_ids:
            # Build IN clause for course_ids
            course_ids_placeholder = ','.join([f':cid{i}' for i in range(len(course_ids))])
            course_ids_params = {f'cid{i}': cid for i, cid in enumerate(course_ids)}
            
            # Delete associations first
            conn.execute(
                sa.text(f'DELETE FROM teachers_in_courses WHERE course_id IN ({course_ids_placeholder})'), 
                course_ids_params
            )
            conn.execute(
                sa.text(f'DELETE FROM students_in_courses WHERE course_id IN ({course_ids_placeholder})'), 
                course_ids_params
            )
            conn.execute(
                sa.text(f'DELETE FROM courses_in_module WHERE course_id IN ({course_ids_placeholder})'), 
                course_ids_params
            )
            # Delete courses
            conn.execute(
                sa.text(f'DELETE FROM "Courses" WHERE id IN ({course_ids_placeholder})'), 
                course_ids_params
            )
        
        # Delete associations with templates
        conn.execute(
            sa.text(f'DELETE FROM course_template_in_modules WHERE course_template_id IN ({template_ids_placeholder})'), 
            template_ids_params
        )
        # Delete templates
        conn.execute(
            sa.text(f'DELETE FROM "CourseTemplates" WHERE id IN ({template_ids_placeholder})'), 
            template_ids_params
        )
    
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
    
    # Insert templates and capture the actual generated IDs
    template_ids = []
    for template in course_templates:
        result = conn.execute(
            sa.text(
                'INSERT INTO "CourseTemplates" (name, code, elective, planned_semester) '
                'VALUES (:name, :code, :elective, :planned_semester) RETURNING id'
            ),
            template
        )
        template_ids.append(result.fetchone()[0])
    
    # Create Courses based on templates using actual IDs
    courses = [
        # Semester 1
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 0},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 1},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 2},
        {'semester': 1, 'exam_type': 'Portfolio', 'credit_points': 5, 'total_units': 60, 'template_idx': 3},
        {'semester': 1, 'exam_type': 'Klausur', 'credit_points': 10, 'total_units': 120, 'template_idx': 4},
        # Semester 2
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 10, 'total_units': 120, 'template_idx': 5},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 6},
        {'semester': 2, 'exam_type': 'Präsentation', 'credit_points': 5, 'total_units': 60, 'template_idx': 7},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 8},
        {'semester': 2, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 9},
        # Semester 3
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 10},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 11},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 12},
        {'semester': 3, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 13},
        {'semester': 3, 'exam_type': 'Portfolio', 'credit_points': 5, 'total_units': 60, 'template_idx': 14},
        # Semester 4
        {'semester': 4, 'exam_type': 'Kombiniert', 'credit_points': 10, 'total_units': 120, 'template_idx': 15},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 16},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 17},
        {'semester': 4, 'exam_type': 'Präsentation', 'credit_points': 5, 'total_units': 60, 'template_idx': 18},
        {'semester': 4, 'exam_type': 'Klausur', 'credit_points': 5, 'total_units': 60, 'template_idx': 19},
    ]
    
    course_ids = []
    for course in courses:
        template_idx = course.pop('template_idx')
        course['template_id'] = template_ids[template_idx]
        result = conn.execute(
            sa.text(
                'INSERT INTO "Courses" (semester, exam_type, credit_points, total_units, template_id) '
                'VALUES (:semester, :exam_type, :credit_points, :total_units, :template_id) RETURNING id'
            ),
            course
        )
        course_ids.append(result.fetchone()[0])
    
    # Create Student with the specified external_id
    result = conn.execute(
        sa.text(
            'INSERT INTO "Students" (external_id) VALUES (:external_id) RETURNING id'
        ),
        {'external_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509'}
    )
    student_id = result.fetchone()[0]
    
    # Link student to all courses using actual course IDs
    for course_id in course_ids:
        conn.execute(
            sa.text(
                "INSERT INTO students_in_courses (course_id, student_id) "
                "VALUES (:course_id, :student_id)"
            ),
            {'course_id': course_id, 'student_id': student_id}
        )

    # Create Teacher with the specified external_id
    result = conn.execute(
        sa.text(
            'INSERT INTO "Teachers" (external_id) VALUES (:external_id) RETURNING id'
        ),
        {'external_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1'}
    )
    teacher_id = result.fetchone()[0]

    # Link teacher to all courses using actual course IDs
    for course_id in course_ids:
            conn.execute(
                sa.text(
                    "INSERT INTO teachers_in_courses (course_id, teacher_id) "
                    "VALUES (:course_id, :teacher_id)"
                ),
                {'course_id': course_id, 'teacher_id': teacher_id}
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
