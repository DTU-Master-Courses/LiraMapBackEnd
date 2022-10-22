from datetime import datetime
import json
from math import sqrt, pow, acos, pi


from sqlalchemy.sql import select

from databases.core import Connection
from lira_backend_api.core.models import (
    DRDMeasurement,
    MeasurementTypes,
    MeasurementModel,
    Trip,
    Device,
    SourceType,
    MapReference,
)

# TODO move schema processing to the endpoint
from lira_backend_api.core.schemas import (
    TripsReturn,
    boundary,
)

async def measurement_types(db: Connection):
    query = select(MeasurementTypes).order_by(MeasurementTypes.type)
    results = await db.fetch_all(query)

    return results

# TODO add function return types to all functions
async def get_measurementtype(measurement_type_id: str, db: Connection):

    query = select(MeasurementTypes).where(MeasurementTypes.id == measurement_type_id)
    result = await db.fetch_one(query)

    return result


async def get_measurementmodel(measurement_model_id: str, db: Connection):

    query = select(MeasurementModel).where(MeasurementModel.id == measurement_model_id)
    result = await db.fetch_one(query)

    return result
    # return (
    #     db.query(MeasurementModel)
    #     .filter(MeasurementModel.id == measurement_model_id)
    #     .first()
    # )


async def get_drdmeasurement(drdmeasurement_id: str, db: Connection):

    query = select(DRDMeasurement).where(DRDMeasurement.id == drdmeasurement_id)
    result = await db.fetch_one(query)

    return result

    # result = DRDMeasurement(id=result._mapping["DRDMeasurementId"],
    # distance)

    # return (
    #     db.query(DRDMeasurement).filter(DRDMeasurement.id == drdmeasurement_id).first()
    # )


async def get_mapreference(mapreference_id: str, db: Connection):
    query = select(MapReference).where(MapReference.id == mapreference_id)
    result = await db.fetch_one(query)

    return result


# KT: Migrated to new approach
# TODO add start city and end city
async def get_trip(trip_id: str, db: Connection):
    # We need to swallow the value error, but one could argue that Pydantic should be failing first
    query = select(Trip).where(Trip.id == trip_id)
    result = await db.fetch_one(query)
    if result is None:
        return None

    # result = Trip(
    #     id=result._mapping["TripId"],
    #     task_id=result._mapping["TaskId"],
    #     start_time_utc=result._mapping["StartTimeUtc"],
    #     end_time_utc=result._mapping["EndTimeUtc"],
    #     start_position_lat=result._mapping["StartPositionLat"],
    #     start_position_lng=result._mapping["StartPositionLng"],
    #     start_position_display=result._mapping["StartPositionDisplay"],
    #     end_position_lat=result._mapping["EndPositionLat"],
    #     end_position_lng=result._mapping["EndPositionLng"],
    #     end_position_display=result._mapping["EndPositionDisplay"],
    #     duration=result._mapping["Duration"],
    #     distance_km=result._mapping["DistanceKm"],
    #     fk_device=result._mapping["FK_Device"],
    #     created_date=result._mapping["Created_Date"],
    #     updated_date=result._mapping["Updated_Date"],
    #     fully_imported=result._mapping["Fully_Imported"],
    # )

    return result


async def get_deviceid(device_id: str, db: Connection):
    query = select(Device).where(Device.id == device_id)
    result = await db.fetch_one(query)

    if result == None:
        return None

    return result


async def get_sourcetype(source_id: str, db: Connection):
    query = select(SourceType).filter(SourceType.id == source_id)
    result = await db.fetch_one(query)

    if result is None:
        return None

    result = SourceType(
        id=result._mapping["SourceTypeId"],
        source_name=result._mapping["SourceName"],
        created_date=result._mapping["Created_Date"],
        updated_date=result._mapping["Updated_Date"],
    )

    return result


def convert_date(json_created_date: any):
    str_format_date = json_created_date[:-6]
    str_format_date = str_format_date.split(".")[0]
    date_as_iso = datetime.fromisoformat(str_format_date)
    return date_as_iso


