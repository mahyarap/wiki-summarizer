import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.functional
def test_summarize_endpoint_real_agent(client: TestClient):
    topic = "Alan Turing"
    response = client.post("/summarize", json={"topic": topic})

    assert response.status_code == 200, response.text
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert "Turing" in data["summary"] or "computer" in data["summary"]
