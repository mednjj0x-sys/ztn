"""Repository interface for Device entity following Clean Architecture."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.device import Device, DeviceStatus, DeviceType


class DeviceRepository(ABC):
    """Abstract repository for Device persistence operations."""
    
    @abstractmethod
    async def save(self, device: Device) -> Device:
        """Save a device entity."""
        pass
    
    @abstractmethod
    async def find_by_id(self, device_id: UUID) -> Optional[Device]:
        """Find a device by ID."""
        pass
    
    @abstractmethod
    async def find_by_device_id(self, device_id: str) -> Optional[Device]:
        """Find a device by hardware identifier."""
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> list[Device]:
        """Find all devices for a user."""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[DeviceStatus] = None,
        device_type: Optional[DeviceType] = None,
    ) -> list[Device]:
        """Find all devices with optional filters."""
        pass
    
    @abstractmethod
    async def delete(self, device_id: UUID) -> bool:
        """Delete a device by ID."""
        pass
    
    @abstractmethod
    async def update_compliance_score(self, device_id: UUID, score: int) -> Device:
        """Update a device's compliance score."""
        pass
    
    @abstractmethod
    async def find_compromised_devices(self) -> list[Device]:
        """Find all compromised devices."""
        pass
