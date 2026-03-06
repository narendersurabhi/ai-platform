"""FastAPI entrypoint for AI platform gateway."""
from fastapi import FastAPI

from agents.orchestrator import AgentOrchestrator
from api.routes import build_router
from llm.client import LLMClient
from retrieval.retriever import Retriever

SEED_DOCS = {
    "policy-101": "Claim flagged because cited source conflicts with approved policy language.",
    "audit-202": "Historical reviews found unsupported statements in similar submissions.",
    "rule-330": "Automated checks detect unverifiable claims and route them for manual validation.",
}


def create_app() -> FastAPI:
    retriever = Retriever.with_seed_docs(SEED_DOCS)
    orchestrator = AgentOrchestrator(retriever=retriever, llm_client=LLMClient(provider="mock"))
    app = FastAPI(title="AI Platform Production Stack")
    app.include_router(build_router(orchestrator))
    return app


app = create_app()
