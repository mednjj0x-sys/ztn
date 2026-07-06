"""Repository interface for User entity following Clean Architecture."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User, UserTrustLevel


class UserRepository(ABC):
    """Abstract repository for User persistence operations."""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user entity."""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find a user by ID."""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        pass
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        role: Optional[str] = None,
    ) -> list[User]:
        """Find all users with optional filters."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user by ID."""
        pass
    
    @abstractmethod
    async def update_trust_level(self, user_id: UUID, trust_level: UserTrustLevel) -> User:
        """Update a user's trust level."""
        pass
    
    @abstractmethod
    async def count_total(self) -> int:
        """Count total number of users."""
        pass
