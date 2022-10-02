from typing import Union
from pydantic import BaseModel, Field


from datetime import datetime

from sqlalchemy import BigInteger


class MeasurementTypes(BaseModel):
    id: str
    type: str
    created_date: datetime

    class Config:
        orm_mode = True

class MeasurementModel(BaseModel):
    """
    Measurement model.
    It returned when accessing measurements models from the API.
    """
    id: str
    timestamp: datetime
    tag: Union[str,None]
    lat: Union[float,None]
    lon: Union[float,None]
    message: Union[str,None]
    is_computed: Union[bool,None]
    fk_trip: Union[str,None]
    fk_measurement_type: Union[str,None]
    created_date: Union[datetime,None]
    updated_date: Union[datetime,None]

class Device(BaseModel):
    id: str
    created_date: Union[datetime,None]
    updated_date: Union[datetime,None]
    fk_sourcetype: Union[str,None]

    class Config:
        orm_mode = True

class Trip(BaseModel):
    id: str
    taskId: int
    startTimeUtc: Union[datetime,None]
    endTimeUtc: Union[datetime,None]
    startPositionLat: Union[str,None]
    startPositionLng: Union[str,None]
    startPositionDisplay: Union[str,None]
    endPositionLat: Union[str,None]
    endPositionLng: Union[str,None]
    endPositionDisplay: Union[str,None]
    duration: Union[datetime,None]
    distanceKm: Union[float,None]
    fk_device: Union[str,None]
    created_Date: Union[datetime,None]
    updated_Date: Union[datetime,None]
    fully_Imported: Union[bool,None]
    fully_RouteAnnotated: Union[bool,None]
    description: Union[str,None]
    changeLog: Union[str,None]

    class Config:
        orm_mode = True

class SourceTypes(BaseModel):
    id: str
    sourceName: Union[str,None]
    created_Date: Union[datetime,None]
    updated_Date: Union[datetime,None]
    
    class Config:
        orm_mode = True