# I don't like how complex this function is. This is definitely a code smell at a minimum.
async def get_ride(trip_id: str, tag: str, db: Connection):
    tripList = list()
    values = list()
    start_city_json = ""
    end_city_json = ""
    query = (
        select(
            MeasurementModel.message,
            MeasurementModel.lat,
            MeasurementModel.lon,
            MeasurementModel.created_date,
            Trip.start_position_display,
            Trip.end_position_display,
        )
        .where(MeasurementModel.fk_trip == trip_id)
        .join(Trip, Trip.id == trip_id)
        .filter(
            MeasurementModel.tag == tag
            and MeasurementModel.lon != None
            and MeasurementModel.lat != None
        )
        .order_by(MeasurementModel.created_date)
        .limit(150)
    )

    result = await db.fetch_all(query)
    result1 = json.loads(result[0][0])
    start, end = json.loads(result[0][4]), json.loads(result[0][5])
    start_city_json, end_city_json = start.get("city"), end.get("city")
    val = result1.get(f"{tag}.value")
    if val is None:
        return None

    for x in result:
        jsonobj = json.loads(x[0])
        try:
            if jsonobj.get(f"{tag}.value") is not None:
                value = int(jsonobj.get(f"{tag}.value"))
                values.append(value)
                json_created_date = jsonobj.get("Created_Date")
            else:
                pass
            if json_created_date is not None:
                date_as_iso = convert_date(json_created_date)
                tripList.append(
                    {
                        "trip_id": trip_id,
                        "lat": x[1],
                        "lng": x[2],
                        "value": value,
                        "metadata": date_as_iso,
                    }
                )
            else:
                json_created_date = jsonobj.get("@ts")
                date_as_iso = convert_date(json_created_date)
                tripList.append(
                    {
                        "trip_id": trip_id,
                        "lat": x[1],
                        "lng": x[2],
                        "value": value,
                        "metadata": date_as_iso,
                    }
                )

        except Exception as e:
            # TODO: Hook this up to the logger we need to use!!!
            print(e)
            value = None

    # TODO: This needs to be made more clear on which pair is starting point, and which is end
    minX = min(tripList, key=lambda x: x["metadata"])
    maxX = max(tripList, key=lambda x: x["metadata"])
    minY = min(values)
    maxY = max(values)

    result = TripsReturn(
        path=[x for x in tripList],
        bounds=boundary(minX=minX, maxX=maxX, minY=minY, maxY=maxY),
        start_city=start_city_json,
        end_city=end_city_json,
    )

    return result


async def get_trips(db: Connection):
    query = (
        select(Trip)
        .where(Trip.task_id != 0)
        .filter(Trip.start_position_lat != None)
        .filter(Trip.start_position_lng != None)
        .filter(Trip.end_position_lat != None)
        .filter(Trip.end_position_lng != None)
        .order_by(Trip.task_id)
        .limit(150)
    )

    results = await db.fetch_all(query)

    return results

    # rides = (
    #     db.query(Trip)
    #     .where(Trip.task_id != 0)
    #     .filter(Trip.start_position_lat != None)
    #     .filter(Trip.start_position_lng != None)
    #     .filter(Trip.end_position_lat != None)
    #     .filter(Trip.end_position_lng != None)
    #     .order_by(Trip.task_id)
    #     .limit(150)
    #     .all()
    # )
    # return rides


# TODO: This is completely broken
async def get_current_acceleration(trip_id: str, db: Connection):
    acc_vector = list()
    query = (
        select(MeasurementModel.message, MeasurementModel.lat, MeasurementModel.lon)
        .where(MeasurementModel.fk_trip == trip_id, MeasurementModel.tag == "acc.xyz")
        .order_by(MeasurementModel.created_date)
        .limit(100)
    )
    res = await db.fetch_all(query)
    for i in res:
        jsonobj = json.loads(i[0])
        if (
            jsonobj.get("acc.xyz.x")
            and jsonobj.get("acc.xyz.y")
            and jsonobj.get("acc.xyz.z") is not None
        ):
            x = jsonobj.get("acc.xyz.x")  # xyz-vector based on data from the database.
            y = jsonobj.get(
                "acc.xyz.y"
            )  # What the reference frame is, is unclear. Need to ask in class.
            z = jsonobj.get(
                "acc.xyz.z"
            )  # Eg. in which direction does the reference frame of x, y & z point.
            # Length is used to calculate the direction. It is also called the magnitude of the vector.
            # Hence it is the relative acceleration wrt. the xyz frame.
            length = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))
            alpha = (
                acos(x / length) * 180 / pi
            )  # Angle(in degrees) of xyz-vector wrt. x-axis
            beta = acos(y / length) * 180 / pi  # Angle of xyz-vector wrt. y-axis
            gamma = acos(z / length) * 180 / pi  # Angle of xyz-vector wrt. z-axis
            # Assuming created date is at least not None.
            json_created_date = jsonobj.get("@ts")
            created_date = convert_date(json_created_date)

            direction = list()
            direction.append(  # The 3d xyz-vector is pointing in a direction in each dimension.
                {
                    "alpha": alpha,
                    "beta": beta,
                    "gamma": gamma,
                }
            )
            acc_vector.append(
                {
                    "x": x,
                    "y": y,
                    "z": z,
                    "lat": i.lat,
                    "lon": i.lon,
                    "created_date": created_date,
                }
            )
        else:
            acc_vector.append(
                {
                    "x": None,
                    "y": None,
                    "z": None,
                    "lat": None,
                    "lon": None,
                    "created_date": None,
                }
            )

    return acc_vector


async def get_segments(trip_id: str, db: Connection):
    query = (
        select(MeasurementModel)
        .where(
            (MeasurementModel.fk_trip == trip_id) & (MeasurementModel.tag == "acc.xyz")
        )
        .order_by(MeasurementModel.timestamp)
    )

    results = await db.fetch_all(query)

    return results
