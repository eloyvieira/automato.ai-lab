import logging
from typing import Any

logger = logging.getLogger('ai_lab.agent')


def log_agent_event(event: str, payload: dict[str, Any] | None = None) -> None:
    """Ponto único para plugar LangSmith/OpenTelemetry futuramente."""
    logger.info('agent_event=%s payload=%s', event, payload or {})
