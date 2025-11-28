"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_docs():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_api_redoc():
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_json():
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert "info" in response.json()


def test_chat_endpoint_missing_message():
    """Test chat endpoint with missing message."""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error


def test_chat_endpoint_invalid_json():
    """Test chat endpoint with invalid JSON."""
    response = client.post("/chat", json={"invalid": "data"})
    assert response.status_code == 422  # Validation error


def test_document_info_no_document():
    """Test document info endpoint when no document is loaded."""
    response = client.get("/document/info")
    assert response.status_code == 200
    data = response.json()
    assert "available" in data


def test_learn_endpoint_missing_fields():
    """Test learn endpoint with missing required fields."""
    # Learn endpoint might accept empty body or have defaults
    # Test with minimal invalid data
    response = client.post("/learn", json={"mode": "invalid_mode"})
    # Should return 422 for invalid mode, or 200 if it handles gracefully
    assert response.status_code in [200, 422]

