"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)


class AskResponse(BaseModel):
    answer: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    sources: list[str]
