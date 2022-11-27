# test_device

import asyncio
from fastapi.testclient import TestClient

import json
from lira_backend_api.v1.tests.conftest import *

def test_get_device_id(client):
    # async def run(Asyclient):
    response = client.get("/device/47690661-f343-4591-920c-50dcd59f74e2")
    assert response.status_code == 200
    assert response.json() == {
        'id': '47690661-f343-4591-920c-50dcd59f74e2',
        'created_date': '2020-05-28T00:00:00+00:00',
        'updated_date': '2020-05-28T00:00:00+00:00',
        'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
        }

def test_get_inexistent_device_id(client):
    # async def run(Asyclient):
    res = client.get("/device/47690661-f343-4491-920c-50dcd59f75e1")
    print(res.status_code)
    assert res.status_code == 404
    assert res.json() == {'detail': 'device not found'}