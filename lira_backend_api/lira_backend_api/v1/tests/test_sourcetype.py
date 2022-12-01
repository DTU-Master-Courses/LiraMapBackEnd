# Main Dev: HUIYULEO
# Supporting Devs: wangrandk
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_single_source(async_client: AsyncClient) -> None:
    url= "/sourcetype/id"
    params = {"source_id":"8b195100-3c87-4912-a315-3fe2b9c32e1a"}
    response = await async_client.get(url=url, params = params)

    assert response.status_code == 200
    assert response.json() != None

async def test_get_inexistent_single_source(async_client: AsyncClient) -> None:
    url= "/sourcetype/id"
    params = {"source_id":"8b195100-3c87-4912-a333-3fe2b9c32e1a"}
    response = await async_client.get(url=url, params = params)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Source Type not found'}
