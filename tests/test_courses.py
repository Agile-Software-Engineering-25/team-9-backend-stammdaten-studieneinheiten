import pytest
from tests.conftest import override_get_db
from app.models.course_template import CourseTemplate
from app.models.course import Course


@pytest.fixture()
def course_templates():
  """Generate a list of course templates and add them to the DB"""
  db = next(override_get_db())
  templates: list[CourseTemplate] = []
  for i in range(5):
    template = CourseTemplate(name=f"Template {i}", elective=False)
    db.add(template)
    templates.append(template)
  db.commit()

  for t in templates:
    db.refresh(t)
    db.expunge(t)

  return templates


@pytest.fixture()
def courses(course_templates):
  """
  Generate a list of course instances based on a list of
  templates and add them to the DB
  """
  db = next(override_get_db())
  courses: list[Course] = []
  for i in range(len(course_templates)):
    course = Course(
      semester=i,
      exam_type="Exam",
      credit_points=2 * i,
      total_units=5 * i,
      template_id=course_templates[i].id,
    )
    db.add(course)
    courses.append(course)
  db.commit()

  for c in courses:
    db.refresh(c)
    db.expunge(c)

  return courses


def test_create_course_instance(client, course_templates):
  res = client.post(
    "/courses/",
    json={
      "template_id": course_templates[0].id,
      "semester": 2,
      "exam_type": "Prüfung",
      "credit_points": 5,
      "total_units": 45,
    },
  )
  assert res.status_code == 200


def test_get_all_courses(client, courses):
  res = client.get("/courses/")
  assert res.status_code == 200

  data = res.json()
  assert len(data) == len(courses)
  assert {c["id"] for c in data} == {c.id for c in courses}


def test_get_course(client, courses):
  c = courses[0]
  res = client.get(f"/courses/{c.id}")
  assert res.status_code == 200

  data = res.json()
  assert data["semester"] == c.semester
  assert data["exam_type"] == c.exam_type
  assert data["credit_points"] == c.credit_points
  assert data["total_units"] == c.total_units
  assert data["template_id"] == c.template_id
