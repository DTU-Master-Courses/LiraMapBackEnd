from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import Trip
from lira_backend_api.v1.endpoints.crud import get_trip
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/trip')

@router.get("/id/{trip_id}", response_model=Trip)
def get_single_trip(trip_id: str, db: Session = Depends(get_db)):
    result = get_trip(trip_id, db)

    return result