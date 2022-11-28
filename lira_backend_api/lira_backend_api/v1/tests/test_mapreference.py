#test_mapreference main:@HUIYULEO s212648 

import pytest
import json
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# test mapreference url
async def test_get_mapreference_id(async_client: AsyncClient) -> None:
    mapference_id = "00001108-c4c5-4e42-acff-73f6ecf6a31c"
    url = "/mapreference/id/" + mapference_id
    res = await async_client.get(url=url)
    assert res.status_code == 200

    assert res.json()['id'] == "00001108-c4c5-4e42-acff-73f6ecf6a31c"
    assert res.json()['fk_measurement_id'] == 'b2209dbc-1759-4107-84a9-abdbdc71196f'


# given a false id, expecting a 404 error.
async def test_get_inexistent_mapreference_id(async_client: AsyncClient) -> None:
    w_mapference_id = "12345678-1234-5678-1234-567812345678"
    url = "/mapreference/id/" + w_mapference_id
    res = await async_client.get(url=url)
    assert res.status_code == 404
    assert res.json() == {'detail': 'No values for mapreference id'}



