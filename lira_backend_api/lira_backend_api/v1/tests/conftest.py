import asyncio
from typing import Generator
import pytest
from fastapi.testclient import TestClient
import json
from lira_backend_api.main import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c