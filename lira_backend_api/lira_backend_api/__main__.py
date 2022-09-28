from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import uvicorn
from lira_backend_api.core.schemas.measurements import MeasurementTypes

from lira_backend_api.database.db import get_db
from lira_backend_api.v1.endpoints.crud import get_measurementtype


app = FastAPI()


@app.get("/{measurement_type_id}", response_model=MeasurementTypes)
def root(measurement_type_id: str, db: Session = Depends(get_db)):
    result = get_measurementtype(measurement_type_id, db)

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
