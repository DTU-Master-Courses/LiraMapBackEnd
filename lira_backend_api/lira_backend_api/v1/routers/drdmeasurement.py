from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

from databases.core import Connection

from lira_backend_api.core.schemas import DRDMeasurement
from lira_backend_api.v1.routers.utils import get_drdmeasurement
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/drdmeasurement")


@router.get("/id/{drdmeasurement_id}", response_model=DRDMeasurement)
async def get_DRDmeasurement_model(drdmeasurement_id: str, db: Connection = Depends(get_connection)):
    result = await get_drdmeasurement(drdmeasurement_id, db)

    return DRDMeasurement(id=result.id, distance=result.distance, tag=result.tag, lat=result.lat,
    lon=result.lon, message=result.message, is_computed=result.is_computed, fk_trip=result.fk_trip, 
    fk_measurement_type=result.fk_measurement_type, created_date=result.created_date, updated_date=result.updated_date)
