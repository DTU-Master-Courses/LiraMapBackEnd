from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import SourceType
from lira_backend_api.v1.routers.utils import get_sourcetype
from lira_backend_api.database.db import get_db

router = APIRouter(prefix="/sourcetype")


@router.get("/id/{source_id}", response_model=SourceType)
def get_single_source(source_id: str, db: Session = Depends(get_db)):
    result = get_sourcetype(source_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="source not found")

    return result
