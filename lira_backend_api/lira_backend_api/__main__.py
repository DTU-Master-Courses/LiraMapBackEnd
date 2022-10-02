from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import uvicorn

from lira_backend_api.core.schemas import MeasurementTypes,MeasurementModel,Device
from lira_backend_api.database.db import get_db
from lira_backend_api.v1.endpoints.crud import get_measurementtype,get_measurementmodel,get_deviceid
from lira_backend_api.settings import settings

from lira_backend_api.v1.routers import measurements, trip, device, sourceTypes


app = FastAPI()
app.include_router(measurements.router)
app.include_router(trip.router)
app.include_router(device.router)
app.include_router(sourceTypes.router)
# TODO: We need to change the origins of this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        app,
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
