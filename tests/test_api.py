from fastapi.testclient import TestClient
from app.main import app

# Create a test client that can make simulated requests to our FastAPI app
client = TestClient(app)

def test_read_root():
    """Tests if the main landing route returns 200 OK and the welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Resume Analyzer API!"}

def test_health_check():
    """Tests if the health route successfully connects and returns database status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()