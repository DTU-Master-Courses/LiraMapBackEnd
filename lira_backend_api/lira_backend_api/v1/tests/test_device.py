import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_device_id(async_client: AsyncClient) -> None:
    dev_id = "47690661-f343-4591-920c-50dcd59f74e2"
    url = "/device/" + dev_id
    response = await async_client.get(url=url)

    assert response.status_code == 200
    assert response.json() == {
        'id': '47690661-f343-4591-920c-50dcd59f74e2',
        'created_date': '2020-05-28T00:00:00+00:00',
        'updated_date': '2020-05-28T00:00:00+00:00',
        'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
        }

async def test_get_inexistent_device_id(async_client: AsyncClient) -> None:
    # async def run(Asyclient):
    W_dev_id = "47690661-f343-4491-920c-50dcd59f75e1"
    url = "/device/" + W_dev_id
    response = await async_client.get(url=url)
    assert response.status_code == 404
    assert response.json() == {'detail': 'device not found'}