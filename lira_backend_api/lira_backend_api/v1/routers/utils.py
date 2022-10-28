from datetime import datetime
import json
from sqlalchemy.orm import Session
from lira_backend_api.core.models import (
    DRDMeasurement,
    MeasurementTypes,
    MeasurementModel,
    Trip,
    Device,
    SourceType,
    MapReference,
)
from lira_backend_api.core.schemas import Acceleration, Direction, boundary
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
    # print(res)
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
    return x, y, z, latitude, longitude


def append_acceleration(list, x, y, z, latitude, longitude):
    list[0].append(x)
    list[1].append(y)
    list[2].append(z)
    list[3].append(latitude)
    list[4].append(longitude)


def clear_average_acceleration(list):
    list[0].clear()
    list[1].clear()
    list[2].clear()
    list[3].clear()
    list[4].clear()
    list[5].pop()  # Single item stored, namely the datetime


def magnitudeCalc(x, y):
    #Notice, only based on x & y
    magnitude = sqrt(pow(x,2) + pow(y,2)) 
    return magnitude


def bearingCalc(latitude, latitude_previous, longitude, longitude_previous):
    d_lon = abs(longitude - longitude_previous)
    X = cos(longitude) * sin(d_lon)
    Y = (cos(latitude) * sin(latitude)) - (sin(latitude) * cos(latitude_previous) * cos(d_lon))
    #atan to convert X, Y to radians. Then use pi to convert to degrees.
    return (atan2(X, Y) * 180/pi + 360) % 360


def distanceCalc(latitude, latitude_previous, longitude, longitude_previous):
    #Approximation of distance calculated by using lat and lon
    earth_radius = 6371e3 #meter
    lat_radians = latitude * (pi / 180)
    lat_prev_radians = latitude_previous * (pi / 180)
    d_lat = (latitude - latitude_previous) * (pi / 180)
    d_lon = (longitude - longitude_previous) * (pi / 180)
    #Haversine formula
    print("latitude = ", latitude, "previous Latitude = ", latitude_previous,"longitude = ", longitude, "previous longitude = ", longitude_previous)
    a = sin(d_lat/2) * sin(d_lat/2) + cos(lat_prev_radians) * cos(lat_radians) * sin(d_lon/2) * sin(d_lon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    print("c * earth_radius = ", c * earth_radius)
    distance = c * earth_radius
    print("##Distance = ", distance, "\n")
    return distance


def average_speed():
    pass


def get_acceleration_list(trip_id: str, db: Session):
    acceleration = list()
    average_acceleration = list()
    created_date = None
    latitude_previous = None
    longitude_previous = None
    bearing = None
    distance = 0
    #Create list filled with empty lists
    for _ in range(6):
        average_acceleration.append(list())
    # Query to acquire messages from Measurements table
    res = (
        db.query(MeasurementModel.message, MeasurementModel.lat, MeasurementModel.lon)
        .where(
            MeasurementModel.fk_trip == trip_id,
            MeasurementModel.lon != None,
            MeasurementModel.lat != None,
        )
        .order_by(MeasurementModel.created_date)
        .limit(10000)
        .all()
    )
    for value in res:
        latitude = value[1]
        longitude = value[2]
        jsonobj = json.loads(value[0])
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
            if average_acceleration[5] == []:
                average_acceleration[5].append(created_date)
            # This statement is called when a dataset with a different date is encountered.
            # This starts the process of calculating and storing values and clearing average_acceleration
            elif average_acceleration[5][0] != created_date:
                x, y, z, latitude, longitude = average_values(average_acceleration)
                #True when there is a previous dataset to compare
                if latitude_previous:
                    #At the first iteration there is no comparison lat and lon
                    #Bearing and distance are not calculated
                    bearing = bearingCalc(latitude, latitude_previous, longitude, longitude_previous)
                    distance += distanceCalc(latitude, latitude_previous, longitude, longitude_previous)
                acceleration.append(
                    {
                        "x": x,
                        "y": y,
                        "z": z,
                        "lat": latitude,
                        "lon": longitude,
                        "magnitude": magnitudeCalc(x, y),
                        "bearing": bearing,
                        "distance": distance,
                        "created_date": created_date,
                    }
                )
                #Used to calculate the change in bearing & distance from point to point
                latitude_previous = latitude
                longitude_previous = longitude
                clear_average_acceleration(average_acceleration)
            append_acceleration(
                average_acceleration, x, y, z, latitude, longitude
            )
    return {"acceleration": acceleration}


def get_power(trip_id: str, db: Session):
    car_mass = 1584
    power = list()
    p = 0
    power.append({"power:":p})
    acceleration = get_acceleration_list(trip_id, db)
    for value in acceleration:
        print(value)
    return {"power": power}


#This endpoint is redundant
def get_direction(trip_id : str, db: Session):
    direction = list()
    lat = None
    lon = None
    acceleration = get_acceleration_list(trip_id, db)
    #print(acceleration)
    for index, (key, value) in enumerate(acceleration.items()):
        print("ENUMERATE")
        for i in value:
            print("i = ", i)
            if lon == None and lat == None:
                lat = i["lat"]
                lon = i["lon"]
                print("lat = ", lat,"lon = ", lon)
                magnitude = sqrt(pow(i["x"],2) + pow(i["y"],2))
                created_date = i["created_date"]
            else:
                d_lon = i["lon"] - lon
                X = cos(i["lat"]) * sin(d_lon)
                Y = (cos(lat) * sin(i["lat"])) - (sin(lat) * cos(i["lat"]) * cos(d_lon))
                lat = i["lat"]
                lon = i["lon"]
                bearing = atan2(X, Y) * 180/pi
                if bearing < 0:
                    bearing += 360
                elif bearing > 360:
                    bearing %= 360
                else:
                    pass
                direction.append(
                    {
                        "bearing": bearing,
                        "magnitude": magnitude,
                        "created_date": created_date,
                    }
                )    
                magnitude = sqrt(pow(i["x"],2) + pow(i["y"],2))
                created_date = i["created_date"]
        print(direction)
        #print("Index = ", index, "Key = ", key, "Value = ", value)
        return {"direction": direction}


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
