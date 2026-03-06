"""Embedding utilities with deterministic local embeddings for demo/testing."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np


@dataclass
class EmbeddingModel:
    dim: int = 128

    def embed(self, text: str) -> np.ndarray:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(digest[:8], "little")
        rng = np.random.default_rng(seed)
        vec = rng.normal(size=self.dim)
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec
