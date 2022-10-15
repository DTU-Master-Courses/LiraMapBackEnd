# from fastapi import APIRouter, Depends,Header, HTTPException
# from sqlalchemy.orm import Session

# from lira_backend_api.core.schemas import Device
# from lira_backend_api.v1.routers.utils import get_deviceid
# from lira_backend_api.database.db import get_db
from fastapi.testclient import TestClient

import json
from lira_backend_api.main import app
# router = APIRouter(prefix="/device")
client = TestClient(app)

# @router.get("/{device_id}", response_model=Device)
# def get_device_id(device_id: str, db: Session = Depends(get_db)):
#     result = get_deviceid(device_id, db)
#     return result
# testing sample from device table row No.4
# "DeviceId"	"Created_Date"	"Updated_Date"	"FK_SourceType"
# "47690661-f343-4591-920c-50dcd59f74e2"	"2020-05-28 00:00:00+00"	"2020-05-28 00:00:00+00"	"fb64715d-09d1-4fd9-8912-685364c7d446"
# 0cb38d9f-3601-4179-b5ef-403a999c9021
def test_get_device_id():
    res = client.get("/device/47690661-f343-4591-920c-50dcd59f74e2")
    assert res.status_code == 200
    print(res.status_code)
    print  (res.json())
    assert res.json() == {
        'id': '47690661-f343-4591-920c-50dcd59f74e2', 
        'created_date': '2020-05-28T00:00:00+00:00', 
        'updated_date': '2020-05-28T00:00:00+00:00', 
        'fk_sourcetype': 'fb64715d-09d1-4fd9-8912-685364c7d446'
        }
   
# given a false id, expecting a 404 error.
def test_get_inexistent_device_id():
    res = client.get("/47690661-")
    assert res.status_code == 404
    print  (res.json())
    assert res.json() == {'detail': 'Not Found'}
