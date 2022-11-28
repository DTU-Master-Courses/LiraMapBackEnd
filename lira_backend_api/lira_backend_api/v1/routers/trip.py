from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from databases.core import Connection
from lira_backend_api.database.db import get_connection
from lira_backend_api.core.schemas import (
    Trip,
    Trips,
    MeasurementLatLon,
    Energy,
    ClimbingForceList,
    Acceleration,
    AccelerationList,
    SpeedVariablesList,
    ContentRpmList,
    FrictionList,
    SpeedVariablesAggList,
    SegmentsList,
    RpmAggList,
)
from lira_backend_api.v1.routers.utils import (
    get_trip,
    get_trips,
    get_variable_list,
    get_segments,
    get_speed_list,
    get_energy,
    get_rpm_LR,
    get_rpm_list,
    get_trip_friction,
    get_speed_list_agg,
    get_climbingforce,
)

router = APIRouter(prefix="/trips")


@router.get("/id/{trip_id}", response_model=Trip)
async def get_single_trip(trip_id: UUID, db: Connection = Depends(get_connection)):
    result = await get_trip(str(trip_id), db)
    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip_result = dict(result._mapping.items())

    trip_response = Trip(*trip_result.values())

    return trip_response


@router.get("", response_model=Trips)
async def get_all_trips(db: Connection = Depends(get_connection)):
    results = await get_trips(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something unexpected happened")

    return {"trips": results}


@router.get("/speed_aggregation/{trip_id}", response_model=SpeedVariablesAggList)
async def get_speed_agg(trip_id, db: Connection = Depends(get_connection)):
    results = await get_speed_list_agg(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain speed data")

    return {"speed_aggregation": results}


@router.get("/climbing_force/{trip_id}", response_model=ClimbingForceList)
async def get_sget_climbingforce_trip(
    trip_id, db: Connection = Depends(get_connection)
):
    results = await get_climbingforce(str(trip_id), db)
    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain speed data")

    return {"climbing_force": results}


# FIXME: rename endpoint for clarity ("list of variables" could be lots of things)
@router.get("/acceleration/{trip_id}", response_model=AccelerationList)
async def get_variables(trip_id, db: Connection = Depends(get_connection)):
    results = await get_variable_list(str(trip_id), db)

    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )

    return {"acceleration": results}


@router.get("/speed/{trip_id}", response_model=SpeedVariablesList)
async def get_speed(trip_id, db: Connection = Depends(get_connection)):
    results = await get_speed_list(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain speed data")

    return {"speed": results}


@router.get("/energy/{trip_id}", response_model=Energy)
async def get_energy_trip(trip_id, db: Connection = Depends(get_connection)):
    results = await get_energy(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain data")

    return { "energy": results}


@router.get("/segments/{trip_id}", response_model=SegmentsList)
async def get_trip_segments(trip_id, db: Connection = Depends(get_connection)):
    results = await get_segments(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain required data"
        )

    lat_lon_collection_all = list()
    results_list = list()

    for result in results:
        lat_lon_collection_all.append(
            tuple([result._mapping.get("lat"), result._mapping.get("lon")])
        )

    for i in range(len(lat_lon_collection_all)):
        if i % 10 == 0:
            results_list.append(
                MeasurementLatLon(
                    lat_lon_collection_all[i][0], lat_lon_collection_all[i][1]
                )
            )

    return {"segments": results_list}


@router.get("/rpm/{trip_id}", response_model=ContentRpmList)
async def get_all_rpm(trip_id, db: Connection = Depends(get_connection)):
    results = await get_rpm_list(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain speed data")

    return {"content_rpm": results}


@router.get("/rpm_aggregation/{trip_id}", response_model=RpmAggList)
async def get_rpm_aggr(trip_id, db: Connection = Depends(get_connection)):
    results = await get_rpm_LR(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain speed data")

    return {"rpm_aggregation": results}


@router.get("/friction/{trip_id}", response_model=FrictionList)
async def get_friction_trip(trip_id, db: Connection = Depends(get_connection)):
    results = await get_trip_friction(str(trip_id), db)

    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain data")

    return {"friction": results}
