import pytest
from fastapi import status

def test_read_main(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

def test_create_plant(client):
    """Test creating a new plant."""
    plant_data = {
        "name": "Test Plant",
        "type": "Test Type",
        "water_frequency": "Every 2 days",
        "sunlight_requirements": "Full Sun",
        "notes": "Test notes"
    }
    response = client.post("/plants", json=plant_data)
    if response.status_code != status.HTTP_200_OK:
        print(f"Response content: {response.content}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["type"] == plant_data["type"]
    assert "id" in data

def test_get_plants(client):
    """Test getting all plants."""
    response = client.get("/plants")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_plant(client):
    """Test getting a specific plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "type": "Test Type",
        "water_frequency": "Every 2 days",
        "sunlight_requirements": "Full Sun",
        "notes": "Test notes"
    }
    create_response = client.post("/plants", json=plant_data)
    if create_response.status_code != status.HTTP_200_OK:
        print(f"Response content: {create_response.content}")
    assert create_response.status_code == status.HTTP_200_OK
    plant_id = create_response.json()["id"]
    
    # Then get the plant
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["type"] == plant_data["type"]

def test_update_plant(client):
    """Test updating a plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "type": "Test Type",
        "water_frequency": "Every 2 days",
        "sunlight_requirements": "Full Sun",
        "notes": "Test notes"
    }
    create_response = client.post("/plants", json=plant_data)
    if create_response.status_code != status.HTTP_200_OK:
        print(f"Response content: {create_response.content}")
    assert create_response.status_code == status.HTTP_200_OK
    plant_id = create_response.json()["id"]
    
    # Update the plant
    update_data = {
        "name": "Updated Plant",
        "type": "Updated Type",
        "water_frequency": "Every 3 days",
        "sunlight_requirements": "Partial Sun",
        "notes": "Updated notes"
    }
    response = client.put(f"/plants/{plant_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["type"] == update_data["type"]

def test_delete_plant(client):
    """Test deleting a plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "type": "Test Type",
        "water_frequency": "Every 2 days",
        "sunlight_requirements": "Full Sun",
        "notes": "Test notes"
    }
    create_response = client.post("/plants", json=plant_data)
    if create_response.status_code != status.HTTP_200_OK:
        print(f"Response content: {create_response.content}")
    assert create_response.status_code == status.HTTP_200_OK
    plant_id = create_response.json()["id"]
    
    # Delete the plant
    response = client.delete(f"/plants/{plant_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    
    # Verify the plant is deleted
    get_response = client.get(f"/plants/{plant_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 