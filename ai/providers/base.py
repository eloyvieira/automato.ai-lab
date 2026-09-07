from abc import ABC, abstractmethod
from typing import Any
from ai.schemas.messages import ChatMessage, LLMResult

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None, previous_response_id: str | None = None) -> LLMResult:
        raise NotImplementedError
