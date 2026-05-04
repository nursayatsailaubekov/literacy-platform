"""Tests for child profile endpoints."""
import pytest
from fastapi.testclient import TestClient


def get_auth_headers(client: TestClient, user_data: dict) -> dict:
    """Helper to get authentication headers."""
    response = client.post("/api/v1/auth/register", json=user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_child(client: TestClient, test_user_data, test_child_data):
    """Test creating a child profile."""
    headers = get_auth_headers(client, test_user_data)

    response = client.post(
        "/api/v1/children",
        json=test_child_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_child_data["name"]
    assert data["age"] == test_child_data["age"]
    assert data["level"] == 1
    assert data["xp"] == 0


def test_get_children(client: TestClient, test_user_data, test_child_data):
    """Test getting all children for a user."""
    headers = get_auth_headers(client, test_user_data)

    client.post("/api/v1/children", json=test_child_data, headers=headers)

    response = client.get("/api/v1/children", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_child_data["name"]


def test_update_child(client: TestClient, test_user_data, test_child_data):
    """Test updating a child profile."""
    headers = get_auth_headers(client, test_user_data)

    create_response = client.post(
        "/api/v1/children",
        json=test_child_data,
        headers=headers
    )
    child_id = create_response.json()["id"]

    update_data = {"name": "Updated Name"}
    response = client.put(
        f"/api/v1/children/{child_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


def test_delete_child(client: TestClient, test_user_data, test_child_data):
    """Test deleting a child profile."""
    headers = get_auth_headers(client, test_user_data)

    create_response = client.post(
        "/api/v1/children",
        json=test_child_data,
        headers=headers
    )
    child_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/children/{child_id}",
        headers=headers
    )
    assert response.status_code == 204

    get_response = client.get("/api/v1/children", headers=headers)
    assert len(get_response.json()) == 0


def test_child_ownership_validation(client: TestClient, test_user_data, test_child_data):
    """Test that users can only access their own children."""
    headers1 = get_auth_headers(client, test_user_data)

    user2_data = {
        "email": "user2@example.com",
        "password": "Password123!",
        "full_name": "User Two"
    }
    headers2 = get_auth_headers(client, user2_data)

    create_response = client.post(
        "/api/v1/children",
        json=test_child_data,
        headers=headers1
    )
    child_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/children/{child_id}",
        headers=headers2
    )
    assert response.status_code == 403
