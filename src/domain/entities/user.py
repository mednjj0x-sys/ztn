"""Domain entity representing a user in the Zero Trust system."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from src.domain.value_objects.user_status import UserStatus
from src.domain.value_objects.user_role import UserRole


class UserTrustLevel(Enum):
    """Trust levels for Zero Trust authentication."""
    UNVERIFIED = "unverified"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class User:
    """User domain entity following Clean Architecture principles."""
    
    id: UUID
    email: str
    username: str
    full_name: str
    status: UserStatus
    role: UserRole
    trust_level: UserTrustLevel
    mfa_enabled: bool
    last_login: Optional[datetime]
    failed_login_attempts: int
    account_locked: bool
    lock_until: Optional[datetime]
    password_changed_at: datetime
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(
        cls,
        email: str,
        username: str,
        full_name: str,
        role: UserRole = UserRole.USER,
    ) -> "User":
        """Create a new user with default values."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            email=email.lower(),
            username=username.lower(),
            full_name=full_name,
            status=UserStatus.ACTIVE,
            role=role,
            trust_level=UserTrustLevel.UNVERIFIED,
            mfa_enabled=False,
            last_login=None,
            failed_login_attempts=0,
            account_locked=False,
            lock_until=None,
            password_changed_at=now,
            created_at=now,
            updated_at=now,
        )
    
    def record_failed_login(self) -> None:
        """Record a failed login attempt."""
        self.failed_login_attempts += 1
        self.updated_at = datetime.utcnow()
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.lock_account()
    
    def record_successful_login(self) -> None:
        """Record a successful login attempt."""
        self.failed_login_attempts = 0
        self.last_login = datetime.utcnow()
        self.account_locked = False
        self.lock_until = None
        self.updated_at = datetime.utcnow()
    
    def lock_account(self, lock_minutes: int = 30) -> None:
        """Lock the user account."""
        from datetime import timedelta
        self.account_locked = True
        self.lock_until = datetime.utcnow() + timedelta(minutes=lock_minutes)
        self.updated_at = datetime.utcnow()
    
    def is_account_locked(self) -> bool:
        """Check if the account is currently locked."""
        if not self.account_locked:
            return False
        if self.lock_until and datetime.utcnow() > self.lock_until:
            self.account_locked = False
            self.lock_until = None
            self.updated_at = datetime.utcnow()
            return False
        return True
    
    def can_access_resource(self, required_trust_level: UserTrustLevel) -> bool:
        """Check if user has sufficient trust level for resource access."""
        trust_hierarchy = {
            UserTrustLevel.UNVERIFIED: 0,
            UserTrustLevel.LOW: 1,
            UserTrustLevel.MEDIUM: 2,
            UserTrustLevel.HIGH: 3,
            UserTrustLevel.CRITICAL: 4,
        }
        return trust_hierarchy[self.trust_level] >= trust_hierarchy[required_trust_level]
