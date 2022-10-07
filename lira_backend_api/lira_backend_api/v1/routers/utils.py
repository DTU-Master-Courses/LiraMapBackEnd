from datetime import datetime
import json
from sqlalchemy.orm import Session
from lira_backend_api.core.models import MeasurementTypes, MeasurementModel, Trip,Device, SourceTypes
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

def get_trip(trip_id: str, db: Session):
    # We need to swallow the value error, but one could argue that Pydantic should be failing first
    result = db.query(Trip)\
        .filter(Trip.id == trip_id)\
        .first()
   
    return result

def get_deviceid(device_id: str, db: Session):
    return(
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

def get_sourcetype(source_id: str, db: Session):
    return(
        db.query(SourceTypes)
        .filter(SourceTypes.id == source_id)
        .first()
    )

def get_ride(trip_id: str, tag: str, db: Session):
    #db.query(MeasurementModel, Trip)
    tripList = list()
    values = list()
    res = db.query(MeasurementModel.message, MeasurementModel.lat, MeasurementModel.lon, MeasurementModel.created_date).where(
        MeasurementModel.fk_trip == trip_id ).filter(
            MeasurementModel.tag == tag and MeasurementModel.lon != None and MeasurementModel.lat != None).order_by(
            MeasurementModel.created_date).limit(150).all()
    # print(res)
    
    #document if created date is not available
    #try '@ts'
    #for x in res:
    #TODO investigate any table with a column of TEXT and diff the JSON
    #TODO else 

    for x in res:
        jsonobj = json.loads(x[0])
        try: 
            if jsonobj.get(f"{tag}.value") is not None:
                value = int(jsonobj.get(f"{tag}.value"))
                values.append(value)
                json_created_date = jsonobj.get("Created_Date")
            # else: 
            #     exit()
            if json_created_date is not None:
                str_format_date = json_created_date[:-6]
                str_format_date = str_format_date.split(".")[0]
                date_as_iso = datetime.fromisoformat(str_format_date)
                tripList.append({'lat': x[1], 'lng': x[2], 'value': value, 'metadata': date_as_iso})
            else:
            #json_created_date = datetime.strptime(jsonobj.get("@ts"), "%Y-%m-%d")
                json_created_date = jsonobj.get("@ts")
                str_format_date = json_created_date[:-6]
                str_format_date = str_format_date.split(".")[0]
                date_as_iso = datetime.fromisoformat(str_format_date)
                tripList.append({'trip_id':trip_id, 'lat': x[1], 'lng': x[2], 'value': value, 'metadata':  date_as_iso })
            
        except Exception as e:
            print(e)
            value = None
    
    #minX = min(json_created_date)
    #maxX = max(json_created_date)

    #Todo
    minX = min(tripList, key=lambda x: x["metadata"])
    maxX = max(tripList, key=lambda x: x["metadata"])
    minY = min(values)
    maxY = max(values)

    return { 'path': tripList, 'bounds': boundary(minX, maxX, minY, maxY) }


def get_trips(db: Session):
    rides = db.query(Trip).where(Trip.taskId != 0)\
        .filter(Trip.startPositionLat != None)\
            .filter(Trip.startPositionLng != None)\
                .filter(Trip.endPositionLat != None)\
                    .filter(Trip.endPositionLng != None)\
                .order_by(Trip.taskId).limit(150).all()

    return rides
