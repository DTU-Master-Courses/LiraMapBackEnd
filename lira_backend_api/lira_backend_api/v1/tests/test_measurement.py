# test measurement

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_all_measurement_type(async_client: AsyncClient) -> None:
    url= "/measurement/types"
    res = await async_client.get(url=url)
    print  (len(res.json()))
    assert res.status_code == 200
    assert res.json() != None


# def test_get_single_measurement_type(client):
#     expert = {
#             "id": "218a5f9c-a54d-4ea1-b015-64930dbe0883",
#             "type": "acc.xyz",
#             "created_date": "0001-01-01T00:00:00+00:00"
#             }
#     url = "/measurement/type/218a5f9c-a54d-4ea1-b015-64930dbe0883"
#     res = client.get(url=url)
#     assert res.status_code == 200
#     # print  (res.json())
#     print(res.status_code)
#     # print  (res.json()['id'])
#     assert res.json()['id'] == "218a5f9c-a54d-4ea1-b015-64930dbe0883"
#     assert res.json() == expert

# def test1_get_single_measurement_model(client):
#     url="/measurement/model/000002b1-795a-44ad-b7fb-8bfc4999aacb"
#     res = client.get(url=url)
#     # print  (len(res.json()))
#     assert res.status_code == 200
#     # assert res.json() != None