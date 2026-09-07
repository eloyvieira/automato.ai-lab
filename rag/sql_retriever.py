from typing import Any
from rag.base import Retriever

class SQLRetriever(Retriever):
    async def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """Implemente aqui sua recuperação estruturada via SQL.
        `query` pode ser usado como intenção textual e `filters` como filtros já interpretados.
        Não gere SQL livre vindo da LLM sem validação.
        """
        raise NotImplementedError('Adicione sua estratégia SQL em rag/sql_retriever.py')
