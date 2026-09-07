from typing import Any

class ConversationRepository:
    async def create_conversation(self, user_id: int | None = None, title: str | None = None) -> int:
        raise NotImplementedError('Implemente seu INSERT em ai_conversations.')

    async def add_message(self, conversation_id: int, role: str, content: str, metadata: dict[str, Any] | None = None) -> int:
        raise NotImplementedError('Implemente seu INSERT em ai_messages.')

    async def get_messages(self, conversation_id: int, limit: int = 50) -> list[dict[str, Any]]:
        raise NotImplementedError('Implemente seu SELECT em ai_messages.')
