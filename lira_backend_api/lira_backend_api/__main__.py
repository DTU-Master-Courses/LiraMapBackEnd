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


# @app.post("/examples")
# async def create_examples(examples: ExampleCollection):
#     return examples


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# def include_router(app: FastAPI):
#     # TODO: Determine the router forming here
#     pass
#     # app.include_router()



# def start_app():
#     app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
#     include_router(app)
#     return app

# if __name__ == "__main__":
#     app = start_app()

# @app.get("/")
# def hello_api():
#     return {"msg":"Hello API"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, log_level="info")