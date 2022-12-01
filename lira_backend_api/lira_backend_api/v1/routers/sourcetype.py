# Main Dev: Mikfor
# Supporting Devs: PossibleNPC
from fastapi import APIRouter, Depends, HTTPException

from databases.core import Connection

from lira_backend_api.core.schemas import SourceType
from lira_backend_api.v1.routers.utils import get_sourcetype
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/sourcetype")


@router.get("/id", response_model=SourceType)
async def get_single_source(source_id: str, db: Connection = Depends(get_connection)):
    result = await get_sourcetype(source_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="Source Type not found")

    return SourceType(
        id=result.id,
        source_name=result.source_name,
        created_date=result.created_date,
        updated_date=result.updated_date,
    )
