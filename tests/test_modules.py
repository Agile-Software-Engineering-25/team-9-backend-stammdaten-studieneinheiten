import pytest
from app.models.module_templates import ModuleTemplate
from app.models.module import Module


def test_modules_exist(client, modules):
  assert modules


def test_delete_module(client, modules):
  m = modules[0]
  res = client.delete(f"/modules/{m.id}")
  assert res.status_code == 200
