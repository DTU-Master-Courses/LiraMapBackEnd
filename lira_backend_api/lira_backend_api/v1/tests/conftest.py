import pytest
from starlette.testclient import TestClient
from lira_backend_api.__main__ import app
from httpx import AsyncClient


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def Asyclient():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
