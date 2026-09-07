import json
from typing import Any
from openai import AsyncOpenAI
from ai.providers.base import LLMProvider
from ai.schemas.messages import ChatMessage, LLMResult, ToolCall
from core.config import get_settings

class OpenAIProvider(LLMProvider):
    def __init__(self):
        s = get_settings()
        self.model = s.openai_model
        self.max_output_tokens = s.openai_max_output_tokens
        self.client = AsyncOpenAI(api_key=s.openai_api_key)

    async def chat(self, messages: list[ChatMessage], tools: list[dict[str, Any]] | None = None, previous_response_id: str | None = None) -> LLMResult:
        input_items = [{'role': m.role, 'content': m.content} for m in messages]
        kwargs: dict[str, Any] = {
            'model': self.model,
            'input': input_items,
            'max_output_tokens': self.max_output_tokens,
        }
        if tools:
            kwargs['tools'] = tools
            kwargs['tool_choice'] = 'auto'
            kwargs['parallel_tool_calls'] = True
        if previous_response_id:
            kwargs['previous_response_id'] = previous_response_id
        response = await self.client.responses.create(**kwargs)
        calls: list[ToolCall] = []
        for item in response.output:
            if getattr(item, 'type', None) == 'function_call':
                raw_args = getattr(item, 'arguments', '{}') or '{}'
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError:
                    args = {}
                calls.append(ToolCall(id=item.call_id, name=item.name, arguments=args))
        usage = getattr(response, 'usage', None)
        return LLMResult(
            text=getattr(response, 'output_text', '') or '',
            tool_calls=calls,
            provider='openai',
            model=self.model,
            response_id=response.id,
            input_tokens=getattr(usage, 'input_tokens', None) if usage else None,
            output_tokens=getattr(usage, 'output_tokens', None) if usage else None,
            raw=response,
        )

    async def submit_tool_outputs(self, response_id: str, outputs: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> LLMResult:
        input_items = [{'type': 'function_call_output', 'call_id': x['call_id'], 'output': json.dumps(x['output'], ensure_ascii=False, default=str)} for x in outputs]
        kwargs: dict[str, Any] = {
            'model': self.model,
            'previous_response_id': response_id,
            'input': input_items,
            'max_output_tokens': self.max_output_tokens,
        }
        if tools:
            kwargs['tools'] = tools
            kwargs['tool_choice'] = 'auto'
            kwargs['parallel_tool_calls'] = True
        response = await self.client.responses.create(**kwargs)
        calls: list[ToolCall] = []
        for item in response.output:
            if getattr(item, 'type', None) == 'function_call':
                try:
                    args = json.loads(getattr(item, 'arguments', '{}') or '{}')
                except json.JSONDecodeError:
                    args = {}
                calls.append(ToolCall(id=item.call_id, name=item.name, arguments=args))
        usage = getattr(response, 'usage', None)
        return LLMResult(
            text=getattr(response, 'output_text', '') or '', tool_calls=calls, provider='openai', model=self.model,
            response_id=response.id, input_tokens=getattr(usage, 'input_tokens', None) if usage else None,
            output_tokens=getattr(usage, 'output_tokens', None) if usage else None, raw=response,
        )
