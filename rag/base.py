from abc import ABC, abstractmethod
from typing import Any

class Retriever(ABC):
    @abstractmethod
    async def search(self, query: str, filters: dict[str, Any] | None = None, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError
