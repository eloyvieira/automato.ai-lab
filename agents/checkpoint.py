from typing import Any
from langgraph.checkpoint.memory import InMemorySaver
from core.config import get_settings


def get_checkpointer() -> Any:
    """Factory do checkpointer LangGraph.

    `memory` é zero-config para o laboratório. Para produção, adicione um
    adapter persistente sem alterar o grafo ou o serviço do agente.
    """
    backend = get_settings().langgraph_memory_backend.lower().strip()
    if backend == 'memory':
        return InMemorySaver()
    raise ValueError(f'LANGGRAPH_MEMORY_BACKEND não suportado: {backend}')
