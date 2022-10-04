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

    return (
        db.query(Trip)
        .filter(Trip.id == trip_id)
        .first()
    )
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
            MeasurementModel.created_date).first()
    print(res)
    
    #document if created date is not available
    #try '@ts'
    #for x in res:
    #TODO investigate any table with a column of TEXT and diff the JSON
    #TODO else 

    jsonobj = json.loads(res[0])
    try: 
        if int(jsonobj.get(f"{tag}.value")) is not None:
            value = int(jsonobj.get(f"{tag}.value"))
            values.append(value)
            json_created_date = jsonobj.get("Created_Date")
        else: 
            
            
        if json_created_date is not None:
            tripList.append({'lat': jsonobj.lat, 'lng': jsonobj.lon, 'value': value, 'metadata': { jsonobj.created_date }})
        else:
            #json_created_date = datetime.strptime(jsonobj.get("@ts"), "%Y-%m-%d")
            json_created_date = datetime.fromisoformat(jsonobj.get("@ts"))
            tripList.append({'lat': jsonobj.lat, 'lng': jsonobj.lon, 'value': value, 'metadata': { json_created_date }})
            
    except Exception as e:
        print(e)
        value = None
    
    #minX = min(json_created_date)
    #maxX = max(json_created_date)

    #Todo
    #minX = min(res, key=lambda x: x.created_date)
    #maxX = max(res, key=lambda x: x.created_date)
    minY = min(values)
    maxY = max(values)

    return { 'path': tripList, 'bounds': boundary(json_created_date, json_created_date, minY, maxY) }

{"id":"00000000-0000-0000-0000-000000000000",
"start_time_utc":"0001-01-01T00:00:00+00:00",
"end_time_utc":"0001-01-01T00:00:00+00:00",
"@vid":44,
"@uid":"76170df3-3657-580b-86ab-e49db637c793",
"@ts":"2022-04-23T17:41:42.041+00:00",
"@t":"track.pos",
"@rec":"2022-04-23T17:41:44.145+00:00",
"track.pos.utc":"2022-05-13T17:41:41+00:00",
"track.pos.alt":15.7,
"track.pos.nsat":8,
"track.pos.cog":177.4,
"track.pos.sog":34,
"track.pos.loc":{"lat":55.72114,"lon":12.52967}}