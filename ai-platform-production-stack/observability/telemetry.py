"""Telemetry capture for AI interactions."""
from dataclasses import dataclass
from time import perf_counter

from observability.logging import log_event


@dataclass
class TelemetryContext:
    question: str
    prompt: str = ""
    response: str = ""
    token_usage: int = 0
    eval_score: float = 0.0


class TelemetryRecorder:
    def __init__(self) -> None:
        self._start = perf_counter()

    def finalize(self, context: TelemetryContext) -> None:
        latency_ms = (perf_counter() - self._start) * 1000
        log_event(
            "request_telemetry",
            {
                "question": context.question,
                "prompt": context.prompt,
                "response": context.response,
                "token_usage": context.token_usage,
                "latency_ms": round(latency_ms, 2),
                "evaluation_score": context.eval_score,
            },
        )
