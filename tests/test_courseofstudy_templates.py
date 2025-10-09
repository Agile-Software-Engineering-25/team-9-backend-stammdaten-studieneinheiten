def test_create_courseofstudy_template(client, module_templates):
  response = client.post(
    "/courseofstudies/templates/",
    json={
      "name": "BIN-T",
      "degree_type": "BSc",
      "planned_semesters": 6,
      "part_time":True,
      "module_template_ids": [mt.id for mt in module_templates[0:3]],
    },
  )
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == "BIN-T"
  assert "id" in data
  checkTemplates = data["module_templates"]
  assert len(checkTemplates) == 3
  for mt in checkTemplates:
    assert mt["id"]
    compareTemplate = next(
      (t for t in module_templates if t.id == mt["id"]), None
    )
    assert compareTemplate
    assert mt["name"] == compareTemplate.name


def test_get_courseofstudy_template(client, courseofstudy_templates):
  template = courseofstudy_templates[0]
  response = client.get(f"/courseofstudies/templates/{template.id}")
  assert response.status_code == 200
  data = response.json()
  assert data["id"] == template.id
  assert data["name"] == template.name
  assert data["degree_type"] == template.degree_type
  assert data["planned_semesters"] == template.planned_semesters
  assert data["part_time"] == template.part_time


def test_get_nonexistent_courseofstudy_template(client):
  id = 420
  response = client.get(f"/courseofstudies/templates/{id}")
  assert response.status_code == 404


def test_create_courseofstudy_no_modules(client):
  response = client.post(
    "/courseofstudies/templates/",
    json={
      "name": "Invalid",
      "degree_type": "professional idiot",
      "planned_semesters": 69,
      "module_template_ids": [],
      "part_time":False
    },
  )
  assert response.status_code == 400


def test_get_all_courseofstudy_templates(client, courseofstudy_templates):
  response = client.get("/courseofstudies/templates/")
  assert response.status_code == 200
  data = response.json()
  assert len(data) == len(courseofstudy_templates)
  assert {t["id"] for t in data} == {t.id for t in courseofstudy_templates}
