import asyncio
from typing import Generator
import pytest
from fastapi.testclient import TestClient
import json
from lira_backend_api.main import app
from lira_backend_api.v1.tests.conftest import *


@pytest.mark.anyio
def test_get_all_measurement_type(client):
    async def run_test(client):
        res = client.get("/measurement/types")
        print  (len(res.json()))
        assert res.status_code == 200


def test_get_single_measurement_type():
    async def run_test(client):
        expert = {
                "id": "218a5f9c-a54d-4ea1-b015-64930dbe0883",
                "type": "acc.xyz",
                "created_date": "0001-01-01T00:00:00+00:00"
                }
        url = "/measurement/type/218a5f9c-a54d-4ea1-b015-64930dbe0883"
        res = client.get(url=url)
        assert res.status_code == 200
        # print  (res.json())
        # print(res.status_code)
        # print  (res.json()['id'])
        assert res.json()['id'] == "218a5f9c-a54d-4ea1-b015-64930dbe0883"
        assert res.json() == expert

def test_get_single_measurement_model():
    async def run_test(client):
        url="/measurement/model/000002b1-795a-44ad-b7fb-8bfc4999aacb"
        res = client.get(url=url)
        print  (len(res.json()))
        assert res.status_code == 200

def test_get_ride():
    async def run_test(client):
        params = {"trip_id": "2857262b-71db-49df-8db6-a042987bf0eb", "tag": "obd.rpm"}
        res = client.get("/measurement/ride",params = params)
        print  (len(res.json()))
        assert res.status_code == 200
        assert res.json()["path"] != None