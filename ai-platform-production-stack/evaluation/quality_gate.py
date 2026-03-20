"""Quality gate for model promotion decisions."""
from dataclasses import dataclass


@dataclass
class QualityGateResult:
    passed: bool
    reason: str


class QualityGate:
    min_accuracy: float = 0.90
    max_hallucination_rate: float = 0.05

    def check(self, accuracy: float, hallucination_rate: float) -> QualityGateResult:
        passed = accuracy >= self.min_accuracy and hallucination_rate < self.max_hallucination_rate
        reason = "PASS" if passed else "FAIL"
        return QualityGateResult(passed=passed, reason=reason)
