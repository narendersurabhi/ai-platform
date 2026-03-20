"""Vector store abstraction with FAISS optional support and numpy fallback."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

try:
    import faiss  # type: ignore
except Exception:  # pragma: no cover
    faiss = None


@dataclass
class VectorStore:
    dim: int
    ids: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._matrix = np.empty((0, self.dim), dtype="float32")
        self._index = faiss.IndexFlatIP(self.dim) if faiss else None

    def build_index(self, embeddings: list[np.ndarray], ids: list[str], docs: list[str]) -> None:
        self.ids = ids
        self.docs = docs
        self._matrix = np.vstack(embeddings).astype("float32") if embeddings else np.empty((0, self.dim), dtype="float32")
        if self._index is not None:
            self._index.reset()
            if len(self._matrix):
                self._index.add(self._matrix)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> list[dict[str, str | float]]:
        if len(self._matrix) == 0:
            return []
        q = query_embedding.astype("float32").reshape(1, -1)
        if self._index is not None:
            scores, indices = self._index.search(q, top_k)
            idxs = indices[0]
            sims = scores[0]
        else:
            sims = (self._matrix @ q.T).flatten()
            idxs = np.argsort(-sims)[:top_k]
        results = []
        for i, score in zip(idxs, sims):
            if i < 0 or i >= len(self.docs):
                continue
            results.append({"id": self.ids[int(i)], "document": self.docs[int(i)], "score": float(score)})
        return results
