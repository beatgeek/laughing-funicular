"""Tests for the FastAPI application."""
import pytest
from fastapi.testclient import TestClient


def test_app_imports():
    """Test that the app can be imported."""
    from app.app import app
    assert app is not None


def test_health_endpoint():
    """Test the health check endpoint."""
    from app.app import app
    client = TestClient(app)
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_index_page():
    """Test that the index page loads."""
    from app.app import app
    client = TestClient(app)
    
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    # Check for title in HTML
    assert "Content Journey Finder" in response.text or "text/html" in response.headers.get("content-type", "")


def test_models():
    """Test the data models."""
    from app.models import Content, Journey
    
    # Test Content model
    content = Content(
        title="Test Movie",
        content_type="movie",
        duration_minutes=120,
        rating=85.5,
        genres=["Action", "Adventure"],
        description="A test movie",
        year=2024
    )
    
    assert content.title == "Test Movie"
    assert content.content_type == "movie"
    assert content.duration_minutes == 120
    
    # Test Journey model
    journey = Journey(
        total_duration=240,
        contents=[content]
    )
    
    assert journey.total_duration == 240
    assert len(journey.contents) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
