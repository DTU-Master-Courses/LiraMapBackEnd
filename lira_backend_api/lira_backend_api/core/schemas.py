from typing import Any, List, Union

from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import BigInteger
from collections import namedtuple


class MeasurementTypes(BaseModel):
    id: str
    type: str
    created_date: datetime

    class Config:
        orm_mode = True


class MeasurementModel(BaseModel):
    id: str
    timestamp: datetime
    tag: Union[str, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[str, None]
    fk_measurement_type: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


class Device(BaseModel):
    id: str
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    fk_sourcetype: Union[str, None]

    class Config:
        orm_mode = True


class Trip(BaseModel):
    id: str
    task_id: int
    start_time_utc: Union[datetime, None]
    end_time_utc: Union[datetime, None]
    start_position_lat: Union[str, None]
    start_position_lng: Union[str, None]
    start_position_display: Union[str, None]
    end_position_lat: Union[str, None]
    end_position_lng: Union[str, None]
    end_position_display: Union[str, None]
    duration: Union[datetime, None]
    distance_km: Union[float, None]
    fk_device: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    fully_imported: Union[bool, None]
    # fully_route_annotated: Union[bool, None]
    # description: Union[str, None]
    # change_log: Union[str, None]

    class Config:
        orm_mode = True


class SourceTypes(BaseModel):
    id: str
    source_name: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


class TripTest(BaseModel):
    trip_id: Union[str, None]
    lat: Union[float, None]
    lng: Union[float, None]
    value: Union[int, None]
    metadata: Any

    class Config:
        orm_mode = True


class DRDMeasurement(BaseModel):

    id: str
    distance: str
    tag: Union[str, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[str, None]
    fk_measurement_type: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


boundary = namedtuple("Boundary", ["minX", "maxX", "minY", "maxY"])


class TripsReturn(BaseModel):
    path: List[TripTest]
    bounds: boundary

    class Config:
        orm_mode = True


class MapReference(BaseModel):

    id: str
    lat_MapMatched: Union[float, None]
    lon_MapMatched: Union[float, None]
    way_point_name: Union[str, None]
    leg_summary_map_matched: Union[str, None]
    leg_distance_map_matched: Union[float, None]
    node_id_map_matched: Union[str, None]
    offset: Union[str, None]
    lane: Union[str, None]
    direction: Union[str, None]
    possible_matching_routes: Union[str, None]
    way_point: Union[str, None]
    fk_measurement_id: Union[str, None]
    fk_section: Union[int, None]

    class Config:
        orm_mode = True
