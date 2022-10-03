from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from lira_backend_api.settings import settings
from lira_backend_api.v1.routers import measurement, sourcetype, trip, DRDmeasurement, device, mapreference


app = FastAPI()
app.include_router(measurement.router)
app.include_router(trip.router)
app.include_router(DRDmeasurement.router)
app.include_router(device.router)
app.include_router(sourcetype.router)
app.include_router(mapreference.router)

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