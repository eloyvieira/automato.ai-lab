from pydantic import BaseModel, Field
from ai.schemas.messages import ChatMessage

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)

class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: list[dict] = Field(default_factory=list)
    latency_ms: float

class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: str | None = None

class AgentChatResponse(BaseModel):
    answer: str
    thread_id: str
    provider: str
    model: str
    latency_ms: float
