from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from databases.core import Connection
#from lira_backend_api.v1.routers.utils import get_current_acceleration
from sqlalchemy.orm import Session


from lira_backend_api.core.schemas import (
    MeasurementTypes,
    MeasurementModel,
    TripsReturn,
    Acceleration
)
from lira_backend_api.v1.routers.utils import (
    get_measurementtype,
    get_measurementmodel,
    get_ride,
    get_current_acceleration,
    measurement_types,
)
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/measurement")


@router.get("/types", response_model=List[MeasurementTypes])
def get_measurement_types(db: Session = Depends(get_db)):
    results = measurement_types(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return results


@router.get("/type/{measurement_type_id}", response_model=MeasurementTypes)
async def get_measurement_type(measurement_type_id: str, db: Connection = Depends(get_connection)):
    result = await get_measurementtype(measurement_type_id, db)

    # res_schema = MeasurementTypes(id=result._mapping["id"], created_date=result._mapping["created_date"], type=result._mapping["type"])

    return MeasurementTypes(id=result.id, created_date=result.created_date, type=result.type)


@router.get("/model/{measurement_model_id}", response_model=MeasurementModel)
async def get_measurement_model(measurement_model_id: str, db: Connection = Depends(get_connection)):
    result = await get_measurementmodel(measurement_model_id, db)

    return MeasurementModel(id=result.id, timestamp=result.timestamp, tag=result.tag, lat=result.lat,
    lon=result.lon, message=result.message, is_computed=result.is_computed, fk_trip=result.fk_trip, 
    fk_measurement_type=result.fk_measurement_type, created_date=result.created_date, updated_date=result.updated_date)


@router.get("/ride", response_model=TripsReturn)
async def get_single_ride(trip_id: str, tag: str, db: Connection = Depends(get_connection)):
    result = await get_ride(trip_id, tag, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag does not contain values")
    else:
        return result

@router.get("/acceleration/{trip_id}", response_model=Acceleration)
async def get_acceleration_trip(trip_id: UUID, db: Connection = Depends(get_connection)):
    results = await get_current_acceleration(str(trip_id), db)
    if results is None:
        raise HTTPException(status_code=404, detail="Trip does not contain acceleration data")
    else:
        return results


# @router.get("/trips")
# def get_trips(db: Session = Depends(get_db)):
#     results = get_trips(db)

#     return results
