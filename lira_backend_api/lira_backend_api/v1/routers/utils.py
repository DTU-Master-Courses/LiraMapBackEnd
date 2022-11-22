from datetime import datetime
import json
from math import atan2, acos, sin, cos, pi, pow, sqrt
from pathlib import Path

import dateutil.parser
from sqlalchemy.sql import select

from databases.core import Connection
from sqlalchemy.orm import Session
from sqlalchemy import null, or_, and_
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import Unicode, JSON
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

from lira_backend_api.settings import settings

sql_files_path = Path.cwd().joinpath("lira_backend_api/core/sql/").resolve()


async def measurement_types(db: Connection):
    query = select(MeasurementTypes).order_by(MeasurementTypes.type)
    results = await db.fetch_all(query)

    return results


# TODO add function return types to all functions
async def get_measurementtype(measurement_type_id: str, db: Connection):

    query = select(MeasurementTypes).where(MeasurementTypes.id == measurement_type_id)
    result = await db.fetch_one(query)

    return result


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


# throws a value error
def convert_date_test(json_created_date: any):
    str_format_date = json_created_date[:-6]
    # str_format_date = str_format_date.split(".")[0]
    # This is the part that throws the value error for invalid datetime
    # This is to test; there is a BIG fucking caveat with this in the docs, but not made apparent
    date_as_iso = dateutil.parser.isoparse(str_format_date)
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
    # query = open('../lira_backend_api/core/sql/func_alltrips.sql','r').read()
    query = open(sql_files_path.joinpath("func_alltrips.sql"), "r").read()
    res = await db.fetch_all(query)
    return res


def average_values(list):
    x = sum(list[0]) / len(list[0])
    y = sum(list[1]) / len(list[1])
    z = sum(list[2]) / len(list[2])
    latitude = sum(list[3]) / len(list[3])
    longitude = sum(list[4]) / len(list[4])
    speed = sum(list[5]) / len(list[5])
    return x, y, z, latitude, longitude, speed


def append_variable_list(list, x, y, z, latitude, longitude, speed):
    list[0].append(x)
    list[1].append(y)
    list[2].append(z)
    list[3].append(latitude)
    list[4].append(longitude)
    list[5].append(speed)


def clear_average_variable_list(list):
    list[0].clear()
    list[1].clear()
    list[2].clear()
    list[3].clear()
    list[4].clear()
    list[5].clear()
    list[6].pop()  # Single item stored, namely the datetime


def magnitudeCalc(x, y):
    # Notice, subtracting gravitational pull from z
    # z - 1
    # Disregarding z entirely for now
    return sqrt(pow(x, 2) + pow(y, 2))  # + pow(z,2))


def dot(K, L):
    if len(K) != len(L):
        return 0

    return sum(i[0] * i[1] for i in zip(K, L))


def angleVectCalc(a, b, maga, magb):
    if maga * magb == 0:
        return 0
    return acos((dot(a, b)) / (maga * magb))


def bearingCalc(latitude, latitude_previous, longitude, longitude_previous):
    d_lon = abs(longitude - longitude_previous)
    X = cos(longitude) * sin(d_lon)
    Y = (cos(latitude) * sin(latitude)) - (
        sin(latitude) * cos(latitude_previous) * cos(d_lon)
    )
    # atan2 to convert X, Y to radians. Then use pi to convert to degrees.
    return atan2(X, Y)  # * 180/pi + 360) % 360


