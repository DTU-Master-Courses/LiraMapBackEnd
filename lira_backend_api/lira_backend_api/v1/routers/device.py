from fastapi import APIRouter, Depends,Header, HTTPException
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import Device
from lira_backend_api.v1.routers.utils import get_deviceid
from lira_backend_api.database.db import get_db

router = APIRouter(prefix="/device")
fake_secret_token = "coneofsilence"

@router.get("/{device_id}", response_model=Device)
def get_device_id(device_id: str, x_token: str = Header(), db: Session = Depends(get_db)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    
    result = get_deviceid(device_id, db)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return result
