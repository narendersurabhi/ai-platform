"""Evaluation metrics for correctness, hallucination, and latency."""
from __future__ import annotations


def correctness_score(answer: str, expected_answer: str) -> float:
    overlap = set(answer.lower().split()) & set(expected_answer.lower().split())
    base = max(1, len(set(expected_answer.lower().split())))
    return round(len(overlap) / base, 2)


def hallucination_detected(answer: str, context: str) -> bool:
    context_words = set(context.lower().split())
    answer_words = set(answer.lower().split())
    unsupported = [w for w in answer_words if len(w) > 5 and w not in context_words]
    return len(unsupported) > 8
