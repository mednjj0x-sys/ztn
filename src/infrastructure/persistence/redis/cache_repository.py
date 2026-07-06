"""Redis cache repository implementation."""

import json
from typing import Optional, Any

import redis.asyncio as redis


class RedisCacheRepository:
    """Redis repository for caching operations."""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        value = await self.redis.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.decode("utf-8")
    
    async def set(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None,
    ) -> bool:
        """Set a value in cache."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        else:
            value = str(value)
        
        return await self.redis.set(key, value, ex=expire_seconds)
    
    async def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        return await self.redis.delete(key) > 0
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        return await self.redis.exists(key) > 0
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key."""
        return await self.redis.expire(key, seconds)
    
    async def get_many(self, keys: list[str]) -> dict[str, Any]:
        """Get multiple values from cache."""
        values = await self.redis.mget(keys)
        result = {}
        for key, value in zip(keys, values):
            if value is not None:
                try:
                    result[key] = json.loads(value)
                except json.JSONDecodeError:
                    result[key] = value.decode("utf-8")
        return result
    
    async def set_many(
        self,
        mapping: dict[str, Any],
        expire_seconds: Optional[int] = None,
    ) -> bool:
        """Set multiple values in cache."""
        pipe = self.redis.pipeline()
        for key, value in mapping.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            else:
                value = str(value)
            pipe.set(key, value, ex=expire_seconds)
        results = await pipe.execute()
        return all(results)
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching a pattern."""
        keys = []
        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            return await self.redis.delete(*keys)
        return 0
