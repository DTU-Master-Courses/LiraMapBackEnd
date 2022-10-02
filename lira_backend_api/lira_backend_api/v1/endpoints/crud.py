from sqlalchemy.orm import Session
from lira_backend_api.core.models import MeasurementTypes, MeasurementModel, Trip, DRDMeasurement, Device, SourceTypes




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

def get_DRDmeasurement(DRDmeasurement_id: str, db: Session):

    return (
        db.query(DRDMeasurement)
        .filter(DRDMeasurement.id == DRDmeasurement_id)
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
