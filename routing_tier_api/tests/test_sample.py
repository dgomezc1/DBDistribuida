
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to ds-node-silin-api | Version: 0.1.0"
    }
