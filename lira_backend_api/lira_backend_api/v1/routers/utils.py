# Main Dev: Tswagerman
# Supporting Devs: Mikfor, wangrandk, HUIYULEO, ViktorRindom, PossibleNPC
from datetime import datetime
from math import atan2, acos, sin, cos, pi, pow, sqrt
from pathlib import Path
from typing import Union

import dateutil.parser
from sqlalchemy import and_
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

sql_files_path = Path.cwd().joinpath("lira_backend_api/core/sql/").resolve()


async def measurement_types(db: Connection):
    query = select(MeasurementTypes).order_by(MeasurementTypes.type)
    results = await db.fetch_all(query)

    return results


async def get_measurementtype(measurement_type_id: str, db: Connection):

    query = select(MeasurementTypes).where(MeasurementTypes.id == measurement_type_id)
    result = await db.fetch_one(query)

    return result


async def get_drdmeasurement(drdmeasurement_id: str, db: Connection):

    query = select(DRDMeasurement).where(DRDMeasurement.id == drdmeasurement_id)
    result = await db.fetch_one(query)

    return result


async def get_mapreference(mapreference_id: str, db: Connection):
    query = select(MapReference).where(MapReference.id == mapreference_id)
    result = await db.fetch_one(query)

    return result


async def get_trip(trip_id: str, tag: Union[str, None], db: Connection):
    if tag:
        query = (
            open(sql_files_path.joinpath("func_measurements_tag_agg.sql"), "r")
            .read()
            .replace("+trip_id+", trip_id)
            .replace("+tag+", tag)
        )
        result = await db.fetch_all(query)
    else:
        query = select(Trip).where(Trip.id == trip_id)
        result = await db.fetch_one(query)

    if result is None:
        return None

    return result


async def get_deviceid(device_id: str, db: Connection):
    query = select(Device).where(Device.id == device_id)
    result = await db.fetch_one(query)

    if result is None:
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


def convert_date_test(json_created_date: any):
    str_format_date = json_created_date[:-6]
    date_as_iso = dateutil.parser.isoparse(str_format_date)
    return date_as_iso


async def get_trips(db: Connection):
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


def scalarProductPower(velocity, force_vector):
    velocity_mag = magnitudeCalc(velocity[0], velocity[1])
    force_mag = magnitudeCalc(force_vector[0], force_vector[1])
    angle = angleVectCalc(velocity, force_vector, velocity_mag, force_mag)
    return velocity_mag * force_mag * cos(angle)


def bearingCalc(latitude, latitude_previous, longitude, longitude_previous):
    d_lon = abs(longitude - longitude_previous)
    X = cos(longitude) * sin(d_lon)
    Y = (cos(latitude) * sin(latitude)) - (
        sin(latitude) * cos(latitude_previous) * cos(d_lon)
    )
    # atan2 to convert X, Y to radians. Then use pi to convert to degrees.
    return atan2(X, Y)  # * 180/pi + 360) % 360


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


def inertialCalc(longitudinal_acceleration, car_mass):
    return longitudinal_acceleration * car_mass


def tireRollResistCalc(velocity, car_mass):
    # Where krt = 0.01.*(1+(obd.spd_veh*3.6)./100) is the rolling resistant coefficient)
    # gw in m/s2 is the gravitational acceleration
    krt = [0.01 * (1 + (i * 3.6) / 100) for i in velocity]
    gw = 9.80665
    return [car_mass * gw * i for i in krt]


def hillClimbingCalc(slope, car_mass):
    gw = 9.80665
    return car_mass * gw * slope


def aerodynamicCalc(velocity):
    # Where cd is the air drag coefficient, rho in kg/m3 is the density of the air
    # A in m^2 is the cross-sectional area of the car
    rho = 1.225
    A = 2.3316
    cd = 0.29
    return [0.5 * rho * A * cd * i**2 for i in velocity]


