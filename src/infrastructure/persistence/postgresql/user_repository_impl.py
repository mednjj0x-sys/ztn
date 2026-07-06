"""PostgreSQL implementation of UserRepository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User, UserTrustLevel
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.persistence.postgresql.models.user_model import UserModel


class PostgreSQLUserRepository(UserRepository):
    """PostgreSQL implementation of UserRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, user: User) -> User:
        """Save a user entity."""
        user_model = await self._to_model(user)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return await self._to_entity(user_model)
    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find a user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return await self._to_entity(user_model) if user_model else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email.lower())
        )
        user_model = result.scalar_one_or_none()
        return await self._to_entity(user_model) if user_model else None
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username.lower())
        )
        user_model = result.scalar_one_or_none()
        return await self._to_entity(user_model) if user_model else None
    
    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        role: Optional[str] = None,
    ) -> list[User]:
        """Find all users with optional filters."""
        query = select(UserModel)
        
        if status:
            query = query.where(UserModel.status == status)
        if role:
            query = query.where(UserModel.role == role)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        user_models = result.scalars().all()
        
        users = []
        for model in user_models:
            user = await self._to_entity(model)
            if user:
                users.append(user)
        return users
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        
        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()
            return True
        return False
    
    async def update_trust_level(self, user_id: UUID, trust_level: UserTrustLevel) -> User:
        """Update a user's trust level."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        
        if user_model:
            user_model.trust_level = trust_level.value
            await self.session.commit()
            await self.session.refresh(user_model)
            return await self._to_entity(user_model)
        
        raise ValueError(f"User with id {user_id} not found")
    
    async def count_total(self) -> int:
        """Count total number of users."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count()).select_from(UserModel)
        )
        return result.scalar()
    
    async def _to_model(self, user: User) -> UserModel:
        """Convert User entity to UserModel."""
        return UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            status=user.status.value,
            role=user.role.value,
            trust_level=user.trust_level.value,
            mfa_enabled=user.mfa_enabled,
            last_login=user.last_login,
            failed_login_attempts=user.failed_login_attempts,
            account_locked=user.account_locked,
            lock_until=user.lock_until,
            password_changed_at=user.password_changed_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    
    async def _to_entity(self, model: UserModel) -> Optional[User]:
        """Convert UserModel to User entity."""
        from src.domain.value_objects.user_status import UserStatus
        from src.domain.value_objects.user_role import UserRole
        
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            status=UserStatus(model.status),
            role=UserRole(model.role),
            trust_level=UserTrustLevel(model.trust_level),
            mfa_enabled=model.mfa_enabled,
            last_login=model.last_login,
            failed_login_attempts=model.failed_login_attempts,
            account_locked=model.account_locked,
            lock_until=model.lock_until,
            password_changed_at=model.password_changed_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
