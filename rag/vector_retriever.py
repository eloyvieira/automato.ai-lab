from typing import Any
from rag.base import Retriever

class VectorRetriever(Retriever):
    async def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """Stub para Qdrant/pgvector/Pinecone/etc."""
        raise NotImplementedError('Implemente um vector database quando chegar nessa fase do lab.')
