from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from databases.core import Connection


from lira_backend_api.core.schemas import (
    MeasurementTypes,
    MeasurementModel,
    TripsReturn,
    Acceleration,
)
from lira_backend_api.v1.routers.utils import (
    get_measurementtype,
    get_ride,
    measurement_types,
)
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/measurement")


# KT: Should be migrated over
@router.get("/types", response_model=List[MeasurementTypes])
async def get_measurement_types(db: Connection = Depends(get_connection)):
    results = await measurement_types(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something went wrong")

    results_modified = list()

    for result in results:
        result_dict = dict(result._mapping.items())
        results_modified.append(MeasurementTypes(*result_dict.values()))

    return results_modified


# KT: Should be migrated over
@router.get("/type/{measurement_type_id}", response_model=MeasurementTypes)
async def get_measurement_type(
    measurement_type_id: str, db: Connection = Depends(get_connection)
):
    result = await get_measurementtype(measurement_type_id, db)

    result_dict = dict(result._mapping.items())

    return MeasurementTypes(*result_dict.values())


# KT: Exception to the usual paradigm we want to follow.
@router.get("/ride", response_model=TripsReturn)
async def get_single_ride(
    trip_id: str, tag: str, db: Connection = Depends(get_connection)
):
    result = await get_ride(trip_id, tag, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag does not contain values")

    return result
