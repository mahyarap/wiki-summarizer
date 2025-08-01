from unittest.mock import Mock

import pytest
from langchain.agents.agent import AgentExecutor

from app.agent import summarize_topic


@pytest.fixture
def agent() -> Mock:
    mck = Mock(spec=AgentExecutor)
    mck.invoke.return_value = {"output": "Mocked summary"}
    return mck


def test_summarize_topic(agent: Mock) -> None:
    topic = "Python programming language"
    summary = summarize_topic(topic, agent)
    assert summary == "Mocked summary"
    agent.invoke.assert_called_once_with(
        {"input": f"Summarize the topic '{topic}' using Wikipedia."}
    )
