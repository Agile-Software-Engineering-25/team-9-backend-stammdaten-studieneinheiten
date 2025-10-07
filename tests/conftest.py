import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.db import Base, get_db
from app.main import fastapi_app as app
from app.models.course_template import CourseTemplate
from app.models.course import Course
from app.models.module_templates import ModuleTemplate
from app.models.courseofstudy_templates import CourseOfStudyTemplate

# Test DB Setup
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False)


# Dependency override
def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_db():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  yield


@pytest.fixture
def client():
  return TestClient(app)


# MARK: Test data fixtures
@pytest.fixture()
def course_templates():
  """Generate a list of course templates and add them to the DB"""
  db = next(override_get_db())
  templates: list[CourseTemplate] = []
  for i in range(20):
    template = CourseTemplate(
      name=f"Template {i}", elective=False, code=f"T{i}", planned_semester=i
    )
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


@pytest.fixture()
def module_templates(course_templates):
  """
  Generate a list of module templates based on a list of course templates
  and add them to the DB
  """
  db = next(override_get_db())
  templates: list[ModuleTemplate] = []
  count = len(course_templates) // 2
  for i in range(count):
    template = ModuleTemplate(
      name=f"ModuleTemplate {i}",
      course_templates=course_templates[(i * 2) : (i * 2 + 2)],
    )
    db.add(template)
    templates.append(template)
  db.commit()

  for t in templates:
    db.refresh(t)
    db.expunge(t)

  return templates


@pytest.fixture()
def courseofstudy_templates(module_templates):
  """
  Generate a list of courseofstudy templates
  based on a list of course and module templates
  and add them to the DB
  """
  db = next(override_get_db())
  templates: list[CourseOfStudyTemplate] = []
  count = len(module_templates) // 3
  for i in range(count):
    template = CourseOfStudyTemplate(
      name=f"COS Template {i}",
      planned_semesters=6,
      degree_type="BSc",
      module_templates=module_templates[(i * 3) : (i * 3 + 3)],
    )
    db.add(template)
    templates.append(template)
  db.commit()

  for t in templates:
    db.refresh(t)
    db.expunge(t)

  return templates
