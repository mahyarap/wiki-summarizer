import logging

from langchain.agents import (
    AgentType,
    Tool,
    initialize_agent,  # type: ignore[reportUnknownVariableType]
)
from langchain.agents.agent import AgentExecutor
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import OpenAI

from .config import Settings

logger = logging.getLogger(__name__)


def create_agent(settings: Settings) -> AgentExecutor:
    llm = OpenAI(temperature=0, api_key=settings.openai_api_key)
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())  # type: ignore[reportCallIssue]

    tools = [
        Tool(
            name="Wikipedia",
            func=wiki.run,
            description="Use this tool to search Wikipedia and get a summary.",
        )
    ]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )


def get_agent(settings: Settings) -> AgentExecutor:
    return create_agent(settings)


def summarize_topic(topic: str, agent: AgentExecutor) -> str:
    """Summarize a topic using the provided agent."""
    logger.info("Summarizing topic: %s", topic)
    result = agent.invoke({"input": f"Summarize the topic '{topic}' using Wikipedia."})
    logger.debug("Agent response: %s", result)
    return result["output"]
