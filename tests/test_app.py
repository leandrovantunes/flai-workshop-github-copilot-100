import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_and_unregister():
    activity = "Soccer Team"
    email = "testuser@example.com"
    # Register
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Check participant added
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email in participants
    # Unregister
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Check participant removed
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email not in participants

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
