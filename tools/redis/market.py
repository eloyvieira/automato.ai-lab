import json
from database.redis_client import get_redis

async def get_current_btc_regime() -> dict:
    raw = await get_redis().get('market:btc:regime')
    if raw is None: return {'found': False, 'value': None}
    try: value = json.loads(raw)
    except json.JSONDecodeError: value = raw
    return {'found': True, 'value': value}

async def get_current_symbol_regime(symbol: str) -> dict:
    raw = await get_redis().get(f'market:{symbol.lower()}:regime')
    if raw is None: return {'found': False, 'value': None}
    try: value = json.loads(raw)
    except json.JSONDecodeError: value = raw
    return {'found': True, 'value': value}
