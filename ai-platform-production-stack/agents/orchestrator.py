"""Agent orchestrator for end-to-end ask pipeline."""
from dataclasses import dataclass

from agents.planner_agent import PlannerAgent
from agents.reasoning_agent import ReasoningAgent
from llm.client import LLMClient
from llm.prompt_templates import build_rag_prompt
from llm.response_parser import parse_response
from observability.telemetry import TelemetryContext, TelemetryRecorder
from retrieval.retriever import Retriever


@dataclass
class OrchestratorResponse:
    answer: str
    confidence_score: float
    sources: list[str]


class AgentOrchestrator:
    def __init__(self, retriever: Retriever, llm_client: LLMClient) -> None:
        self.planner = PlannerAgent()
        self.reasoner = ReasoningAgent()
        self.retriever = retriever
        self.llm = llm_client

    def handle(self, question: str) -> OrchestratorResponse:
        telemetry = TelemetryRecorder()
        plan = self.planner.plan(question)
        retrieved = self.retriever.retrieve(question, top_k=3) if plan.use_retrieval else []
        contexts = [str(r["document"]) for r in retrieved]
        sources = [str(r["id"]) for r in retrieved]
        prompt = build_rag_prompt(question, contexts)
        llm_out = self.llm.generate(prompt)
        parsed = parse_response(llm_out.text)
        result = self.reasoner.synthesize(question, contexts, parsed.answer)

        telemetry.finalize(
            TelemetryContext(
                question=question,
                prompt=prompt,
                response=result.answer,
                token_usage=llm_out.token_usage,
                eval_score=result.confidence_score,
            )
        )
        return OrchestratorResponse(answer=result.answer, confidence_score=result.confidence_score, sources=sources)
