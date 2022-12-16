# Main Dev: HUIYULEO
# Supporting Devs: wangrandk
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_single_trip(async_client: AsyncClient) -> None:
    trip_id = "003a157f-786a-4430-b6c7-c48f6f968364"
    url = "/trips/id/" + trip_id
    res = await async_client.get(url=url)
    assert res.status_code == 200

    assert res.json()['id'] == "003a157f-786a-4430-b6c7-c48f6f968364"
    assert res.json() == {'id': '003a157f-786a-4430-b6c7-c48f6f968364', 'task_id': 4020,
                          'start_time_utc': '2020-08-01T15:52:10.053325+00:00',
                          'end_time_utc': '2020-08-01T15:55:35.991564+00:00', 'start_position_lat': '55.453020',
                          'start_position_lng': '11.207970',
                          'start_position_display': '{"city":"Stillinge Strand","house_number":"7","country":"Denmark","county":"Slagelse Municipality","suburb":null,"state":"Region Zealand","postcode":"4200","country_code":null,"road":null}',
                          'end_position_lat': '55.448430', 'end_position_lng': '11.210200',
                          'end_position_display': '{"city":"Stillinge Strand","house_number":"59","country":"Denmark","county":"Kalundborg Municipality","suburb":null,"state":"Region Zealand","postcode":"4200","country_code":null,"road":null}',
                          'duration': '2020-08-26T00:03:25.938239+00:00', 'distance_km': 0.642550058722749,
                          'fk_device': '187c70cc-4eff-4307-8157-ac0fa0102f43',
                          'created_date': '2020-08-26T11:45:20.290879+00:00',
                          'updated_date': '0001-01-01T00:00:00+00:00', 'fully_imported': True}

async def test_get_single_trip_tag(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/id/" + trip_id
    params = "tag=obd.rpm_fl"
    res = await async_client.get(url=url,params=params)
    data = res.json()
    assert res.status_code == 200
    assert (res.json()) != []
    assert data[0]['tag'] == "obd.rpm_fl"

# given a false id, expecting a 404 error.
async def test_get_inexistent_single_trip(async_client: AsyncClient) -> None:
    w_trip_id = "12345678-786a-4430-b6c7-c48f6f968364"
    url = "/trips/id/" + w_trip_id
    res = await async_client.get(url=url)
    assert res.status_code == 404

    assert res.json() == {'detail': 'Trip not found'}


async def test_get_all_trips(async_client: AsyncClient) -> None:
    res = await async_client.get("/trips")

    assert res.status_code == 200
    # we have set limit to 150 rows
    assert (res.json()) != []


async def test_get_trip_segments(async_client: AsyncClient) -> None:
    url = "/trips/segments/2857262b-71db-49df-8db6-a042987bf0eb"
    res = await async_client.get(url=url)
    assert res.status_code == 200
    assert (res.json()) != []


async def test_get_inexistent_trip_segments(async_client: AsyncClient) -> None:
    url = "/trips/segments/7e746b5e-1111-4c1b-1234-72f61fa858e6"
    res = await async_client.get(url=url)

    if (res.json() == [] and res.status_code == 200):
        res = {'detail': 'Trip does not contain required data'}
    assert res.status_code == 404


async def test_get_speed_agg(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/speed_aggregation/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []


async def test_get_inexistent_speed_agg(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/speed_aggregation/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_speed(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/speed/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_speed(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/speed/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_acceleration(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/acceleration/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_acceleration(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/acceleration/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_climbing_force(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/climbing_force/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_climbing_force(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/climbing_force/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404


async def test_get_energy(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/energy/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_energy(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/energy/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_rpm(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/rpm/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_rpm(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/rpm/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_rpm_agg(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/rpm_aggregation/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_rpm_agg(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/rpm_aggregation/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404

async def test_get_friction(async_client: AsyncClient) -> None:
    trip_id = "2857262b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/friction/" + trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 200
    assert (res.json()) != []

async def test_get_inexistent_friction(async_client: AsyncClient) -> None:
    w_trip_id = "1234562b-71db-49df-8db6-a042987bf0eb"
    url = "/trips/friction/" + w_trip_id
    res = await async_client.get(url=url)

    assert res.status_code == 404
