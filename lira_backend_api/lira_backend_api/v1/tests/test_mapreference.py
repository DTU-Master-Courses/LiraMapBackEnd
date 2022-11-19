import asyncio
from typing import Generator
import pytest
from fastapi.testclient import TestClient
import json
from lira_backend_api.main import app
from lira_backend_api.v1.tests.conftest import *



        
@pytest.mark.anyio
def test_get_mapreference_id():
    async def run_test(client):
        res = client.get("/mapreference/id/00001108-c4c5-4e42-acff-73f6ecf6a31c")
        assert res.status_code == 200
        print  (res.json())
        print(res.status_code)
        print  (res.json()['id'])
        assert res.json()['id'] == "00001108-c4c5-4e42-acff-73f6ecf6a31c"
        assert res.json()['fk_measurement_id'] =='b2209dbc-1759-4107-84a9-abdbdc71196f'

# given a false id, expecting a 404 error. 
def test_get_inexistent_mapreference_id():
    async def run_test(client):
        res = client.get("/mapreference/id/12345678-1234-5678-1234-567812345678")
        assert res.status_code == 404
        print  (res.json())
        assert res.json() == {'detail': 'mapreference not found'}
    
    
    
   