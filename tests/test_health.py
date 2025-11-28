"""
Basic health check tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    # Root endpoint may return HTML (frontend) or JSON (API)
    # Check if it's JSON, otherwise it's HTML frontend
    try:
        data = response.json()
        assert "version" in data or "message" in data
    except Exception:
        # If it's HTML (frontend), that's also valid
        assert "text/html" in response.headers.get("content-type", "")


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "rag_available" in data


