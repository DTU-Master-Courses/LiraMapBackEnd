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
    MapReference
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


def get_drdmeasurement(DRDmeasurement_id: str, db: Session):

    return (
        db.query(DRDMeasurement).filter(DRDMeasurement.id == DRDmeasurement_id).first()
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
    print(res)
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
