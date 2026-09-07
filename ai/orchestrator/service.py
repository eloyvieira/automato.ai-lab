import time
from typing import Any
from ai.providers.factory import get_llm_provider
from ai.providers.openai_provider import OpenAIProvider
from ai.prompts.system import SYSTEM_PROMPT
from ai.schemas.messages import ChatMessage
from core.config import get_settings
from tools.registry import execute_tool, get_openai_tools

class AIOrchestrator:
    def __init__(self):
        self.provider = get_llm_provider()
        self.settings = get_settings()

    async def ask(self, user_message: str, history: list[ChatMessage] | None = None) -> dict[str, Any]:
        messages = [ChatMessage(role='system', content=SYSTEM_PROMPT)]
        if history: messages.extend(history)
        messages.append(ChatMessage(role='user', content=user_message))
        tools = get_openai_tools()
        started = time.perf_counter()
        result = await self.provider.chat(messages=messages, tools=tools)
        total_input = result.input_tokens or 0
        total_output = result.output_tokens or 0
        executed: list[dict[str, Any]] = []
        iterations = 0

        while result.tool_calls:
            iterations += 1
            if iterations > self.settings.max_tool_iterations:
                raise RuntimeError('Limite de iterações de tools atingido.')
            outputs = []
            for call in result.tool_calls:
                try:
                    value = await execute_tool(call.name, call.arguments)
                    outputs.append({'call_id': call.id, 'output': {'ok': True, 'data': value}})
                    executed.append({'tool': call.name, 'arguments': call.arguments, 'ok': True})
                except Exception as exc:
                    outputs.append({'call_id': call.id, 'output': {'ok': False, 'error': str(exc)}})
                    executed.append({'tool': call.name, 'arguments': call.arguments, 'ok': False, 'error': str(exc)})
            if not isinstance(self.provider, OpenAIProvider):
                raise NotImplementedError('Implemente submit_tool_outputs no adapter do provider alternativo.')
            result = await self.provider.submit_tool_outputs(result.response_id, outputs, tools=tools)
            total_input += result.input_tokens or 0
            total_output += result.output_tokens or 0

        return {
            'answer': result.text,
            'provider': result.provider,
            'model': result.model,
            'input_tokens': total_input,
            'output_tokens': total_output,
            'tool_calls': executed,
            'latency_ms': round((time.perf_counter() - started) * 1000, 2),
        }
