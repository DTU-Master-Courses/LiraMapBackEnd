from typing import Union
from pydantic import BaseModel, Field


from datetime import datetime


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

    class Config:
        orm_mode = True

