from sqlalchemy.orm import Session
from lira_backend_api.core.models import MeasurementTypes


def get_measurementtype(measurement_type_id: str, db: Session):

    return (
        db.query(MeasurementTypes)
        .filter(MeasurementTypes.id == measurement_type_id)
        .first()
    )
