from evaluation.runner import EvaluationRunner
from llm.client import LLMClient


def test_evaluation_runner_returns_summary() -> None:
    runner = EvaluationRunner(llm_client=LLMClient(provider="mock"))
    summary = runner.run("datasets/rag_eval_dataset.json")
    assert 0.0 <= summary.accuracy <= 1.0
    assert 0.0 <= summary.hallucination_rate <= 1.0
    assert summary.gate in {"PASS", "FAIL"}
