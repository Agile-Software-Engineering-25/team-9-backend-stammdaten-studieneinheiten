def test_create_module_template(client):
  response = client.post(
    "/courses/templates/",
    json={
      "name": "Mathe",
      "elective": False,
      "code": "Test",
      "planned_semester": 69,
    },
  )
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == "Mathe"
  assert data["elective"] is False
  assert "id" in data

  response = client.post(
    "/modules/templates/",
    json={"name": "MatheMod", "course_template_ids": [data["id"]]},
  )
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == "MatheMod"
  assert "id" in data
  courseTemplates = data["course_templates"]
  assert len(courseTemplates) == 1
  checkedcourse = courseTemplates[0]
  assert checkedcourse["name"] == "Mathe"
  assert checkedcourse["elective"] is False


def test_get_course_template(client):
  create_resp = client.post(
    "/courses/templates/",
    json={
      "name": "GDI",
      "elective": False,
      "code": "Test",
      "planned_semester": 69,
    },
  )
  assert create_resp.status_code == 200
  template_id = create_resp.json()["id"]
  create_resp = client.post(
    "/modules/templates/",
    json={"name": "TestMod", "course_template_ids": [template_id]},
  )
  assert create_resp.status_code == 200
  template_id = create_resp.json()["id"]

  get_resp = client.get(f"/modules/templates/{template_id}")
  assert get_resp.status_code == 200
  data = get_resp.json()
  assert data["id"] == template_id
  assert data["name"] == "TestMod"

  courseTemplates = data["course_templates"]
  assert len(courseTemplates) == 1
  checkedcourse = courseTemplates[0]
  assert checkedcourse["name"] == "GDI"
  assert checkedcourse["elective"] is False


def test_get_nonexistent_course_template(client):
  random_id = 69

  response = client.get(f"/modules/templates/{random_id}")
  assert response.status_code == 404


def test_get_all_templates(client):
  create_resp = client.post(
    "/courses/templates/",
    json={
      "name": "GDI",
      "elective": False,
      "code": "Test",
      "planned_semester": 69,
    },
  )
  assert create_resp.status_code == 200
  testId = create_resp.json()["id"]
  # Generate random course templates and add them to the DB
  ids = [
    client.post(
      "/modules/templates/",
      json={"name": f"T{i}", "course_template_ids": [testId]},
    ).json()["id"]
    for i in range(3)
  ]

  # get all
  res = client.get("/modules/templates/")
  assert res.status_code == 200

  data = res.json()
  assert len(data) == 3
  assert {t["id"] for t in data} == set(ids)


def test_delete_template(client, module_templates, db_session):
  template_to_delete = module_templates[0]
  template_id = template_to_delete.id

  # verify associations exist
  from sqlalchemy import text

  count = db_session.execute(
    text(
      "SELECT COUNT(*) FROM course_template_in_modules "
      "WHERE module_template_id = :id"
    ),
    {"id": template_id},
  ).scalar()
  assert count != 0

  # Delete template
  res = client.delete(f"/modules/templates/{template_id}")
  assert res.status_code == 200

  # Verify associations deleted
  db_session.expire_all()
  count = db_session.execute(
    text(
      "SELECT COUNT(*) FROM course_template_in_modules "
      "WHERE module_template_id = :id"
    ),
    {"id": template_id},
  ).scalar()
  assert count == 0


def test_delete_template_with_instance(client, module_templates, courses):
  template_id = module_templates[0].id

  # create instance
  res = client.post(
    "/modules/",
    json={"template_id": template_id, "course_ids": [courses[0].id]},
  )
  assert res.status_code == 200

  # try delete
  res = client.delete(f"/modules/templates/{template_id}")
  assert res.status_code == 400
