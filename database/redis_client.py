import redis.asyncio as redis
from core.config import get_settings

_client = None

def get_redis():
    global _client
    if _client is None:
        _client = redis.from_url(get_settings().redis_url, decode_responses=True)
    return _client
