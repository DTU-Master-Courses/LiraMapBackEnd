from lira_backend_api.v1.tests.conftest import *


@pytest.mark.anyio
def test_get_single_source():
    async def run_test(client):
        res = client.get("/sourcetype/id/8b195100-3c87-4912-a315-3fe2b9c32e1a")
        assert res.status_code == 200
