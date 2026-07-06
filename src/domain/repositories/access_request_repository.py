"""Repository interface for AccessRequest entity following Clean Architecture."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.access_request import AccessRequest, AccessDecision, ResourceType


class AccessRequestRepository(ABC):
    """Abstract repository for AccessRequest persistence operations."""
    
    @abstractmethod
    async def save(self, request: AccessRequest) -> AccessRequest:
        """Save an access request entity."""
        pass
    
    @abstractmethod
    async def find_by_id(self, request_id: UUID) -> Optional[AccessRequest]:
        """Find an access request by ID."""
        pass
    
    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AccessRequest]:
        """Find all access requests for a user."""
        pass
    
    @abstractmethod
    async def find_by_device_id(
        self,
        device_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AccessRequest]:
        """Find all access requests for a device."""
        pass
    
    @abstractmethod
    async def find_active_requests(
        self,
        user_id: Optional[UUID] = None,
        resource_type: Optional[ResourceType] = None,
    ) -> list[AccessRequest]:
        """Find all currently valid access requests."""
        pass
    
    @abstractmethod
    async def find_expired_requests(self) -> list[AccessRequest]:
        """Find all expired access requests."""
        pass
    
    @abstractmethod
    async def update_decision(
        self,
        request_id: UUID,
        decision: AccessDecision,
        reason: str,
    ) -> AccessRequest:
        """Update the decision for an access request."""
        pass
    
    @abstractmethod
    async def revoke_expired_requests(self) -> int:
        """Revoke all expired access requests and return count."""
        pass
