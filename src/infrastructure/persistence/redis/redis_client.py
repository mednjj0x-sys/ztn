"""Redis client configuration and management."""

import redis.asyncio as redis

from apps.config.settings import settings


class RedisClient:
    """Redis client manager."""
    
    def __init__(self):
        self.client = None
    
    def connect(self, redis_url: str = None) -> None:
        """Create Redis client."""
        url = redis_url or settings.redis_url
        self.client = redis.from_url(
            url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=settings.redis_max_connections,
        )
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.client:
            await self.client.close()
    
    def get_client(self) -> redis.Redis:
        """Get the Redis client instance."""
        if not self.client:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self.client


# Global Redis client instance
redis_client = RedisClient()
