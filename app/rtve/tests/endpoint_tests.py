from fastapi.testclient import TestClient

from app.rtve.router import router #as router_rtve 
# 

client = TestClient(router)

def test_read_item():
    response = client.get("/ping")
    assert response.status_code == 200

