from typing import Any
from ai.providers.base import LLMProvider
from ai.schemas.messages import ChatMessage, LLMResult

class GeminiProvider(LLMProvider):
    async def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None, previous_response_id: str | None = None) -> LLMResult:
        raise NotImplementedError('Implemente aqui a API do Gemini mantendo a mesma interface LLMProvider.')
