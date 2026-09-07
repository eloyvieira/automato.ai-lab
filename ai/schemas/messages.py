from typing import Any, Literal
from pydantic import BaseModel, Field

Role = Literal['system', 'user', 'assistant']

class ChatMessage(BaseModel):
    role: Role
    content: str

class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

class LLMResult(BaseModel):
    text: str = ''
    tool_calls: list[ToolCall] = Field(default_factory=list)
    provider: str
    model: str
    response_id: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    raw: Any = None
