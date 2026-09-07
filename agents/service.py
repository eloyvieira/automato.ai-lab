import time
import uuid
from typing import Any
from langchain_core.messages import AIMessage, HumanMessage
from agents.graph import get_agent_graph
from core.config import get_settings
from observability.agent_events import log_agent_event


class LangGraphAgentService:
    """API de alto nível para o agente LangGraph, sem substituir o fluxo legado."""
    def __init__(self):
        self.graph = get_agent_graph()
        self.settings = get_settings()

    async def ask(self, message: str, thread_id: str | None = None) -> dict[str, Any]:
        thread_id = thread_id or str(uuid.uuid4())
        started = time.perf_counter()
        log_agent_event('run.started', {'thread_id': thread_id, 'provider': self.settings.llm_provider})
        config = {
            'configurable': {'thread_id': thread_id},
            'recursion_limit': self.settings.langgraph_recursion_limit,
        }
        result = await self.graph.ainvoke({'messages': [HumanMessage(content=message)]}, config=config)
        messages = result.get('messages', [])
        final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and m.content), None)
        answer = final.content if final else ''
        if isinstance(answer, list):
            answer = ''.join(str(x.get('text', x)) if isinstance(x, dict) else str(x) for x in answer)
        payload = {
            'answer': str(answer),
            'thread_id': thread_id,
            'provider': self.settings.llm_provider,
            'model': self._model_name(),
            'latency_ms': round((time.perf_counter() - started) * 1000, 2),
        }
        log_agent_event('run.completed', {'thread_id': thread_id, 'latency_ms': payload['latency_ms']})
        return payload

    def _model_name(self) -> str:
        if self.settings.llm_provider.lower() == 'openai':
            return self.settings.openai_model
        if self.settings.llm_provider.lower() == 'gemini':
            return self.settings.gemini_model
        return ''
