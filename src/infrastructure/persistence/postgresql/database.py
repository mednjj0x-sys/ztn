"""Database connection and session management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from apps.config.settings import settings


class Database:
    """Database connection manager."""
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
    
    def connect(self, database_url: str = None) -> None:
        """Create database engine and session maker."""
        url = database_url or settings.database_url
        self.engine = create_async_engine(
            url,
            echo=settings.debug,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_pre_ping=True,
        )
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def disconnect(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database instance
database = Database()
