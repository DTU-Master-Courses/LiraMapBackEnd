from lira_backend_api.database.db import Base

from sqlalchemy import INTEGER, Column, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, DOUBLE_PRECISION, BOOLEAN, BIGINT


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
    tag = Column("T", Text, nullable=True)
    lat = Column("lat", DOUBLE_PRECISION, nullable=True)
    lon = Column("lon", DOUBLE_PRECISION, nullable=True)
    message = Column("message", Text, nullable=True)
    is_computed = Column("isComputed", BOOLEAN, nullable=False)
    fk_trip = Column("FK_Trip", UUID, ForeignKey("Trips.TripId"), nullable=False)
    fk_measurement_type = Column("FK_MeasurementType", UUID, nullable=False)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=True)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True


class Device(Base):
    __tablename__ = "Devices"

    id = Column("DeviceId", UUID, primary_key=True, nullable=False)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)
    fk_sourcetype = Column("FK_SourceType", UUID, nullable=False)

    class Config:
        orm_mode = True


class Trip(Base):
    __tablename__ = "Trips"

    id = Column("TripId", UUID, primary_key=True, nullable=False)
    task_id = Column("TaskId", INTEGER, nullable=False)
    start_time_utc = Column("StartTimeUtc", DateTime(timezone=True))
    end_time_utc = Column("EndTimeUtc", DateTime(timezone=True))
    start_position_lat = Column("StartPositionLat", Text)
    start_position_lng = Column("StartPositionLng", Text)
    start_position_display = Column("StartPositionDisplay", Text)
    end_position_lat = Column("EndPositionLat", Text)
    end_position_lng = Column("EndPositionLng", Text)
    end_position_display = Column("EndPositionDisplay", Text)
    duration = Column("Duration", DateTime(timezone=True))
    distance_km = Column("DistanceKm", DOUBLE_PRECISION)
    fk_device = Column(
        "FK_Device", UUID, ForeignKey("Devices.DeviceId"), nullable=False
    )
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)
    fully_imported = Column("Fully_Imported", BOOLEAN, nullable=False)
    # fully_route_annotated = Column("Fully_RouteAnnotated", BOOLEAN, nullable=True)
    # description = Column("Description", Text, nullable=True)
    # change_log = Column("ChangeLog", Text, nullable=True)

    class Config:
        orm_mode = True


class SourceType(Base):
    __tablename__ = "SourceTypes"

    id = Column("SourceTypeId", UUID, primary_key=True, nullable=False)
    source_name = Column("SourceName", Text)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True


class DRDMeasurement(Base):
    __tablename__ = "DRDMeasurements"

    id = Column("DRDMeasurementId", UUID, primary_key=True, nullable=False)
    distance = Column("TS_or_Distance", Text)
    tag = Column("T", Text)
    lat = Column("lat", DOUBLE_PRECISION)
    lon = Column("lon", DOUBLE_PRECISION)
    message = Column("message", Text)
    is_computed = Column("isComputed", BOOLEAN, nullable=False)
    fk_trip = Column("FK_Trip", UUID, nullable=False)
    fk_measurement_type = Column("FK_MeasurementType", UUID, nullable=False)
    created_date = Column("Created_Date", DateTime(timezone=True), nullable=False)
    updated_date = Column("Updated_Date", DateTime(timezone=True), nullable=False)

    class Config:
        orm_mode = True


class MapReference(Base):
    __tablename__ = "MapReferences"

    id = Column("MapReferenceId", UUID, primary_key=True, nullable=False)
    lat_map_matched = Column("lat_MapMatched", DOUBLE_PRECISION)
    lon_map_matched = Column("lon_MapMatched", DOUBLE_PRECISION)
    way_point_name = Column("wayPointName", Text)
    leg_summary_map_matched = Column("legSummary_MapMatched", Text)
    leg_distance_map_matched = Column("legDistance_MapMatched", DOUBLE_PRECISION)
    node_id_map_matched = Column("nodeId_MapMatched", Text)
    offset = Column("offset", Text)
    lane = Column("lane", Text)
    direction = Column("direction", Text)
    possible_matching_routes = Column("PossibleMatchingRoutes", Text)
    way_point = Column("WayPoint", Text)
    fk_measurement_id = Column("FK_MeasurementId", UUID, nullable=False)
    fk_osmwaypointid = Column("FK_OSMWayPointId", BIGINT)

    class Config:
        orm_mode = True
