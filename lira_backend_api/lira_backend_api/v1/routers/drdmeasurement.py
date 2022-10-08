from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import DRDMeasurement
from lira_backend_api.v1.routers.utils import get_DRDmeasurement
from lira_backend_api.database.db import get_db

router = APIRouter(prefix="/drdmeasurement")


@router.get("/id/{drdmeasurement_id}", response_model=DRDMeasurement)
def get_DRDmeasurement_model(drdmeasurement_id: str, db: Session = Depends(get_db)):
    result = get_DRDmeasurement(drdmeasurement_id, db)

    return result
