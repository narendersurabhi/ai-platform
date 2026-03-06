"""API route definitions."""
from fastapi import APIRouter

from agents.orchestrator import AgentOrchestrator
from api.schemas import AskRequest, AskResponse


def build_router(orchestrator: AgentOrchestrator) -> APIRouter:
    router = APIRouter()

    @router.post("/ask", response_model=AskResponse)
    def ask(request: AskRequest) -> AskResponse:
        result = orchestrator.handle(request.question)
        return AskResponse(answer=result.answer, confidence_score=result.confidence_score, sources=result.sources)

    return router
