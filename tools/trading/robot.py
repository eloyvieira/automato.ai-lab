from typing import Any

async def get_robot_status() -> dict[str, Any]:
    """Conecte aqui ao status/runtime do robô, via API, arquivo, Redis etc."""
    return {'status': 'not_configured'}

async def get_market_snapshot(symbol: str, timeframe: str = '15m') -> dict[str, Any]:
    """Conecte aqui aos indicadores atuais do seu robô/market data."""
    raise NotImplementedError('Implemente a fonte de market snapshot em tools/trading/robot.py')
