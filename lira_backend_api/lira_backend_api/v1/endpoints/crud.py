import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from lira_backend_api.core.models.measurements import MeasurementTypes


# measurement_types_table = Base.metadata.tables["MeasurementTypes"]

def get_measurementtype(measurement_type_id: str, db: Session):
    # query = measurement_types_table.select().filter(measurement_types_table.id == measurement_type_id).first()

    # return await db.execute(query)

    return db.query(MeasurementTypes).filter(MeasurementTypes.id == measurement_type_id).first()

    # return await db.query(MeasurementTypes).filter(MeasurementTypes.id == uuid(measurement_type_id)).first()
    #db.query(models.MeasurementTypes).filter(models.MeasurementTypes.MeasurementTypeId == measurement_type_id).first()