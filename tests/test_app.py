from collections.abc import Generator
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from langchain.agents.agent import AgentExecutor

from app.deps import get_agent
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def agent() -> Generator[Mock, Any, Any]:
    agent = Mock(spec=AgentExecutor)
    app.dependency_overrides[get_agent] = lambda: agent
    yield agent
    app.dependency_overrides.clear()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_info(client: TestClient) -> None:
    response = client.get("/info")
    assert response.status_code == 200
    assert "agent" in response.json()


def test_summarize_valid(client: TestClient, agent: Mock) -> None:
    agent.invoke.return_value = {"output": "Python is a programming language."}
    response = client.post("/summarize", json={"topic": "Python"})
    assert response.status_code == 200
    assert "Python" in response.json()["summary"]


def test_summarize_with_agent_error(client: TestClient, agent: Mock) -> None:
    agent.invoke.side_effect = RuntimeError("agent failed")
    with pytest.raises(RuntimeError, match="agent failed"):
        client.post("/summarize", json={"topic": "AI"})
