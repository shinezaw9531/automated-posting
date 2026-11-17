from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_validation_exceeds_200_chars():
    long_msg = "A" * 190 + " https://example.com"
    response = client.post("/posting", json={"message": long_msg})
    assert response.status_code == 422

def test_validation_missing_link():
    response = client.post("/posting", json={"message": "Hello world without a link"})
    assert response.status_code == 422

def test_validation_multiple_links():
    response = client.post("/posting", json={"message": "Two links https://a.com and https://b.com"})
    assert response.status_code == 422

def test_valid_posting_request():
    response = client.post(
        "/posting",
        json={"message": "Check out our latest business platform and grow your online visibility. https://example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) == 5
