from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from datetime import datetime


class MeasurementTypesBase(BaseModel):
    pass


class MeasurementTypes(MeasurementTypesBase):
    id: str
    type: str
    created_date: datetime

    class Config:
        orm_mode = True
