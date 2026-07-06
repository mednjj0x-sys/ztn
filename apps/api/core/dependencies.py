"""FastAPI dependencies for dependency injection."""

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from apps.config.settings import settings
from apps.core.logging_config import get_logger
from src.infrastructure.persistence.postgresql.database import database
from src.infrastructure.persistence.redis.redis_client import redis_client
from src.infrastructure.persistence.redis.cache_repository import RedisCacheRepository

logger = get_logger(__name__)
security = HTTPBearer()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with database.get_session() as session:
        yield session


async def get_redis_cache() -> RedisCacheRepository:
    """Get Redis cache repository dependency."""
    redis = redis_client.get_client()
    return RedisCacheRepository(redis)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify JWT token and return user info."""
    token = credentials.credentials
    
    # In production, implement proper JWT verification
    # For now, this is a placeholder
    logger.info("Token verification", token=token[:10] + "...")
    
    # Placeholder: return mock user info
    return {
        "user_id": "mock-user-id",
        "email": "user@example.com",
        "role": "user",
    }


async def require_admin(
    user_info: dict = Depends(verify_token),
) -> dict:
    """Require admin role dependency."""
    if user_info.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user_info
