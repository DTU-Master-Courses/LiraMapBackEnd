from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from databases.core import Connection
from lira_backend_api.database.db import get_connection
from lira_backend_api.core.schemas import (
    ContentAcceleration,
    MapReference,
    MeasurementLatLon,
    Trip,
    Acceleration,
    MeasurementLatLon,
)
from lira_backend_api.v1.routers.utils import (
    get_trip,
    get_trips,
    get_current_acceleration,
    get_segments,
)

router = APIRouter(prefix="/trips")


# KT: Migrated to new approach.
@router.get("/id/{trip_id}", response_model=Trip)
async def get_single_trip(trip_id: UUID, db: Connection = Depends(get_connection)):
    result = await get_trip(str(trip_id), db)
    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip_result = dict(result._mapping.items())

    trip_response = Trip(*trip_result.values())

    return trip_response


# KT: Migrated to new approach
@router.get("", response_model=List[Trip])
async def get_all_trips(db: Connection = Depends(get_connection)):
    results = await get_trips(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something unexpected happened")

    results_mod = list()

    for row in results:
        row_dict = dict(row._mapping.items())
        results_mod.append(Trip(*row_dict.values()))

    return results_mod


# TODO: This will result in a Front-End breaking change to the API
@router.get("/acceleration/{trip_id}", response_model=List[ContentAcceleration])
async def get_acceleration_trip(trip_id, db: Connection = Depends(get_connection)):
    results = await get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    results_modified = list()

    for result in results:
        results_modified.append(ContentAcceleration(*result.values()))

    return results_modified


# KT: This is migrated over
@router.get("/segments/{trip_id}", response_model=List[MeasurementLatLon])
async def get_trip_segments(trip_id, db: Connection = Depends(get_connection)):
    results = await get_segments(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
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
    return results_list
