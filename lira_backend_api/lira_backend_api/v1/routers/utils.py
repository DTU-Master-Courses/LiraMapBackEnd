from ctypes import sizeof
from datetime import datetime
import json
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
from lira_backend_api.core.schemas import boundary
from math import atan2, acos, sin, cos, pi, pow, sqrt


def get_measurementtype(measurement_type_id: str, db: Session):

    return (
        db.query(MeasurementTypes)
        .filter(MeasurementTypes.id == measurement_type_id)
        .first()
    )


def get_measurementmodel(measurement_model_id: str, db: Session):

    return (
        db.query(MeasurementModel)
        .filter(MeasurementModel.id == measurement_model_id)
        .first()
    )


def get_drdmeasurement(drdmeasurement_id: str, db: Session):

    return (
        db.query(DRDMeasurement).filter(DRDMeasurement.id == drdmeasurement_id).first()
    )


def get_mapreference(mapreference_id: str, db: Session):
    return db.query(MapReference).filter(MapReference.id == mapreference_id).first()


def get_trip(trip_id: str, db: Session):
    # We need to swallow the value error, but one could argue that Pydantic should be failing first
    result = db.query(Trip).filter(Trip.id == trip_id).first()

    return result


def get_deviceid(device_id: str, db: Session):
    return db.query(Device).filter(Device.id == device_id).first()


def get_sourcetype(source_id: str, db: Session):
    return db.query(SourceType).filter(SourceType.id == source_id).first()


def convert_date(json_created_date: any):
    str_format_date = json_created_date[:-6]
    str_format_date = str_format_date.split(".")[0]
    date_as_iso = datetime.fromisoformat(str_format_date)
    return date_as_iso


def get_ride(trip_id: str, tag: str, db: Session):
    tripList = list()
    values = list()
    res = (
        db.query(
            MeasurementModel.message,
            MeasurementModel.lat,
            MeasurementModel.lon,
            MeasurementModel.created_date,
        )
        .where(MeasurementModel.fk_trip == trip_id)
        .filter(
            MeasurementModel.tag == tag
            and MeasurementModel.lon != None
            and MeasurementModel.lat != None
        )
        .order_by(MeasurementModel.created_date)
        .limit(500)
        .all()
    )
    res1 = json.loads(res[0][0])
    val = res1.get(f"{tag}.value")
    if val is None:
        return None

    for x in res:
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

    return {"path": tripList, "bounds": boundary(minX, maxX, minY, maxY)}


def get_trips(db: Session):
    rides = (
        db.query(Trip)
        .where(Trip.task_id != 0)
        .filter(Trip.start_position_lat != None)
        .filter(Trip.start_position_lng != None)
        .filter(Trip.end_position_lat != None)
        .filter(Trip.end_position_lng != None)
        .order_by(Trip.task_id)
        .limit(150)
        .all()
    )
    return rides


def measurement_types(db: Session):
    results = db.query(MeasurementTypes).order_by(MeasurementTypes.type).all()

    return results


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
    #Notice, subtracting gravitational pull from z
    #z - 1
    #Disregarding z entirely for now
    return  sqrt(pow(x,2) + pow(y,2))# + pow(z,2)) 


def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))

def angleVectCalc(a, b, maga, magb):
    if maga * magb == 0:
        return 0
    return  acos((dot(a, b)) / (maga * magb))


def bearingCalc(latitude, latitude_previous, longitude, longitude_previous):
    d_lon = abs(longitude - longitude_previous)
    X = cos(longitude) * sin(d_lon)
    Y = (cos(latitude) * sin(latitude)) - (sin(latitude) * cos(latitude_previous) * cos(d_lon))
    #atan2 to convert X, Y to radians. Then use pi to convert to degrees. 
    return (atan2(X, Y))# * 180/pi + 360) % 360


