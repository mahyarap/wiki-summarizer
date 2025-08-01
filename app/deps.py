from functools import lru_cache

from fastapi import Depends
from langchain.agents.agent import AgentExecutor

from .agent import create_agent
from .config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[reportCallIssue]


def get_agent(settings: Settings = Depends(get_settings)) -> AgentExecutor:
    return create_agent(settings)
