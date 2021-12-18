from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    """Test somethings
    """
    response = client.get("/api/v1/sample")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_read_main1():
    """Test somethings
    """
    response = client.get("/api/v1/sample")
    assert response.status_code == 400
    assert response.json() == {"hello": "pass"}
