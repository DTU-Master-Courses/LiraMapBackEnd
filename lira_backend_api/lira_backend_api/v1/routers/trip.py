from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

from databases.core import Connection

from lira_backend_api.core.schemas import Trip, Acceleration
from lira_backend_api.v1.routers.utils import get_trip, get_trips, get_current_acceleration
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/trips")


@router.get("/id/{trip_id}", response_model=Trip)
async def get_single_trip(trip_id: str, db: Connection = Depends(get_connection)):
    result = await get_trip(trip_id, db)
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

    return results


@router.get("/acceleration/{trip_id}", response_model=Acceleration)
def get_acceleration_trip(trip_id, db: Connection = Depends(get_connection)):
    results = get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain acceleration data")
    else:
        return results

    
    
