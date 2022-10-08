from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lira_backend_api.core.schemas import  MapReference
from lira_backend_api.v1.routers.utils import get_mapreference
from lira_backend_api.database.db import get_db

router = APIRouter(prefix="/mapreference")


@router.get("/id/{mapreference_id}", response_model=MapReference)
def get_mapreference_id(mapreference_id: str, db: Session = Depends(get_db)):
    result = get_mapreference(mapreference_id, db)

    return result
