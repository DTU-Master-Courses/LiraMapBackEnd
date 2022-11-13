import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lira_backend_api.v1.routers import (
    drdmeasurement,
    measurement,
    sourcetype,
    trip,
    device,
    mapreference,
)
from lira_backend_api.settings import settings
from lira_backend_api.database.db import lira_database, setup_db

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

app = FastAPI()
app.include_router(measurement.router)
app.include_router(trip.router)
app.include_router(drdmeasurement.router)
app.include_router(device.router)
app.include_router(sourcetype.router)
app.include_router(mapreference.router)
add_pagination(app)


# TODO: We need to change the origins of this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await lira_database.connect()
    await setup_db()
    # TODO: We need to do the same for Altitude Database


@app.on_event("shutdown")
async def shutdown():
    await lira_database.disconnect()
    # TODO: We need to do the same for Altitude Database


if __name__ == "__main__":
    uvicorn.run(
        app,
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
