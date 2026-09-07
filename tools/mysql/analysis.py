from typing import Any

async def get_ai_analysis(start_date: str | None = None, end_date: str | None = None, decision: str | None = None, order_id: int | None = None, limit: int = 100) -> list[dict[str, Any]]:
    """Implemente o SELECT da sua tabela de análises de IA aqui."""
    raise NotImplementedError('Adicione seu SQL em tools/mysql/analysis.py:get_ai_analysis')

async def save_ai_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    """Opcional: implemente INSERT da análise. Mantenha desabilitado se quiser somente leitura."""
    raise NotImplementedError('Adicione seu SQL de INSERT em tools/mysql/analysis.py:save_ai_analysis')
