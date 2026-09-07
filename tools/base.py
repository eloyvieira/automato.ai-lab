from dataclasses import dataclass
from typing import Any, Awaitable, Callable

ToolHandler = Callable[..., Awaitable[Any]]

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: ToolHandler

    def openai_schema(self) -> dict[str, Any]:
        return {
            'type': 'function',
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters,
            'strict': True,
        }
