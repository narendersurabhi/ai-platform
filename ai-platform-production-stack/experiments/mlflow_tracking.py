"""MLflow experiment tracking wrapper."""
from __future__ import annotations

import os
from typing import Any


def track_run(params: dict[str, Any], metrics: dict[str, float]) -> None:
    try:
        import mlflow  # type: ignore
    except Exception:
        return

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("ai-platform-production-stack")
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
