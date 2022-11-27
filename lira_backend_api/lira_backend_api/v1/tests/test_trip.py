import asyncio
from typing import Generator
import pytest
from fastapi.testclient import TestClient
import json
from lira_backend_api.__main__ import app
from lira_backend_api.v1.tests.conftest import *

@pytest.mark.anyio
def test_get_single_trip():
    async def run_test(client):
        res = client.get("/trips/id/003a157f-786a-4430-b6c7-c48f6f968364")
        assert res.status_code == 200
        print  (res.json())
        print(res.status_code)
        print  (res.json()['id'])
        assert res.json()['id'] == "003a157f-786a-4430-b6c7-c48f6f968364"
        assert res.json() == {'id': '003a157f-786a-4430-b6c7-c48f6f968364', 'task_id': 4020, 'start_time_utc': '2020-08-01T15:52:10.053325+00:00', 'end_time_utc': '2020-08-01T15:55:35.991564+00:00', 'start_position_lat': '55.453020', 'start_position_lng': '11.207970', 'start_position_display': '{"city":"Stillinge Strand","house_number":"7","country":"Denmark","county":"Slagelse Municipality","suburb":null,"state":"Region Zealand","postcode":"4200","country_code":null,"road":null}', 'end_position_lat': '55.448430', 'end_position_lng': '11.210200', 'end_position_display': '{"city":"Stillinge Strand","house_number":"59","country":"Denmark","county":"Kalundborg Municipality","suburb":null,"state":"Region Zealand","postcode":"4200","country_code":null,"road":null}', 'duration': '2020-08-26T00:03:25.938239+00:00', 'distance_km': 0.642550058722749, 'fk_device': '187c70cc-4eff-4307-8157-ac0fa0102f43', 'created_date': '2020-08-26T11:45:20.290879+00:00', 'updated_date': '0001-01-01T00:00:00+00:00', 'fully_imported': True}


# given a false id, expecting a 404 error.
def test_get_inexistent_single_trip():
    async def run_test(client):
        res = client.get("/trips/id/12345678-1234-5678-1234-567812345678")
        assert res.status_code == 404
        print  (res.json())
        assert res.json() == {'detail': 'Trip not found'}


def test_get_all_trips():
    async def run_test(client):
        res = client.get("/trips/")
        # print  (res.json()[0])
        # print  (res.json()[0].items())
        print  (len(res.json()))
        assert res.status_code == 200
        # we have set limit to 150 rows
        assert  (len(res.json())) == 150

def test_get_acceleration_trip():
    async def run_test(client):
        res = await client.get("/segments/acceleration/351c02c6-733e-4a4b-a0c1-e6cad55b931f")
        assert res.status_code == 200
        print  (res.json()['acceleration'][0])
        assert res.json()['acceleration'][0]== {'x': -0.15444444444444447, 'y': -0.2422222222222222, 'z': 1.0022222222222223, 'lon': 12.530856499999997, 'lat': 55.72094272222222, 'created_date': '2020-07-09T19:53:33'}


def test_get_inexistent_acceleration_trip():
    async def run_test(client):
        res = client.get("/segmaents/acceleration/d5684a99-de96-4476-aacc-133e15786df3")
        assert res.status_code == 404
        assert res.json() ==  {'detail': 'Not Found'}

# def test_get_trip_segments():
#     res = client.get("/segments/6193620e-4b97-4a9b-bca5-e0b73d216de6")

#     print  (res.json())
#     assert res.status_code == 200

def test_get_inexistent_trip_segments():
    async def run_test(client):
        res = client.get("/trips/segments/7e746b5e-0d7b-4c1b-9564-72f61fa858e6")
        print  (res.json())
        if  (res.json() == [] and res.status_code == 200):
            result = {'detail': 'Not Found'}
        assert result ==  {'detail': 'Not Found'}

def test_get_all_speed_agg():
    async def run_test(client):
        res = client.get("/trips/list_of_speed_agg/2857262b-71db-49df-8db6-a042987bf0eb")
        # print  (res.json()[0])
        # print  (res.json()[0].items())
        print  (len(res.json()))
        assert res.status_code == 200



