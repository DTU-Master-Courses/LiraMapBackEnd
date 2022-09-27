# from typing import Text
from lira_backend_api.database.db import Base

from sqlalchemy import MetaData, Table, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

# metadata_obj = MetaData()

class MeasurementTypes(Base):
    __tablename__ = "MeasurementTypes"

    # id: str
    # type: str
    # created_date: str

    id = Column("MeasurementTypeId", UUID, primary_key=True, nullable=False)
    type = Column("type", Text)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True