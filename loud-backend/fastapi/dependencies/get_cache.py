from typing import Optional
import redis
from core.config import settings
from cache.redis_cache import RedisCache
from cache.base import Cache

_redis_client: Optional[redis.Redis] = None
_cache_instance: Optional[Cache] = None

def get_redis_client() -> redis.Redis:
    """Obtiene el cliente Redis (singleton)"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2
        )
    return _redis_client

def get_cache() -> Cache:
    """Dependencia de FastAPI para la caché"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache(get_redis_client(), default_ttl=settings.CACHE_TTL)
    return _cache_instance