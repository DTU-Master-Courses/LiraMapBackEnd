# Main Dev: PossibleNPC
# Supporting Devs: Tswagerman, Mikfor
from fastapi import APIRouter, Depends, HTTPException

from databases.core import Connection


from lira_backend_api.core.schemas import MeasurementTypes, MeasurementTypesList
from lira_backend_api.v1.routers.utils import (
    measurement_types,
)
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/measurement")


@router.get("/types", response_model=MeasurementTypesList)
async def get_measurement_types(db: Connection = Depends(get_connection)):
    results = await measurement_types(db)

    if results is None:
        raise HTTPException(status_code=500, detail="Something went wrong")

    results_modified = list()

    for result in results:
        result_dict = dict(result._mapping.items())
        results_modified.append(MeasurementTypes(*result_dict.values()))

    return {"measurement_types": results_modified}
