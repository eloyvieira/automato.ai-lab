from typing import Any

async def get_btc_regime_history(start_date: str, end_date: str | None = None, limit: int = 500) -> list[dict[str, Any]]:
    """Implemente a consulta de histórico do regime BTC aqui."""
    raise NotImplementedError('Adicione seu SQL em tools/mysql/regimes.py:get_btc_regime_history')

async def get_symbol_regime_history(symbol: str, start_date: str, end_date: str | None = None, limit: int = 500) -> list[dict[str, Any]]:
    """Implemente a consulta do regime da altcoin aqui."""
    raise NotImplementedError('Adicione seu SQL em tools/mysql/regimes.py:get_symbol_regime_history')
