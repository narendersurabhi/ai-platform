# ai-platform-production-stack

Production-style reference repository for AI platform engineering teams building reliable LLM applications.

## Motivation
This repo demonstrates a clean, modular architecture for:
- RAG-backed question answering.
- Agentic orchestration.
- Evaluation and quality gates.
- Observability and experiment tracking.
- CI/CD and deployment with Kubernetes + Argo.

## Architecture
```text
User Request
   ↓
API Gateway (FastAPI)
   ↓
Agent Orchestrator
   ↓
Retriever (Vector Search)
   ↓
LLM Generation
   ↓
Evaluation Harness
   ↓
Observability + Metrics
   ↓
Response
```

Offline:
```text
Dataset → Argo Workflow → Evaluation Runner → Quality Gate → Model Promotion
```

## Components
- `api/`: FastAPI gateway and request/response schemas.
- `agents/`: planner, reasoning, and orchestrator agents.
- `retrieval/`: embeddings, vector store, retriever/index builder.
- `llm/`: provider abstraction, prompts, and response parsing.
- `evaluation/`: metrics, hallucination checks, runner, and quality gate.
- `observability/`: JSON logging and telemetry.
- `experiments/`: MLflow tracking.
- `pipelines/`: Argo workflow and training pipeline spec.
- `deploy/`: Docker + Kubernetes manifests.
- `tests/`: unit tests.

## Local Run
```bash
pip install -r requirements.txt
uvicorn api.server:app --reload
```

Request example:
```bash
curl -X POST localhost:8000/ask -H "content-type: application/json" -d '{"question": "Why was this claim flagged?"}'
```

## Run Tests
```bash
pytest -q
```

## Run Evaluation
```bash
python -c "from evaluation.runner import EvaluationRunner; from llm.client import LLMClient; print(EvaluationRunner(LLMClient()).run('datasets/rag_eval_dataset.json'))"
```

## Docker
```bash
docker build -f deploy/dockerfile -t ai-platform-production-stack .
docker run -p 8000:8000 ai-platform-production-stack
```

## Kubernetes
```bash
kubectl apply -f deploy/k8s_deployment.yaml
kubectl apply -f deploy/k8s_service.yaml
```

## Argo Workflow
```bash
kubectl apply -f pipelines/argo_evaluation_workflow.yaml
argo submit --watch pipelines/argo_evaluation_workflow.yaml
```

## Quality Gate
Thresholds in `evaluation/quality_gate.py`:
- `accuracy >= 0.90`
- `hallucination_rate < 0.05`
