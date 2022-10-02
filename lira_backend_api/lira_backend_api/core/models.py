from lira_backend_api.database.db import Base

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID,DOUBLE_PRECISION,BOOLEAN


class MeasurementTypes(Base):
    __tablename__ = "MeasurementTypes"

    id = Column("MeasurementTypeId", UUID, primary_key=True, nullable=False)
    type = Column("type", Text)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True

class MeasurementModel(Base):
    __tablename__ = "Measurements"

    id = Column("MeasurementId", UUID, primary_key=True, nullable=False)
    timestamp = Column("TS_or_Distance", DateTime(timezone=True), nullable=False)
    tag = Column("T", Text, nullable=False) 
    lat = Column("lat", DOUBLE_PRECISION, nullable=False)
    lon = Column("lon", DOUBLE_PRECISION, nullable=False)
    message = Column("message", Text, nullable=False) 
    is_computed = Column("isComputed", BOOLEAN, nullable=False)
    fk_trip = Column("FK_Trip", UUID, nullable=False)#, ForeignKey("MeasurementTypes.id")
    fk_measurement_type = Column("FK_MeasurementType", UUID, nullable=False)#, ForeignKey("MeasurementTypes.id")
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True
