from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
from lira_backend_api.database.db import get_db

router = APIRouter(prefix="/trips")


@router.get("/{trip_id}", response_model=Trip)
def get_single_trip(trip_id: UUID, db: Session = Depends(get_db)):
    result = get_trip(str(trip_id), db)

    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return result


@router.get("", response_model=List[Trip])
def get_all_trips(db: Session = Depends(get_db)):
    results = get_trips(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something unexpected happened")

    return results


@router.get("/acceleration/{trip_id}", response_model=Acceleration)
def get_acceleration_trip(trip_id, db: Session = Depends(get_db)):
    results = get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )
    else:
        return results


# TODO: The following function is an awful hack, but don't have time to properly implement for Release 1, circle back to Release 2
@router.get("/segments/{trip_id}", response_model=List[MeasurementLatLon])
def get_trip_segments(trip_id, db: Session = Depends(get_db)):
    results = get_segments(str(trip_id), db)
    if results is None:
        raise HTTPException(
            status_code=404, detail="Trip does not contain acceleration data"
        )

    results_list = list()
    for result in results:
        results_list.append(MeasurementLatLon(lat=result[0], long=result[1]))
    return results_list
