from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import  DRDMeasurement
from lira_backend_api.v1.endpoints.crud import get_DRDmeasurement
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/drdmeasurement')

@router.get("/id/{DRDmeasurement_id}", response_model=DRDMeasurement)
def get_DRDmeasurement_model(DRDmeasurement_id: str, db: Session = Depends(get_db)):
    result = get_DRDmeasurement(DRDmeasurement_id, db)

    return result