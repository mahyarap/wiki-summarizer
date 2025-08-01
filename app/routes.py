from fastapi import APIRouter, Depends
from langchain.agents.agent import AgentExecutor

from .agent import summarize_topic
from .deps import get_agent
from .schemas import SummarizeRequest, SummarizeResponse

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/info")
def info() -> dict[str, str]:
    return {"agent": "Wikipedia summarizer"}


@router.post("/summarize")
def summarize(
    request: SummarizeRequest,
    agent: AgentExecutor = Depends(get_agent),
) -> SummarizeResponse:
    summary = summarize_topic(request.topic, agent)
    return SummarizeResponse(summary=summary)
