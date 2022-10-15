from fastapi.testclient import TestClient
import json
from lira_backend_api.main import app
client = TestClient(app)

#422 error
def test_get_single_source():
    res = client.get("/sourcetype/id/8b195100-3c87-4912-a315-3fe2b9c32e1a")
    print  (res.json())
    print (res.status_code)
    assert res.status_code == 200