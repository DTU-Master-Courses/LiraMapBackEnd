from typing import List

from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import MeasurementTypes, MeasurementModel, TripsReturn, Trip
from lira_backend_api.v1.routers.utils import get_measurementtype, get_measurementmodel, get_ride, get_trip, get_trips
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/measurement')

@router.get("/type/{measurement_type_id}", response_model=MeasurementTypes)
def get_measurement_type(measurement_type_id: str, db: Session = Depends(get_db)):
    result = get_measurementtype(measurement_type_id, db)

    return result

@router.get("/model/{measurement_model_id}", response_model=MeasurementModel)
def get_measurement_model(measurement_model_id: str, db: Session = Depends(get_db)):
    result = get_measurementmodel(measurement_model_id, db)

    return result

@router.get("/ride", response_model=TripsReturn)
def get_single_ride(trip_id: str, tag: str, db: Session = Depends(get_db)):
    result = get_ride(trip_id,tag, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag does not contain values")
    else:
        return result


# @router.get("/trips")
# def get_trips(db: Session = Depends(get_db)):
#     results = get_trips(db)

#     return results

