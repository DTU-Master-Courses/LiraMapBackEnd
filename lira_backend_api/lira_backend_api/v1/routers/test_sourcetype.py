from fastapi.testclient import TestClient
import json
from lira_backend_api.main import app
client = TestClient(app)


def test_get_single_source():
    res = client.get("/sourcetype/id/dae3115a-7bff-434c-8a77-e6672ebc7599")
   
    print  (res.json())
    print (res.status_code)
    assert res.status_code == 404