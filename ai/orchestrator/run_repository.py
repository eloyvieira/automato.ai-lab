from typing import Any

class RunRepository:
    async def save_run(self, payload: dict[str, Any]) -> int:
        raise NotImplementedError('Implemente INSERT em ai_runs se quiser persistir custos/latência/tokens.')

    async def save_tool_call(self, run_id: int, payload: dict[str, Any]) -> int:
        raise NotImplementedError('Implemente INSERT em ai_tool_calls se quiser auditoria completa.')
