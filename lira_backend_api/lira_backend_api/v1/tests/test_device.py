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

from lira_backend_api.main import app
# router = APIRouter(prefix="/device")
# client = TestClient(app)

# @router.get("/{device_id}", response_model=Device)
# def get_device_id(device_id: str, db: Session = Depends(get_db)):
#     result = get_deviceid(device_id, db)
#     return result
# testing sample from device table row No.4
# "DeviceId"	"Created_Date"	"Updated_Date"	"FK_SourceType"
# "47690661-f343-4591-920c-50dcd59f74e2"	"2020-05-28 00:00:00+00"	"2020-05-28 00:00:00+00"	"fb64715d-09d1-4fd9-8912-685364c7d446"
# 0cb38d9f-3601-4179-b5ef-403a999c9021


@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.mark.anyio
# async def test_get_device_id(async_client: AsyncClient):
async def test_get_device_id(client):
    # async with AsyncClient(app=app, base_url="http://localhost") as ac:
    # with TestClient(app) as async_client:
    response = client.get("/device/47690661-f343-4591-920c-50dcd59f74e2")
    assert response.status_code == 200
    assert response.json() == {
        'id': '47690661-f343-4591-920c-50dcd59f74e2',
        'created_date': '2020-05-28T00:00:00+00:00',
        'updated_date': '2020-05-28T00:00:00+00:00',
        'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
        }
    # res = client.get("/device/47690661-f343-4591-920c-50dcd59f74e2")
    # assert res.status_code == 200
    # print(res.status_code)
    # print  (res.json())
    # assert res.json() == {
    #     'id': '47690661-f343-4591-920c-50dcd59f74e2',
    #     'created_date': '2020-05-28T00:00:00+00:00',
    #     'updated_date': '2020-05-28T00:00:00+00:00',
    #     'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
    #     }

# given a false id, expecting a 404 error.
@pytest.mark.anyio
async def test_get_inexistent_device_id(client):
    res = client.get("/device/47690661-f343-4591-920c-50dcd59f74e1")
    assert res.status_code == 404
    assert res.json() == {'detail': 'device not found'}