# Not needed if we can get 'obd.spd' from database.
def distanceCalc(latitude, latitude_previous, longitude, longitude_previous):
    # Approximation of distance calculated by using lat and lon
    earth_radius = 6378.137e3  # meter
    lat_radians = latitude * (pi / 180)
    lat_prev_radians = latitude_previous * (pi / 180)
    d_lat = (latitude - latitude_previous) * (pi / 180)
    d_lon = (longitude - longitude_previous) * (pi / 180)
    # Haversine formula
    a = sin(d_lat / 2) * sin(d_lat / 2) + cos(lat_prev_radians) * cos(
        lat_radians
    ) * sin(d_lon / 2) * sin(d_lon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return c * earth_radius


def aerodynamicCalc(velocity):
    # Where cd is the air drag coefficient, rho in kg/m3 is the density of the air
    # A in m^2 is the cross-sectional area of the car
    rho = 1.225
    A = 2.3316
    cd = 0.29
    return [0.5 * rho * A * cd * i**2 for i in velocity]


def tireRollResistCalc(velocity, car_mass):
    # Where krt = 0.01.*(1+(obd.spd_veh*3.6)./100) is the rolling resistant coefficient)
    # gw in m/s2 is the gravitational acceleration
    krt = [0.01 * (1 + (i * 3.6) / 100) for i in velocity]
    gw = 9.80665
    return [car_mass * gw * i for i in krt]


async def get_variable_list(trip_id: str, db: Connection):
    # Saving these values in a database for all trips would save a lot of computation time
    # Query to acquire messages from Measurements table
    # query = open('lira_backend_api/core/sql/func_measurements_scrape.sql','r').read().replace('+trip_id+', trip_id)
    query = (
        open(sql_files_path.joinpath("func_measurements_scrape.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    result = await db.fetch_all(query)
    return result


# TODO This function is currently broken on async
# Not working as inteded yet, use trip_id = 2857262b-71db-49df-8db6-a042987bf0eb to see some non zero output
async def get_speed_list(trip_id: str, db: Connection):
    # query = open('lira_backend_api/core/sql/func_speedlist.sql','r').read().replace('+trip_id+', trip_id)
    query = (
        open(sql_files_path.joinpath("func_speedlist.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_speed_list_agg(trip_id: str, db: Connection):
    # query = open('lira_backend_api/core/sql/func_speedlist_agg.sql','r').read().replace('+trip_id+', trip_id)
    query = (
        open(sql_files_path.joinpath("func_speedlist.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_climbingforce(trip_id: str, db: Connection):
    # query = open('lira_backend_api/core/sql/func_climbingforce.sql','r').read().replace('+trip_id+', trip_id)
    query = (
        open(sql_files_path.joinpath("func_climbingforce.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


# TODO This function is currently broken on async
# Not working as inteded yet, use trip_id = 2857262b-71db-49df-8db6-a042987bf0eb to see some non zero output
async def get_energy(trip_id: str, db: Connection):
    energy = list()
    car_mass = 1584
    E = 0.0
    bearing = 0
    velocity = [0, 0]
    dictionary = await get_variable_list(trip_id, db)
    for rec in dictionary:
        result = tuple(rec.values())
        if "+" in result[1]:
            continue
        acceleration_mag = result[8]
        speed = result[5]
        # Need to implement the angle
        # between the acceleration wrt the vehicles direction
        acceleration = [result[5], result[4]]
        # Bearing is the direction of the vehicle
        if (dictionary.index(rec)) + 1 != len(dictionary):
            next_ = tuple(dictionary[dictionary.index(rec) + 1].values())
            bearing = bearingCalc(next_[6], result[6], next_[7], result[7])
        if (dictionary.index(rec)) - 1 != 0:
            previous_ = tuple(dictionary[dictionary.index(rec) - 1].values())
            distance = distanceCalc(result[6], previous_[6], result[7], previous_[7])
        if speed == None:
            speed = 0
        # Division by 3.6 to convert km/h to m/s
        speed = float(speed) / 3.6
        Xvel = cos(bearing) * float(speed)  # * cos(Z-Bearing)
        Yvel = sin(bearing) * float(speed)  # * cos(Z-Bearing)
        # Zvel = sin(Z-Bearing)
        change_in_velocity = [Xvel - velocity[0], Yvel - velocity[1]]
        velocity = [Xvel, Yvel]
        # Force Vector
        inertial_force = [i * car_mass for i in change_in_velocity]
        aerodynamic_force = aerodynamicCalc(velocity)
        # hill_climbing_force =
        rolling_resistance_force = tireRollResistCalc(velocity, car_mass)
        force = [
            inertial_force[i] + aerodynamic_force[i] + rolling_resistance_force[i]
            for i in range(len(inertial_force))
        ]  # + hill_climbing_force
        # Scalar product of force and velocity
        velocity_mag = magnitudeCalc(velocity[0], velocity[1])
        force_mag = magnitudeCalc(force[0], force[1])
        angle = angleVectCalc(velocity, force, velocity_mag, force_mag)
        # scalar product
        P = velocity_mag * force_mag * cos(angle)
        E += P
        date = str(result[0] + " " + result[1])
        energy.append(
            {
                "power": P,
                "energy": E,
                "bearing": bearing,
                "distance": distance,
                "created_date": date,
            }
        )
    return {"energy": energy}


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


async def get_rpm_list(trip_id: str, db: Connection):
    query = (
        open("lira_backend_api/core/sql/func_rpmlist.sql", "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_rpm_LR(trip_id: str, db: Connection):
    query = (
        open("lira_backend_api/core/sql/func_rpmlist_agg.sql", "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_trip_friction(trip_id: str, db: Connection):
    query = (
        open("lira_backend_api/core/sql/func_friction.sql", "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_speed_list_agg(trip_id: str, db: Connection):
    query = (
        open("lira_backend_api/core/sql/func_speedlist_agg.sql", "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res


async def get_climbingforce(trip_id: str, db: Connection):
    query = (
        open("lira_backend_api/core/sql/func_climbingforce.sql", "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    print("result length = ", len(res))
    return res
