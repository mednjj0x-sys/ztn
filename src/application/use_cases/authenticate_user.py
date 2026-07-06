"""Use case for user authentication."""

from typing import Optional
from uuid import UUID

from src.application.dto.auth_dto import AuthenticationResultDTO
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.services.authentication_service import AuthenticationService


class AuthenticateUserUseCase:
    """Use case for authenticating a user."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        device_repository: DeviceRepository,
        authentication_service: AuthenticationService,
    ):
        self.user_repository = user_repository
        self.device_repository = device_repository
        self.authentication_service = authentication_service
    
    async def execute(
        self,
        email: str,
        password: str,
        device_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuthenticationResultDTO:
        """Execute the authentication use case."""
        # Authenticate user credentials
        user, error = await self.authentication_service.authenticate_user(
            email=email,
            password=password,
            device_id=device_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        if not user:
            return AuthenticationResultDTO(
                success=False,
                user_id=None,
                access_token=None,
                refresh_token=None,
                requires_mfa=False,
                error=error or "Authentication failed",
            )
        
        # Check if account is locked
        if user.is_account_locked():
            return AuthenticationResultDTO(
                success=False,
                user_id=user.id,
                access_token=None,
                refresh_token=None,
                requires_mfa=False,
                error="Account is temporarily locked",
            )
        
        # Update device information if provided
        if device_id:
            device = await self.device_repository.find_by_device_id(device_id)
            if device:
                device.update_last_seen(ip_address or "", user_agent or "")
                await self.device_repository.save(device)
        
        # Check MFA requirement
        if user.mfa_enabled:
            return AuthenticationResultDTO(
                success=False,
                user_id=user.id,
                access_token=None,
                refresh_token=None,
                requires_mfa=True,
                error=None,
            )
        
        # Record successful login
        user.record_successful_login()
        await self.user_repository.save(user)
        
        # Generate tokens (would be done by a token service in real implementation)
        # For now, return success
        return AuthenticationResultDTO(
            success=True,
            user_id=user.id,
            access_token="generated_access_token",  # Placeholder
            refresh_token="generated_refresh_token",  # Placeholder
            requires_mfa=False,
            error=None,
        )
