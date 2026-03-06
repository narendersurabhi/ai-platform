"""Hallucination detection helpers."""
from evaluation.metrics import hallucination_detected


class HallucinationDetector:
    def run(self, answer: str, context: str) -> bool:
        return hallucination_detected(answer, context)
