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
        "species": "Test Species",
        "location": "Test Location",
        "watering_frequency": 7,
        "last_watered": "2024-03-20T00:00:00"
    }
    response = client.post("/plants/", json=plant_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["species"] == plant_data["species"]
    assert "id" in data

def test_get_plants(client):
    """Test getting all plants."""
    response = client.get("/plants/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_plant(client):
    """Test getting a specific plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "species": "Test Species",
        "location": "Test Location",
        "watering_frequency": 7,
        "last_watered": "2024-03-20T00:00:00"
    }
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    # Then get the plant
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == plant_data["name"]
    assert data["species"] == plant_data["species"]

def test_update_plant(client):
    """Test updating a plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "species": "Test Species",
        "location": "Test Location",
        "watering_frequency": 7,
        "last_watered": "2024-03-20T00:00:00"
    }
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    # Update the plant
    update_data = {
        "name": "Updated Plant",
        "species": "Updated Species",
        "location": "Updated Location",
        "watering_frequency": 14,
        "last_watered": "2024-03-20T00:00:00"
    }
    response = client.put(f"/plants/{plant_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["species"] == update_data["species"]

def test_delete_plant(client):
    """Test deleting a plant."""
    # First create a plant
    plant_data = {
        "name": "Test Plant",
        "species": "Test Species",
        "location": "Test Location",
        "watering_frequency": 7,
        "last_watered": "2024-03-20T00:00:00"
    }
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    
    # Delete the plant
    response = client.delete(f"/plants/{plant_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the plant is deleted
    get_response = client.get(f"/plants/{plant_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 