"""Domain service for authorization operations."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.access_request import AccessRequest, ResourceType
from src.domain.entities.user import User
from src.domain.entities.device import Device


class AuthorizationService(ABC):
    """Domain service for authorization logic."""
    
    @abstractmethod
    async def evaluate_access_request(
        self,
        user: User,
        device: Device,
        resource_type: ResourceType,
        resource_id: str,
        action: str,
        context: dict,
    ) -> tuple[bool, str]:
        """
        Evaluate an access request.
        Returns (is_allowed, reason) tuple.
        """
        pass
    
    @abstractmethod
    async def check_permission(
        self,
        user_id: UUID,
        permission: str,
        resource_id: Optional[str] = None,
    ) -> bool:
        """Check if a user has a specific permission."""
        pass
    
    @abstractmethod
    async def grant_permission(
        self,
        user_id: UUID,
        permission: str,
        resource_id: Optional[str] = None,
    ) -> bool:
        """Grant a permission to a user."""
        pass
    
    @abstractmethod
    async def revoke_permission(
        self,
        user_id: UUID,
        permission: str,
        resource_id: Optional[str] = None,
    ) -> bool:
        """Revoke a permission from a user."""
        pass
