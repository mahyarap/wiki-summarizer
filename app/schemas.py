from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    topic: str


class SummarizeResponse(BaseModel):
    summary: str
