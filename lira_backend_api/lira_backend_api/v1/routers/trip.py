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
    Variables,
    MeasurementLatLon,
    Power,
    SpeedList,
    SpeedVariables,
    SpeedVariablesAgg
    Energy,
)
from lira_backend_api.v1.routers.utils import (
    get_trip,
    get_trips,
    get_variable_list,
    get_segments,
    get_power,
    get_speed_list,
    get_speed_list_agg
    get_energy,
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


@router.get("/list_of_variables/{trip_id}", response_model=Variables)
async def get_variables(trip_id, db: Connection = Depends(get_connection)):
    results = await get_variable_list(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    results_modified = list()

@router.get("/list_of_speed/{trip_id}", response_model=List[SpeedVariables])
def get_speed(trip_id, db: Session = Depends(get_db)):
    results = get_speed_list(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    else:
        return results

@router.get("/list_of_speed_agg/{trip_id}", response_model=List[SpeedVariablesAgg])
def get_speed(trip_id, db: Session = Depends(get_db)):
    results = get_speed_list_agg(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    else:
        return results



@router.get("/energy/{trip_id}", response_model=Energy)
async def get_energy_trip(trip_id, db: Connection = Depends(get_connection)):
    results = await get_energy(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain data"
        )
    else:
        return results


# TODO: The following function is an awful hack, but don't have time to properly implement for Release 1, circle back to Release 2
@router.get("/segments/{trip_id}", response_model=List[MeasurementLatLon])
def get_trip_segments(trip_id, db: Session = Depends(get_db)):
    results = get_segments(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain required data"
        )

    results_list = list()
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
