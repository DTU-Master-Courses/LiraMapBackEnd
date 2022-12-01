# Main Dev: HUIYULEO
# Supporting Devs: wangrandk

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# test endpoint /measurement/types
async def test_get_all_measurement_type(async_client: AsyncClient) -> None:
    url= "/measurement/types"
    res = await async_client.get(url=url)
    assert res.status_code == 200
    assert res.json() != None

