from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import SourceTypes
from lira_backend_api.v1.routers.utils import get_sourcetype
from lira_backend_api.database.db import get_db

router = APIRouter(prefix='/sourcetype')

@router.get("/id/{trip_id}", response_model=SourceTypes)
def get_single_source(source_id: str, db: Session = Depends(get_db)):
    result = get_sourcetype(source_id, db)

    return result