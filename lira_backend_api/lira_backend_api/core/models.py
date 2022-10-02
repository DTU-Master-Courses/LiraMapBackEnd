from lira_backend_api.database.db import Base

from sqlalchemy import INTEGER, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, BOOLEAN


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

class Device(Base):
    __tablename__ = "Devices"

    id = Column("DeviceId", UUID, primary_key=True, nullable=False)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)
    fk_sourcetype =  Column("FK_SourceType", UUID, nullable=False)

    class Config:
        orm_mode = True

class Trip(Base):
    __tablename__ = "Trips"

    id = Column("TripId", UUID, primary_key=True, nullable=False)
    task_id = Column("TaskId", INTEGER, nullable=False)
    start_time_utc = Column("StartTimeUtc", DateTime(timezone=True))
    end_time_utc = Column("EndTimeUtc", DateTime(timezone=True))
    star_position_lat = Column("StartPositionLat", Text)
    start_position_lng = Column("StartPositionLng", Text)
    start_position_display = Column("StartPositionDisplay", Text)
    end_position_lat = Column("EndPositionLat", Text)
    end_position_lng = Column("EndPositionLng", Text)
    end_position_display = Column("EndPositionDisplay", Text)
    duration = Column("Duration", DateTime(timezone=True))
    distance_km = Column("DistanceKm", DOUBLE_PRECISION)
    fk_device = Column("FK_Device", UUID, nullable=False)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)
    fully_imported = Column("Fully_Imported", BOOLEAN, nullable=False)
    fully_route_annotated = Column("Fully_RouteAnnotated", BOOLEAN)
    description = Column("Description", Text)
    change_log = Column("ChangeLog", Text)

    class Config:
        orm_mode = True

class SourceTypes(Base):
    __tablename__ = "SourceTypes"
    
    id = Column("SourceTypeId", UUID, primary_key=True, nullable=False)
    source_name = Column("SourceName", Text)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)
    
    class Config:
        orm_mode = True


