"""Use case for requesting resource access."""

from uuid import UUID

from src.application.dto.access_dto import AccessRequestDTO
from src.domain.entities.access_request import AccessRequest, ResourceType
from src.domain.entities.device import Device
from src.domain.entities.user import User
from src.domain.repositories.access_request_repository import AccessRequestRepository
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.authorization_service import AuthorizationService


class RequestAccessUseCase:
    """Use case for requesting access to a resource."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        device_repository: DeviceRepository,
        access_request_repository: AccessRequestRepository,
        authorization_service: AuthorizationService,
    ):
        self.user_repository = user_repository
        self.device_repository = device_repository
        self.access_request_repository = access_request_repository
        self.authorization_service = authorization_service
    
    async def execute(
        self,
        user_id: UUID,
        device_id: UUID,
        resource_type: ResourceType,
        resource_id: str,
        action: str,
        metadata: dict,
        context: dict,
    ) -> AccessRequestDTO:
        """Execute the access request use case."""
        # Fetch user and device
        user = await self.user_repository.find_by_id(user_id)
        device = await self.device_repository.find_by_id(device_id)
        
        if not user:
            raise ValueError("User not found")
        if not device:
            raise ValueError("Device not found")
        
        # Evaluate access request
        is_allowed, reason = await self.authorization_service.evaluate_access_request(
            user=user,
            device=device,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            context=context,
        )
        
        # Create access request
        access_request = AccessRequest.create(
            user_id=user_id,
            device_id=device_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            metadata=metadata,
            context=context,
        )
        
        # Set decision based on evaluation
        if is_allowed:
            access_request.approve(reason=reason, ttl_seconds=3600)  # 1 hour TTL
        else:
            access_request.deny(reason=reason)
        
        # Save the request
        saved_request = await self.access_request_repository.save(access_request)
        
        return AccessRequestDTO(
            id=saved_request.id,
            user_id=saved_request.user_id,
            device_id=saved_request.device_id,
            resource_type=saved_request.resource_type.value,
            resource_id=saved_request.resource_id,
            action=saved_request.action,
            decision=saved_request.decision.value,
            decision_reason=saved_request.decision_reason,
            requested_at=saved_request.requested_at,
            decided_at=saved_request.decided_at,
            expires_at=saved_request.expires_at,
        )
