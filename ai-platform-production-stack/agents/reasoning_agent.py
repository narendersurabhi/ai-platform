"""Reasoning agent synthesizes final explanations."""
from dataclasses import dataclass


@dataclass
class ReasoningResult:
    answer: str
    confidence_score: float


class ReasoningAgent:
    def synthesize(self, question: str, context_docs: list[str], llm_answer: str) -> ReasoningResult:
        confidence = min(0.99, 0.6 + 0.1 * len(context_docs))
        if not context_docs:
            confidence = 0.5
        answer = f"{llm_answer}\n\nEvidence summary: {' | '.join(context_docs) if context_docs else 'No external evidence.'}"
        return ReasoningResult(answer=answer, confidence_score=round(confidence, 2))
