from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

from databases.core import Connection
from lira_backend_api.database.db import get_connection
from lira_backend_api.core.schemas import (
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


@router.get("/id/{trip_id}", response_model=Trip)
async def get_single_trip(trip_id: UUID, db: Connection = Depends(get_connection)):
    result = await get_trip(str(trip_id), db)
    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    else:
        return Trip(id=result.id, task_id=result.task_id, start_time_utc=result.start_time_utc,
        end_time_utc=result.end_time_utc, start_position_lat=result.start_position_lat, 
        start_position_lng=result.start_position_lng, start_position_display=result.start_position_display, 
        end_position_display=result.end_position_display, end_position_lat=result.end_position_display, 
        end_position_lng=result.end_position_display, duration=result.duration, distance_km=result.distance_km, 
        fk_device=result.fk_device, created_date=result.created_date, updated_date=result.updated_date, 
        fully_imported=result.fully_imported)

@router.get("", response_model=List[Trip])
def get_all_trips(db: Connection = Depends(get_connection)):
    results = get_trips(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something unexpected happened")

    return results


@router.get("/acceleration/{trip_id}", response_model=Acceleration)
async def get_acceleration_trip(trip_id, db: Connection = Depends(get_connection)):
    results = await get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    else:
        return results


# TODO: The following function is an awful hack, but don't have time to properly implement for Release 1, circle back to Release 2
@router.get("/segments/{trip_id}", response_model=List[MeasurementLatLon])
def get_trip_segments(trip_id, db: Connection = Depends(get_connection)):
    results = get_segments(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )

    results_list = list()
    for result in results:
        results_list.append(MeasurementLatLon(lat=result[0], lon=result[1]))
    return results_list
