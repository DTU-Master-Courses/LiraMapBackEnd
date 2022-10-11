from datetime import datetime
from itertools import count
import json
from math import sqrt, pow, acos, pi
from queue import Empty
from random import betavariate
from re import T
from typing import List
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
from lira_backend_api.core.schemas import boundary

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
    #print(res)
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
            print(e)
            value = None

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


def clear_acceleration(list):
    list[0].clear()
    list[1].clear()
    list[2].clear()
    list[3].clear()
    list[4].clear()
    list[5].pop() #Single item stored, namely the datetime


def append_acceleration(list, x, y, z, latitude,longitude):
    list[0].append(x)
    list[1].append(y)
    list[2].append(z)
    list[3].append(latitude)
    list[4].append(longitude)


def get_current_acceleration(trip_id: str,db: Session):
    acceleration = list()
    average_acceleration_100Hz = list()
    created_date = None
    for _ in range(6):
        average_acceleration_100Hz.append(list())
    #Query to acquire messages from Measurements table 
    res = db.query(
                MeasurementModel.message,
                MeasurementModel.lat,
                MeasurementModel.lon
                ).where(
                    MeasurementModel.fk_trip == trip_id,
                    MeasurementModel.lon != None,
                    MeasurementModel.lat != None
                ).order_by(MeasurementModel.created_date).limit(1000).all()
    for value in res:
        latitude = value[1]
        longitude = value[2]
        jsonobj = json.loads(value[0])
        if jsonobj.get("acc.xyz.x") is not None and jsonobj.get("acc.xyz.y") is not None and jsonobj.get("acc.xyz.z")  is not None:
            x = jsonobj.get("acc.xyz.x") #xyz-vector based on data from the database.
            y = jsonobj.get("acc.xyz.y") #The reference frame is the car itself. 
            z = jsonobj.get("acc.xyz.z") #Eg. in which direction does the reference frame of x, y & z point.
            #Assuming created date is at least not None.
            json_created_date = jsonobj.get("@ts") 
            created_date = convert_date(json_created_date)
            #Only need the date once. 
            if average_acceleration_100Hz[5] == []:
                average_acceleration_100Hz[5].append(created_date)
            #This statement is called when a dataset with a different date is encountered.
            elif average_acceleration_100Hz[5][0] != created_date:
                x = sum(average_acceleration_100Hz[0])/len(average_acceleration_100Hz[0])
                y = sum(average_acceleration_100Hz[1])/len(average_acceleration_100Hz[1])
                z = sum(average_acceleration_100Hz[2])/len(average_acceleration_100Hz[2])
                latitude = sum(average_acceleration_100Hz[3])/len(average_acceleration_100Hz[3])
                longitude = sum(average_acceleration_100Hz[4])/len(average_acceleration_100Hz[4])
                acceleration.append(
                {
                    "x": x,
                    "y": y,
                    "z": z,
                    "lon": longitude,
                    "lat": latitude,
                    "created_date": created_date,
                })
                clear_acceleration(average_acceleration_100Hz)
            append_acceleration(average_acceleration_100Hz, x, y, z, latitude, longitude)
        else:
            print("at least one of acc.xyz is zero")
            continue
            
    return {"acceleration": acceleration}
