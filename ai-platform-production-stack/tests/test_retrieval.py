from retrieval.retriever import Retriever


def test_retrieval_returns_ranked_documents() -> None:
    retriever = Retriever.with_seed_docs({"a": "policy conflict evidence", "b": "unrelated weather update"})
    results = retriever.retrieve("Why policy conflict was flagged?", top_k=1)
    assert len(results) == 1
    assert results[0]["id"] in {"a", "b"}
