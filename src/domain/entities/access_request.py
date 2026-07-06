"""Domain entity representing an access request in the Zero Trust system."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class AccessDecision(Enum):
    """Access decision outcomes."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    REVOKED = "revoked"


class ResourceType(Enum):
    """Types of resources that can be accessed."""
    API_ENDPOINT = "api_endpoint"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    NETWORK = "network"
    SERVICE = "service"


@dataclass
class AccessRequest:
    """Access request domain entity following Clean Architecture principles."""
    
    id: UUID
    user_id: UUID
    device_id: UUID
    resource_type: ResourceType
    resource_id: str
    action: str  # e.g., "read", "write", "execute"
    decision: AccessDecision
    decision_reason: Optional[str]
    requested_at: datetime
    decided_at: Optional[datetime]
    expires_at: Optional[datetime]
    metadata: dict
    context: dict
    
    @classmethod
    def create(
        cls,
        user_id: UUID,
        device_id: UUID,
        resource_type: ResourceType,
        resource_id: str,
        action: str,
        metadata: Optional[dict] = None,
        context: Optional[dict] = None,
    ) -> "AccessRequest":
        """Create a new access request."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            user_id=user_id,
            device_id=device_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            decision=AccessDecision.PENDING,
            decision_reason=None,
            requested_at=now,
            decided_at=None,
            expires_at=None,
            metadata=metadata or {},
            context=context or {},
        )
    
    def approve(self, reason: str, ttl_seconds: Optional[int] = None) -> None:
        """Approve the access request."""
        self.decision = AccessDecision.APPROVED
        self.decision_reason = reason
        self.decided_at = datetime.utcnow()
        if ttl_seconds:
            from datetime import timedelta
            self.expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
    
    def deny(self, reason: str) -> None:
        """Deny the access request."""
        self.decision = AccessDecision.DENIED
        self.decision_reason = reason
        self.decided_at = datetime.utcnow()
    
    def revoke(self, reason: str) -> None:
        """Revoke previously approved access."""
        self.decision = AccessDecision.REVOKED
        self.decision_reason = reason
        self.decided_at = datetime.utcnow()
    
    def is_valid(self) -> bool:
        """Check if the access request is still valid."""
        if self.decision != AccessDecision.APPROVED:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def has_expired(self) -> bool:
        """Check if the access has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
