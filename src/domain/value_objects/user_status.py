"""Value object for user status."""

from enum import Enum


class UserStatus(Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
    DELETED = "deleted"
    
    def is_active(self) -> bool:
        """Check if user status is active."""
        return self == UserStatus.ACTIVE
    
    def can_authenticate(self) -> bool:
        """Check if user can authenticate."""
        return self in [UserStatus.ACTIVE, UserStatus.PENDING_VERIFICATION]