async def get_acceleration(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_acceleration.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    result = await db.fetch_all(query)
    return result


async def get_variable_list(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_measurements_scrape.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    result = await db.fetch_all(query)
    return result


# Not working as inteded yet, use trip_id = 2857262b-71db-49df-8db6-a042987bf0eb to see some non zero output
async def get_speed_list(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_speedlist.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


async def get_speed_list_agg(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_speedlist.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


async def get_climbingforce(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_climbingforce.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


# Not working as inteded yet, use trip_id = 2857262b-71db-49df-8db6-a042987bf0eb to see some non zero output
async def get_energy(trip_id: str, db: Connection):
    energy = list()
    car_mass = 1584
    E = 0.0
    bearing = 0
    velocity = [0, 0]
    distance = 0
    dictionary = await get_variable_list(trip_id, db)
    for rec in dictionary:
        result = tuple(rec.values())
        # result index from 0 to 9 ts_date, ts_time, az, ay,
        # ax, speed, acc_long, acc_yaw, lat, lon
        speed = float(result[5]) / 3.6 if result[5] else 0
        # offset of 198 according to car data validation
        # resolution changed from 1 to 0.05
        # longitudinal acceleration - units of meters
        acc_long = (float(result[6]) - 198) * 0.05 if result[6] else 0  # m/s^2
        # Offset of 2047
        acc_yaw = (float(result[7]) - 2047) if result[7] else 0  # in degrees a second

        # Bearing is the direction of the vehicle
        if (dictionary.index(rec)) + 1 != len(dictionary):
            next_ = tuple(dictionary[dictionary.index(rec) + 1].values())
            bearing = bearingCalc(result[8], next_[8], result[9], next_[9])
        if (dictionary.index(rec)) != 0:
            previous_ = tuple(dictionary[dictionary.index(rec) - 1].values())
            distance = distanceCalc(result[8], previous_[8], result[9], previous_[9])
        # Division by 3.6 to convert km/h to m/s
        Xvel = cos(bearing) * float(speed)  # * cos(Z-Bearing)
        Yvel = sin(bearing) * float(speed)  # * cos(Z-Bearing)
        # Zvel = sin(Z-Bearing)
        velocity = [Xvel, Yvel]
        # Force. Inertial force and hill climbing force are calculated as scalar values.
        inertial_force = inertialCalc(acc_long, car_mass)
        hill_climbing_force = hillClimbingCalc(acc_yaw, car_mass)
        aerodynamic_force = aerodynamicCalc(velocity)
        rolling_resistance_force = tireRollResistCalc(velocity, car_mass)
        force_vector = [
            aerodynamic_force[i] + rolling_resistance_force[i]
            for i in range(len(velocity))
        ]
        P = scalarProductPower(velocity, force_vector) + (
            inertial_force + hill_climbing_force
        ) * magnitudeCalc(velocity[0], velocity[1])
        force = (
            magnitudeCalc(force_vector[0], force_vector[1])
            + inertial_force
            + hill_climbing_force
        )
        E += (1 / 3600) * distance * force
        date = str(result[0] + " " + result[1])
        energy.append(
            {
                "power": P,
                "energy": E,
                "bearing": bearing,
                "distance": distance,
                "inertial_force": inertial_force,
                "inertial_energy": (1 / 3600) * distance * inertial_force,
                "hill_climbing_force": hill_climbing_force,
                "hill_climbing_energy": (1 / 3600) * distance * hill_climbing_force,
                "aerodynamic_force": magnitudeCalc(
                    aerodynamic_force[0], aerodynamic_force[1]
                ),
                "aerodynamic_energy": (1 / 3600)
                * distance
                * magnitudeCalc(aerodynamic_force[0], aerodynamic_force[1]),
                "rolling_resistance_force": magnitudeCalc(
                    rolling_resistance_force[0], rolling_resistance_force[1]
                ),
                "rolling_resistance_energy": (1 / 3600)
                * distance
                * magnitudeCalc(
                    rolling_resistance_force[0], rolling_resistance_force[1]
                ),
                "created_date": date,
            }
        )
    return energy


async def get_segments(trip_id: str, db: Connection):
    query = (
        select(MeasurementModel)
        .where(
            (MeasurementModel.fk_trip == trip_id) & (MeasurementModel.tag == "acc.xyz")
        )
        .order_by(MeasurementModel.timestamp)
        .limit(10000)
    )

    results = await db.fetch_all(query)

    return results


async def get_rpm_list(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_rpmlist.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


async def get_rpm_LR(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_rpmlist_agg.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


async def get_trip_friction(trip_id: str, db: Connection):
    query = (
        open(sql_files_path.joinpath("func_friction.sql"), "r")
        .read()
        .replace("+trip_id+", trip_id)
    )
    res = await db.fetch_all(query)
    return res


async def get_physics(task_id: int, db: Connection):
    # First we have to get the Trip UUID from the Task ID
    query = (
        select(Trip)
        .where(
            (Trip.task_id == task_id)
        )
    )
    res = await db.fetch_one(query)

    if res is None:
        return None

    trip_id = str(res["TripId"])

    speed_agg_results = await get_speed_list_agg(trip_id=trip_id, db=db)
    climbing_force_results = await get_climbingforce(trip_id=trip_id, db=db)
    accel_results = await get_variable_list(trip_id=trip_id, db=db)
    speed_results = await get_speed_list(trip_id=trip_id, db=db)
    energy_results = await get_energy(trip_id=trip_id, db=db)
    rpm_results = await get_rpm_list(trip_id=trip_id, db=db)
    friction_results = await get_trip_friction(trip_id=trip_id, db=db)

    massive_json = {
        "speed_aggregation": speed_agg_results,
        "climbing_force": climbing_force_results,
        "acceleration": accel_results,
        "speed": speed_results,
        "energy": energy_results,
        "content_rpm": rpm_results,
        "friction": friction_results,
    }

    return massive_json
