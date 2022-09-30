from pydantic import BaseModel, Field

from datetime import datetime


class MeasurementTypes(BaseModel):
    id: str
    type: str
    created_date: datetime

    class Config:
        orm_mode = True
