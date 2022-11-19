# from fastapi import APIRouter, Depends,Header, HTTPException
# from sqlalchemy.orm import Session
import asyncio
from typing import Generator

import pytest
# from lira_backend_api.core.schemas import Device
# from lira_backend_api.v1.routers.utils import get_deviceid
# from lira_backend_api.database.db import get_db
from fastapi.testclient import TestClient

import json
from lira_backend_api.v1.tests.conftest import *
from lira_backend_api.main import app

# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'

# @pytest.fixture(scope="session")
# def event_loop() -> Generator:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture
# def client():
#     with TestClient(app) as c:
#         yield c


@pytest.mark.anyio
def test_get_device_id():
    async def run(client):
        response = client.get("/device/47690661-f343-4591-920c-50dcd59f74e2")
        assert response.status_code == 200
        assert response.json() == {
            'id': '47690661-f343-4591-920c-50dcd59f74e2',
            'created_date': '2020-05-28T00:00:00+00:00',
            'updated_date': '2020-05-28T00:00:00+00:00',
            'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
            }

# given a false id, expecting a 404 error.
def test_get_inexistent_device_id():
    async def run(client):
        res = client.get("/device/47690661-f343-4591-920c-50dcd59f74e1")
        print(res.status_code)
        assert res.status_code == 404
        assert res.json() == {'detail': 'device not found'}

