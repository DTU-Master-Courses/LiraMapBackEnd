from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

from databases.core import Connection

from lira_backend_api.core.schemas import Trip, Acceleration
from lira_backend_api.v1.routers.utils import get_trip, get_trips, get_current_acceleration
from lira_backend_api.database.db import get_connection, get_db

router = APIRouter(prefix="/trips")


@router.get("/id/{trip_id}", response_model=Trip)
def get_single_trip(trip_id: UUID, db: Connection = Depends(get_connection)):
    result = get_trip(str(trip_id), db)

    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    return result


@router.get("", response_model=List[Trip])
def get_all_trips(db: Connection = Depends(get_connection)):
    results = get_trips(db)

    return results


@router.get("/acceleration/{trip_id}", response_model=Acceleration)
def get_acceleration_trip(trip_id, db: Session = Depends(get_db)):
    results = get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain acceleration data")
    else:
        return results

    
    
