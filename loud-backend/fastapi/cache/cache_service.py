import json
from typing import Optional, Any
import redis
from core.config import settings

class CacheService:
    
    def __init__(self):
        self.redis = None
        self.enabled = False
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            self.redis.ping()
            self.enabled = True
            print("Redis connected - caching enabled")
        except Exception as e:
            print(f"Redis not available: {e} - running without cache (graceful degradation)")
            self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        if not self.enabled or not self.redis:
            return None
        try:
            data = self.redis.get(key)
            return json.loads(data) if data else None  # type: ignore
        except:
            return None
    
    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        if not self.enabled or not self.redis:
            return
        try:
            self.redis.setex(key, ttl, json.dumps(value))
        except:
            pass
    
    def delete(self, key: str) -> None:
        if not self.enabled or not self.redis:
            return
        try:
            self.redis.delete(key)
        except:
            pass

# Instancia global
cache = CacheService()