from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from databases.core import Connection
from lira_backend_api.v1.routers.utils import get_current_acceleration

from lira_backend_api.core.schemas import (
    Acceleration,
    MeasurementTypes,
    MeasurementModel,
    TripsReturn,
    Trip,
)
from lira_backend_api.v1.routers.utils import (
    get_measurementtype,
    get_measurementmodel,
    get_ride,
    get_trip,
    get_trips,
)
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/measurement")


@router.get("/type/{measurement_type_id}", response_model=MeasurementTypes)
async def get_measurement_type(measurement_type_id: str, db: Connection = Depends(get_connection)):
    result = await get_measurementtype(measurement_type_id, db)

    return result


@router.get("/model/{measurement_model_id}", response_model=MeasurementModel)
def get_measurement_model(measurement_model_id: str, db: Connection = Depends(get_connection)):
    result = get_measurementmodel(measurement_model_id, db)

    return result


@router.get("/ride", response_model=TripsReturn)
def get_single_ride(trip_id: str, tag: str, db: Connection = Depends(get_connection)):
    result = get_ride(trip_id, tag, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag does not contain values")
    else:
        return result

@router.get("/acceleration/{trip_id}", response_model=Acceleration)
def get_acceleration_trip(trip_id, db: Connection = Depends(get_connection)):
    results = get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain acceleration data")
    else:
        return results


# @router.get("/trips")
# def get_trips(db: Session = Depends(get_db)):
#     results = get_trips(db)

#     return results
