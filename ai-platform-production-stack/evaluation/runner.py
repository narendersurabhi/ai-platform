"""Dataset-driven evaluation runner."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from experiments.mlflow_tracking import track_run
from llm.client import LLMClient
from llm.prompt_templates import build_rag_prompt
from evaluation.hallucination_detection import HallucinationDetector
from evaluation.metrics import correctness_score
from evaluation.quality_gate import QualityGate


@dataclass
class EvaluationSummary:
    accuracy: float
    hallucination_rate: float
    avg_latency_ms: float
    gate: str


class EvaluationRunner:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.detector = HallucinationDetector()
        self.gate = QualityGate()

    def run(self, dataset_path: str) -> EvaluationSummary:
        rows = json.loads(Path(dataset_path).read_text())
        correctness, hallucinations, latencies = [], [], []

        for row in rows:
            start = perf_counter()
            prompt = build_rag_prompt(row["question"], [row["context"]])
            response = self.llm_client.generate(prompt)
            latencies.append((perf_counter() - start) * 1000)
            correctness.append(correctness_score(response.text, row["expected_answer"]))
            hallucinations.append(1.0 if self.detector.run(response.text, row["context"]) else 0.0)

        accuracy = round(sum(correctness) / max(1, len(correctness)), 2)
        hallucination_rate = round(sum(hallucinations) / max(1, len(hallucinations)), 2)
        avg_latency = round(sum(latencies) / max(1, len(latencies)), 2)

        gate_result = self.gate.check(accuracy, hallucination_rate)
        track_run(
            params={"model_version": "mock-v1", "prompt_version": "rag-v1"},
            metrics={"accuracy": accuracy, "hallucination_rate": hallucination_rate, "avg_latency_ms": avg_latency},
        )
        return EvaluationSummary(
            accuracy=accuracy,
            hallucination_rate=hallucination_rate,
            avg_latency_ms=avg_latency,
            gate=gate_result.reason,
        )


if __name__ == "__main__":
    summary = EvaluationRunner(LLMClient(provider="mock")).run("datasets/rag_eval_dataset.json")
    print(summary)
