"""Retriever implementation: query -> embedding -> vector search -> top_k docs."""
from __future__ import annotations

from dataclasses import dataclass

from retrieval.embeddings import EmbeddingModel
from retrieval.vector_store import VectorStore


@dataclass
class Retriever:
    embedding_model: EmbeddingModel
    vector_store: VectorStore

    @classmethod
    def with_seed_docs(cls, documents: dict[str, str], dim: int = 128) -> "Retriever":
        model = EmbeddingModel(dim=dim)
        store = VectorStore(dim=dim)
        ids = list(documents.keys())
        docs = list(documents.values())
        embeds = [model.embed(d) for d in docs]
        store.build_index(embeds, ids, docs)
        return cls(embedding_model=model, vector_store=store)

    def retrieve(self, query: str, top_k: int = 3) -> list[dict[str, str | float]]:
        q_emb = self.embedding_model.embed(query)
        return self.vector_store.search(q_emb, top_k=top_k)
