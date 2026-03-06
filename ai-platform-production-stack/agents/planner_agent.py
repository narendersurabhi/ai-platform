"""Planner agent chooses tools and workflow."""
from dataclasses import dataclass


@dataclass
class Plan:
    use_retrieval: bool
    reasoning_style: str


class PlannerAgent:
    def plan(self, question: str) -> Plan:
        needs_retrieval = any(k in question.lower() for k in ["why", "evidence", "flagged", "source"])
        style = "chain_of_thought_summary" if needs_retrieval else "direct"
        return Plan(use_retrieval=needs_retrieval, reasoning_style=style)
