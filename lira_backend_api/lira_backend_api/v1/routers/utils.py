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
from math import atan2, sin, cos, pi, pow, sqrt


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


def clear_acceleration(list):
    list[0].clear()
    list[1].clear()
    list[2].clear()
    list[3].clear()
    list[4].clear()
    list[5].pop()  # Single item stored, namely the datetime


def get_acceleration_list(trip_id: str, db: Session):
    acceleration = list()
    average_acceleration = list()
    created_date = None
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
    for idx, value in enumerate(res):
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
            z = jsonobj.get("acc.xyz.z")  # The acceleration in the z direction is heavily influenced by the gravitational pull
            # Assuming created date is at least not None.
            json_created_date = jsonobj.get("@ts")
            created_date = convert_date(json_created_date)
            # Only need the date once.
            if average_acceleration[5] == []:
                average_acceleration[5].append(created_date)
            # This statement is called when a dataset with a different date is encountered.
            elif average_acceleration[5][0] != created_date:
                x, y, z, latitude, longitude = average_values(average_acceleration)
                magnitude = sqrt(pow(x,2) + pow(y,2))
                #if res[idx + 1]:
                next_ =  res[idx + 1]
                latitude_next = next_[1]
                longitude_next = next_[2]
                d_lon = longitude_next - longitude
                X = cos(longitude_next) * sin(d_lon)
                Y = (cos(latitude_next) * sin(latitude_next)) - (sin(latitude_next) * cos(latitude) * cos(d_lon))
                #X = cos(latitude_next) * sin(d_lon)
                #Y = (cos(latitude_next) * sin(latitude_next)) - (sin(longitude) * cos(latitude_next) * cos(d_lon))
                bearing = atan2(X, Y) * 180/pi
                if bearing < 0:
                    bearing += 360
                elif bearing > 360:
                    bearing %= 360
                acceleration.append(
                    {
                        "x": x,
                        "y": y,
                        "z": z,
                        "lat": latitude,
                        "lon": longitude,
                        "magnitude": magnitude, #Based on x and y
                        "bearing": bearing,
                        "created_date": created_date,
                    }
                )
                clear_acceleration(average_acceleration)
            append_acceleration(
                average_acceleration, x, y, z, latitude, longitude
            )
    #print("Acceleratyion = ", acceleration)
    return {"acceleration": acceleration}


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
