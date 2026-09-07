import json
from typing import Any
from langchain_core.tools import StructuredTool
from rag.service import RAGService
from core.config import get_settings

RAG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'query': {'type': 'string', 'description': 'O que deve ser procurado no conhecimento/histórico.'},
        'filters': {'type': ['object', 'null'], 'description': 'Filtros estruturados opcionais.'},
        'limit': {'type': 'integer', 'minimum': 1, 'maximum': 100},
    },
    'required': ['query', 'filters', 'limit'],
}


async def _search_knowledge(query: str, filters: dict[str, Any] | None = None, limit: int | None = None) -> str:
    s = get_settings()
    service = RAGService()
    result = await service.retrieve(query=query, filters=filters, limit=limit or s.rag_default_limit)
    return json.dumps({'ok': True, 'results': result}, ensure_ascii=False, default=str)


def get_rag_tool() -> StructuredTool:
    """RAG como uma tool explícita; a LLM decide quando aprofundar a busca."""
    return StructuredTool(
        name='search_knowledge',
        description='Busca conhecimento ou casos históricos relevantes quando os dados objetivos das tools não forem suficientes.',
        args_schema=RAG_SCHEMA,
        coroutine=_search_knowledge,
    )
