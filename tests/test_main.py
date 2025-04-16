"""
Tests for the main application routes.
"""
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """
    Test the root endpoint.
    
    Args:
        client: TestClient fixture
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_health_check_endpoint(client: TestClient):
    """
    Test the health check endpoint.
    
    Args:
        client: TestClient fixture
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy" 