from backend.main import app  # Assuming app is defined in backend/main.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/db-check")
    assert response.status_code == 200
