from typing import Any, List, Union

from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from datetime import datetime
from sqlalchemy import BigInteger
from collections import namedtuple


@dataclass(frozen=True)
class MeasurementTypes:
    id: UUID
    created_date: datetime
    type: str


@dataclass(frozen=True)
class MeasurementModel:
    id: UUID
    timestamp: datetime
    tag: Union[str, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[UUID, None]
    fk_measurement_type: Union[UUID, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]


@dataclass(frozen=True)
class Device:
    id: UUID
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    fk_sourcetype: Union[UUID, None]

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class Trip:
    id: UUID
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
    fk_device: Union[UUID, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    fully_imported: Union[bool, None]


@dataclass(frozen=True)
class SourceType:
    id: UUID
    source_name: Union[str, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class TripTest(BaseModel):
    trip_id: Union[str, None]
    lat: Union[float, None]
    lng: Union[float, None]
    value: Union[int, None]
    metadata: Any

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class DRDMeasurement:

    id: UUID
    distance: str
    tag: Union[str, None]
    is_computed: Union[bool, None]
    fk_trip: Union[UUID, None]
    fk_measurement_type: Union[UUID, None]
    created_date: Union[datetime, None]
    updated_date: Union[datetime, None]
    lat: Union[float, None]
    lon: Union[float, None]
    message: Union[str, None]
    

    class Config:
        orm_mode = True


boundary = namedtuple("Boundary", ["minX", "maxX", "minY", "maxY"])


@dataclass(frozen=True)
class TripsReturn(BaseModel):
    path: List[TripTest]
    bounds: boundary
    start_city: str
    end_city: str

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class MapReference(BaseModel):

    id: UUID
    lat_MapMatched: Union[float, None]
    lon_MapMatched: Union[float, None]
    way_point_name: Union[str, None]
    leg_summary_map_matched: Union[str, None]
    leg_distance_map_matched: Union[float, None]
    node_id_map_matched: Union[str, None]
    possible_matching_routes: Union[str, None]
    way_point: Union[str, None]
    fk_measurement_id: Union[UUID, None]
    fk_osmwaypointid: Union[int, None]
    offset: Union[str, None]
    lane: Union[str, None]
    direction: Union[str, None]
    

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class ContentAcceleration(BaseModel):
    x: Union[float, None]
    y: Union[float, None]
    z: Union[float, None]
    lon: Union[float, None]
    lat: Union[float, None]
    created_date: Union[datetime, None]

    class Config:
        orm_mode = True


# TODO: REMOVE ME
@dataclass(frozen=True)
class Acceleration(BaseModel):
    acceleration: List[ContentAcceleration]

    class Config:
        orm_mode = True


@dataclass(frozen=True)
class MeasurementLatLon(BaseModel):
    lat: Union[float, None]
    lon: Union[float, None]

    class Config:
        orm_mode = True
