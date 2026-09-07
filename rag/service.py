from typing import Any
from rag.base import Retriever
from rag.sql_retriever import SQLRetriever

class RAGService:
    def __init__(self, retriever: Retriever | None = None):
        self.retriever = retriever or SQLRetriever()

    async def retrieve(self, query: str, filters: dict[str, Any] | None = None, limit: int = 20) -> list[dict[str, Any]]:
        return await self.retriever.search(query=query, filters=filters, limit=limit)
