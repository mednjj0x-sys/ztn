"""Domain entity representing a device in the Zero Trust system."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class DeviceType(Enum):
    """Types of devices in the system."""
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    MOBILE = "mobile"
    TABLET = "tablet"
    SERVER = "server"
    IOT = "iot"


class DeviceStatus(Enum):
    """Device status in the Zero Trust system."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPROMISED = "compromised"
    QUARANTINED = "quarantined"
    DECOMMISSIONED = "decommissioned"


class DeviceTrustScore(Enum):
    """Trust scores for devices."""
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    TRUSTED = 4


@dataclass
class Device:
    """Device domain entity following Clean Architecture principles."""
    
    id: UUID
    user_id: UUID
    device_name: str
    device_type: DeviceType
    device_id: str  # Hardware identifier
    os_type: str
    os_version: str
    status: DeviceStatus
    trust_score: DeviceTrustScore
    last_seen: Optional[datetime]
    last_authenticated: Optional[datetime]
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_managed: bool
    compliance_score: int  # 0-100
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(
        cls,
        user_id: UUID,
        device_name: str,
        device_type: DeviceType,
        device_id: str,
        os_type: str,
        os_version: str,
    ) -> "Device":
        """Create a new device with default values."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            user_id=user_id,
            device_name=device_name,
            device_type=device_type,
            device_id=device_id,
            os_type=os_type,
            os_version=os_version,
            status=DeviceStatus.ACTIVE,
            trust_score=DeviceTrustScore.UNKNOWN,
            last_seen=now,
            last_authenticated=None,
            ip_address=None,
            user_agent=None,
            is_managed=False,
            compliance_score=0,
            created_at=now,
            updated_at=now,
        )
    
    def update_last_seen(self, ip_address: str, user_agent: str) -> None:
        """Update the last seen information."""
        self.last_seen = datetime.utcnow()
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.updated_at = datetime.utcnow()
    
    def record_authentication(self) -> None:
        """Record successful authentication."""
        self.last_authenticated = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def quarantine(self) -> None:
        """Quarantine the device."""
        self.status = DeviceStatus.QUARANTINED
        self.trust_score = DeviceTrustScore.LOW
        self.updated_at = datetime.utcnow()
    
    def mark_compromised(self) -> None:
        """Mark the device as compromised."""
        self.status = DeviceStatus.COMPROMISED
        self.trust_score = DeviceTrustScore.LOW
        self.updated_at = datetime.utcnow()
    
    def is_trusted(self) -> bool:
        """Check if the device is trusted."""
        return (
            self.status == DeviceStatus.ACTIVE
            and self.trust_score in [DeviceTrustScore.HIGH, DeviceTrustScore.TRUSTED]
            and self.compliance_score >= 80
        )
    
    def is_compliant(self) -> bool:
        """Check if the device meets compliance requirements."""
        return self.compliance_score >= 70
