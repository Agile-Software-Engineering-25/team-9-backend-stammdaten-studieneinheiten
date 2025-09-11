def test_create_course_template(client):
  response = client.post(
    "/courses/templates/",
    json={
      "name": "Mathe",
      "elective": False,
      "planned_semester": 1,
      "code": "M1",
    },
  )
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == "Mathe"
  assert data["code"] == "M1"
  assert data["planned_semester"] == 1
  assert data["elective"] is False
  assert "id" in data


def test_get_course_template(client):
  create_resp = client.post(
    "/courses/templates/",
    json={
      "name": "Grundlagen der Informatik",
      "elective": False,
      "planned_semester": 1,
      "code": "GDI",
    },
  )
  assert create_resp.status_code == 200
  template_id = create_resp.json()["id"]

  get_resp = client.get(f"/courses/templates/{template_id}")
  assert get_resp.status_code == 200
  data = get_resp.json()
  assert data["id"] == template_id
  assert data["name"] == "Grundlagen der Informatik"
  assert data["code"] == "GDI"
  assert data["planned_semester"] == 1
  assert data["elective"] is False


def test_get_nonexistent_course_template(client):
  random_id = 420

  response = client.get(f"/courses/templates/{random_id}")
  assert response.status_code == 404
  assert response.json()["detail"] == "Course Template not found"


def test_get_all_templates(client):
  # Generate random course templates and add them to the DB
  ids = [
    client.post(
      "/courses/templates/",
      json={
        "name": f"Template {i}",
        "elective": True,
        "planned_semester": i % 6,
        "code": f"T{i}",
      },
    ).json()["id"]
    for i in range(3)
  ]

  # get all
  res = client.get("/courses/templates/")
  assert res.status_code == 200

  data = res.json()
  assert len(data) == 3
  assert {t["id"] for t in data} == set(ids)
