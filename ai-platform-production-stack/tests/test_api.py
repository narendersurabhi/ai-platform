from fastapi.testclient import TestClient

from api.server import create_app


def test_ask_endpoint_returns_structured_response() -> None:
    client = TestClient(create_app())
    payload = {"question": "Why was this claim flagged?"}
    resp = client.post("/ask", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body
    assert "confidence_score" in body
    assert isinstance(body["sources"], list)
