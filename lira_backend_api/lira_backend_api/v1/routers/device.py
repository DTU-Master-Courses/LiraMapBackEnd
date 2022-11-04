from fastapi import APIRouter, Depends, HTTPException

# from sqlalchemy.orm import Session

from databases.core import Connection

from lira_backend_api.core.schemas import Device
from lira_backend_api.v1.routers.utils import get_deviceid
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/device")


# KT: This is migrated
@router.get("/{device_id}", response_model=Device)
async def get_device_id(device_id: str, db: Connection = Depends(get_connection)):
    result = await get_deviceid(device_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="device not found")

    result_dict = dict(result._mapping.items())
    return Device(*result_dict.values())
