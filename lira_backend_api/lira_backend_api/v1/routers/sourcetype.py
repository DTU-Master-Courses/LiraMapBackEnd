from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
from databases.core import Connection

from lira_backend_api.core.schemas import SourceType
from lira_backend_api.v1.routers.utils import get_sourcetype
from lira_backend_api.database.db import get_connection

router = APIRouter(prefix="/sourcetype")


@router.get("/id/{trip_id}", response_model=SourceType)
def get_single_source(source_id: str, db: Connection = Depends(get_connection)):
    result = get_sourcetype(source_id, db)

    return result