#Not needed if we can get 'obd.spd' from database. 
def distanceCalc(latitude, latitude_previous, longitude, longitude_previous):
    #Approximation of distance calculated by using lat and lon
    earth_radius = 6378.137e3 #meter
    lat_radians = latitude * (pi / 180)
    lat_prev_radians = latitude_previous * (pi / 180)
    d_lat = (latitude - latitude_previous) * (pi / 180)
    d_lon = (longitude - longitude_previous) * (pi / 180)
    #Haversine formula
    a = sin(d_lat/2) * sin(d_lat/2) + cos(lat_prev_radians) * cos(lat_radians) * sin(d_lon/2) * sin(d_lon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return c * earth_radius


def get_variable_list(trip_id: str, db: Session):
    #Saving these values in a database for all trips would save a lot of computation time
    variable_list, average_variable_list = list(), list()
    created_date, latitude_previous, longitude_previous = None, None, None
    distance = 0
    speed = 0
    #Create list filled with empty lists
    for _ in range(7):
        average_variable_list.append(list())
    # Query to acquire messages from Measurements table
    res = (
        db.query(MeasurementModel.message, MeasurementModel.lat, MeasurementModel.lon)
        .where(
            MeasurementModel.fk_trip == trip_id,
            MeasurementModel.lon != None,
            MeasurementModel.lat != None,
        ).filter(or_(MeasurementModel.tag == 'obd.spd', MeasurementModel.tag == 'obd.spd_veh', MeasurementModel.tag == 'acc.xyz'))
        .order_by(MeasurementModel.created_date)
        .limit(100000)
        .all()
    )
    for value in res:
        latitude, longitude = value[1], value[2]
        jsonobj = json.loads(value[0])
        if jsonobj.get("obd.spd_veh.value") is not None:
            speed = jsonobj.get("obd.spd_veh.value")
        if jsonobj.get("obd.spd.value") is not None:
            speed = jsonobj.get("obd.spd.value")
        if (
            jsonobj.get("acc.xyz.x") is not None
            and jsonobj.get("acc.xyz.y") is not None
            and jsonobj.get("acc.xyz.z") is not None
        ):
            x = jsonobj.get("acc.xyz.x")  # xyz-vector based on data from the database.
            y = jsonobj.get("acc.xyz.y")  # The reference frame is the car itself.
            z = jsonobj.get("acc.xyz.z")  # The acceleration in the z direction is influenced by the gravitational pull
            # Assuming created date is at least not None.
            json_created_date = jsonobj.get("@ts")
            created_date = convert_date(json_created_date)
            # Only need the date once.
            if average_variable_list[6] == []:
                average_variable_list[6].append(created_date)
            # This statement is called when a dataset with a different date is encountered.
            # This starts the process of calculating and storing values and clearing variable_list
            elif average_variable_list[6][0] != created_date:
                x, y, z, latitude, longitude, speed = average_values(average_variable_list)
                #True when there is a previous dataset to compare
                if latitude_previous:
                    #At the first iteration there is no comparison lat and lon
                    distance += distanceCalc(latitude, latitude_previous, longitude, longitude_previous)
                variable_list.append(
                    {
                        "x": x,
                        "y": y,
                        "z": z,
                        "lat": latitude,
                        "lon": longitude,
                        "magnitude": magnitudeCalc(x, y),
                        "speed": speed,
                        "distance": distance,
                        "created_date": created_date,
                    }
                )
                #Used to calculate the change in distance from point to point
                latitude_previous = latitude
                longitude_previous = longitude
                clear_average_variable_list(average_variable_list)
            append_variable_list(
                average_variable_list, x, y, z, latitude, longitude, speed
            )
    return {"variables": variable_list}

def get_speed_list(trip_id: str, db: Session):
    l = list()
    res = db.execute(" select * from public.func_SpeedList( '"+trip_id+"') ")
    print("result = ",res) 
    for value in res:
        l.append(
                        {
                            "ts": value.ts,
                            "vid": value.vid,
                            "uid": value.uid,
                            "rec": value.rec,
                            "speed": value.speed,
                            "lon": value.lon,
                            "lat": value.lat,
                            
                        }
                    ) 
    print("speed count = ",len(l)) 
    return l

def get_speed_list_agg(trip_id: str, db: Session):
    l = list()
    res = db.execute(" select * from public.func_SpeedList_agg( '"+trip_id+"') ")
    print("result = ",res) 
    for value in res:
        l.append(
                        {
                            "ts_date": value.ts_date,
                            "ts_time": value.ts_time,
                            "vid": value.vid,
                            "speed": value.speed,
                            "lon": value.lon,
                            "lat": value.lat,
                            
                        }
                    ) 
    print("speed count = ",len(l)) 
    return l        
        

#Not working as inteded yet, use trip_id = 2857262b-71db-49df-8db6-a042987bf0eb to see some non zero output
def get_energy(trip_id: str, db: Session):
    energy = list()
    car_mass = 1584
    E = 0.0
    bearing = 0
    velocity = [0, 0]
    dictionary = get_variable_list(trip_id, db)
    values = dictionary["variables"]
    for i in values:
        acceleration_mag = i["magnitude"]
        speed = i["speed"]
        #Need to implement the angle 
        #between the acceleration wrt the vehicles direction
        acceleration = [i["x"], i["y"]]
        #Bearing is the direction of the vehicle
        if (values.index(i))+1 != len(values):
            next_ = values[values.index(i)+1]
            bearing = bearingCalc(next_["lat"], i["lat"], next_["lon"], i["lon"])
        Xvel = cos(bearing) * speed #* cos(Z-Bearing)
        Yvel = sin(bearing) * speed #* cos(Z-Bearing)
        #Zvel = sin(Z-Bearing)
        change_in_velocity = [Xvel - velocity[0], Yvel - velocity[1]]
        print("change_in_velocity = ", change_in_velocity)
        velocity = [Xvel, Yvel]
        #Force Vector
        inertial_force = [i * car_mass for i in change_in_velocity]
        print("inertial_force = ", inertial_force)
        # aerodynamic_force = 
        # hill_climbing_force = 
        # rolling_resistance_force = 
        force = inertial_force # + aerodynamic_force + hill_climbing_force + rolling_resistance_force
        print("force = ", force)
        velocity_ms = [i / 3.6 for i in velocity]
        print("velocity_ms = ", velocity_ms)
        #Scalar product of force and velocity
        velocity_mag = magnitudeCalc(velocity_ms[0], velocity_ms[1])
        force_mag = magnitudeCalc(force[0], force[1])
        angle = angleVectCalc(velocity_ms, force, velocity_mag, force_mag)
        #scalar product
        P = velocity_mag * force_mag * cos(angle)
        print("power = ", P)
        E += P
        energy.append({
            "power": P,
            "energy": E,
            "bearing": bearing,
            "created_date": i["created_date"],
            })
    return {"energy": energy}


def get_segments(trip_id: str, db: Session):
    # results = db.query(MapReference).where(MeasurementModel.fk_trip == trip_id).join(MapReference, MapReference.fk_measurement_id == MeasurementModel.id).limit(100).all()

    # results = db.query(MeasurementModel).where(MeasurementModel.fk_trip == trip_id).order_by(MeasurementModel.timestamp).join(MapReference, MeasurementModel.id == MapReference.fk_measurement_id).filter((MapReference.lat_map_matched != -1) | (MapReference.lat_map_matched != None) | (MapReference.lon_map_matched != -1) | (MapReference.lon_map_matched != None)).all()

    lat_lon_collection_all = list()
    lat_lon_collection_minified = list()

    results = (
        db.query(MeasurementModel)
        .where(
            (MeasurementModel.fk_trip == trip_id) & (MeasurementModel.tag == "acc.xyz")
        )
        .order_by(MeasurementModel.timestamp)
        .all()
    )

    for result in results:
        lat_lon_collection_all.append(tuple([result.lat, result.lon]))

    for i in range(len(lat_lon_collection_all)):
        if i % 10 == 0:
            lat_lon_collection_minified.append(lat_lon_collection_all[i])

    return lat_lon_collection_minified
