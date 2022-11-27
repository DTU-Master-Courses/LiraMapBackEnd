import asyncio
from typing import Generator
import pytest
from fastapi.testclient import TestClient
import json
from lira_backend_api.__main__ import app
from lira_backend_api.v1.tests.conftest import *


@pytest.mark.anyio
def test_get_single_source():
    async def run_test(client):
        res = client.get("/sourcetype/id/8b195100-3c87-4912-a315-3fe2b9c32e1a")
        print  (res.json())
        print (res.status_code)
        assert res.status_code == 200
