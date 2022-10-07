from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import Device
from lira_backend_api.v1.routers.utils import get_deviceid
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/device')

@router.get("/{device_id}", response_model=Device)
def get_device_id(device_id: str, db: Session = Depends(get_db)):
    result = get_deviceid(device_id, db)

    return result

