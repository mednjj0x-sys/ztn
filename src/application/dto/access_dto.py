"""Data Transfer Objects for access operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class AccessRequestDTO:
    """DTO for access request."""
    id: UUID
    user_id: UUID
    device_id: UUID
    resource_type: str
    resource_id: str
    action: str
    decision: str
    decision_reason: Optional[str]
    requested_at: datetime
    decided_at: Optional[datetime]
    expires_at: Optional[datetime]


@dataclass
class CreateAccessRequestDTO:
    """DTO for creating an access request."""
    user_id: UUID
    device_id: UUID
    resource_type: str
    resource_id: str
    action: str
    metadata: dict
    context: dict


@dataclass
class AccessDecisionDTO:
    """DTO for access decision."""
    request_id: UUID
    decision: str
    reason: str
    ttl_seconds: Optional[int] = None
