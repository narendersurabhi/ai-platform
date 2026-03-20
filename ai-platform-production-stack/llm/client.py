"""LLM client abstraction supporting OpenAI and a local mock model."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class LLMResult:
    text: str
    token_usage: int


class LLMClient:
    def __init__(self, provider: str = "mock") -> None:
        self.provider = provider

    def generate(self, prompt: str) -> LLMResult:
        if self.provider == "openai" and os.getenv("OPENAI_API_KEY"):
            # Production hook placeholder.
            text = "[OpenAI output placeholder] " + prompt[:180]
        else:
            text = "[Mock model] Based on retrieved evidence, this claim was flagged due to policy inconsistency."
        token_usage = max(1, len(prompt.split()) + len(text.split()))
        return LLMResult(text=text, token_usage=token_usage)
