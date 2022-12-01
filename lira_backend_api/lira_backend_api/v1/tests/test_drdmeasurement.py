# Main Dev: HUIYULEO
# Supporting Devs: wangrandk, PossibleNPC
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# test DRDmeasurement_model
async def test_get_DRDmeasurement_model(async_client: AsyncClient) -> None:
    drd_id = "000000a5-07eb-4385-9fac-8a79b403f229"
    url = "drdmeasurement/id/" + drd_id
    res = await async_client.get(url=url)

    assert res.status_code == 200


async def test_get_inexisten_DRDmeasurement_model(async_client: AsyncClient) -> None:
    wdrd_id = "7017e64d-a58f-4362-9dc6-a7b07f3d6d99"
    url= "/drdmeasurement/id/" + wdrd_id
    res = await async_client.get(url=url)

    assert res.status_code == 404
