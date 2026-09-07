import json
from typing import Any
from langchain_core.tools import StructuredTool
from tools.registry import TOOLS, execute_tool


def _serialize(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _build_coroutine(tool_name: str):
    async def invoke(**kwargs: Any) -> str:
        result = await execute_tool(tool_name, kwargs)
        return _serialize({'ok': True, 'data': result})
    return invoke


def get_langchain_tools() -> list[StructuredTool]:
    """Adapta as Core Tools existentes sem alterar sua implementação."""
    output: list[StructuredTool] = []
    for definition in TOOLS.values():
        output.append(StructuredTool(
            name=definition.name,
            description=definition.description,
            args_schema=definition.parameters,
            coroutine=_build_coroutine(definition.name),
        ))
    return output
