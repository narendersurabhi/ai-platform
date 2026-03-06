"""Prompt templates for generation."""


def build_rag_prompt(question: str, contexts: list[str]) -> str:
    context_block = "\n".join(f"- {ctx}" for ctx in contexts)
    return (
        "You are a reliable AI assistant. Answer the user's question using only the evidence.\n"
        f"Question: {question}\n"
        f"Evidence:\n{context_block}\n"
        "Return a concise explanation and mention uncertainty when needed."
    )
