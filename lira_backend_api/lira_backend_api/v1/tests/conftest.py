import asyncio
from typing import Generator
import pytest
from starlette.testclient import TestClient
import json
from lira_backend_api.__main__ import app
from httpx import AsyncClient


# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'

# @pytest.fixture(scope='session')
# def event_loop() -> Generator:
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
async def Asyclient():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
