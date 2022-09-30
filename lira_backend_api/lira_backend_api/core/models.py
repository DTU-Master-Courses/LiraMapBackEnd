from lira_backend_api.database.db import Base

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID


class MeasurementTypes(Base):
    __tablename__ = "MeasurementTypes"

    id = Column("MeasurementTypeId", UUID, primary_key=True, nullable=False)
    type = Column("type", Text)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True
