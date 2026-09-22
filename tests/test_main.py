from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_transfer_unauthorized():
    payload = {
        "account_id": "ACC_12345",
        "recipient_email": "user@example.com",
        "amount": 2500.0,
        "currency": "INR"
    }
    response = client.post("/api/v1/transfer", json=payload)
    assert response.status_code == 403 or response.status_code == 401

def test_transfer_authorized_success():
    payload = {
        "account_id": "ACC_12345",
        "recipient_email": "user@example.com",
        "amount": 2500.0,
        "currency": "INR"
    }
    headers = {"Authorization": "Bearer test-secure-token-123"}
    response = client.post("/api/v1/transfer", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PROCESSED"
    assert data["amount"] == 2500.0
