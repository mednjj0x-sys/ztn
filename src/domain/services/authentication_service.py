"""Domain service for authentication operations."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.entities.device import Device


class AuthenticationService(ABC):
    """Domain service for authentication logic."""
    
    @abstractmethod
    async def authenticate_user(
        self,
        email: str,
        password: str,
        device_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> tuple[Optional[User], Optional[str]]:
        """
        Authenticate a user with credentials.
        Returns (user, error_message) tuple.
        """
        pass
    
    @abstractmethod
    async def verify_mfa(self, user_id: UUID, code: str) -> bool:
        """Verify MFA code for a user."""
        pass
    
    @abstractmethod
    async def generate_mfa_secret(self, user_id: UUID) -> str:
        """Generate MFA secret for a user."""
        pass
    
    @abstractmethod
    async def evaluate_device_trust(self, device: Device) -> int:
        """Evaluate device trust score (0-100)."""
        pass
    
    @abstractmethod
    async def evaluate_user_risk(self, user: User) -> int:
        """Evaluate user risk score (0-100)."""
        pass
