import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange
    # (No setup needed, using in-memory DB)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_valid():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/signup", params={"email": "removeme@mergington.edu"})
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_root_redirect():
    # Arrange
    # (No setup needed)
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200 or response.status_code == 307  # FastAPI TestClient may follow redirect
