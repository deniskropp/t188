from fastapi.testclient import TestClient
from src.dashboard.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "MetaCognito Dashboard" in response.text

def test_api_graph():
    response = client.get("/api/graph")
    assert response.status_code == 200
    data = response.json()
    assert "elements" in data
    assert isinstance(data["elements"], list)

def test_api_chat():
    response = client.post("/api/chat", json={"message": "Test message"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0
