# Main Dev: Tswagerman
# Supporting Devs: Mikfor, wangrandk, HUIYULEO, ViktorRindom, PossibleNPC
from fastapi import APIRouter, Depends,HTTPException

from databases.core import Connection

from lira_backend_api.core.schemas import DRDMeasurement
from lira_backend_api.v1.routers.utils import get_drdmeasurement
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/drdmeasurement")


@router.get("/id/{drdmeasurement_id}", response_model=DRDMeasurement)
async def get_DRDmeasurement_model(
    drdmeasurement_id: str, db: Connection = Depends(get_connection)
):
    result = await get_drdmeasurement(drdmeasurement_id, db)

    if result is None:
            raise HTTPException(status_code=404, detail="drdmeasurement not found")
    result_dict = dict(result._mapping.items())

    return DRDMeasurement(*result_dict.values())
