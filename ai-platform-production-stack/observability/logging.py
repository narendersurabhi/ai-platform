"""Structured JSON logging utilities."""
import json
import logging
from datetime import datetime, timezone
from typing import Any


logger = logging.getLogger("ai_platform")
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log_event(event_type: str, payload: dict[str, Any]) -> None:
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    logger.info(json.dumps(record, default=str))
