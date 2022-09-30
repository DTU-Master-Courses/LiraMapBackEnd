from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import uvicorn

from lira_backend_api.core.schemas import MeasurementTypes
from lira_backend_api.database.db import get_db
from lira_backend_api.v1.endpoints.crud import get_measurementtype
from lira_backend_api.settings import settings


app = FastAPI()
# TODO: We need to change the origins of this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{measurement_type_id}", response_model=MeasurementTypes)
def root(measurement_type_id: str, db: Session = Depends(get_db)):
    result = get_measurementtype(measurement_type_id, db)

    return result


if __name__ == "__main__":
    uvicorn.run(
        app,
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
