from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import MeasurementTypes, MeasurementModel
from lira_backend_api.v1.endpoints.crud import get_measurementtype, get_measurementmodel
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