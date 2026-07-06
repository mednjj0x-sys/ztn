"""Unit tests for Device entity."""

import pytest
from uuid import uuid4

from src.domain.entities.device import Device, DeviceStatus, DeviceTrustScore, DeviceType


class TestDevice:
    """Tests for Device entity."""
    
    def test_create_device(self):
        """Test device creation with default values."""
        user_id = uuid4()
        device = Device.create(
            user_id=user_id,
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        assert device.user_id == user_id
        assert device.device_name == "Test Device"
        assert device.device_type == DeviceType.LAPTOP
        assert device.device_id == "device-123"
        assert device.status == DeviceStatus.ACTIVE
        assert device.trust_score == DeviceTrustScore.UNKNOWN
        assert device.compliance_score == 0
        assert device.is_managed is False
    
    def test_update_last_seen(self):
        """Test updating last seen information."""
        device = Device.create(
            user_id=uuid4(),
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        device.update_last_seen("192.168.1.1", "Mozilla/5.0")
        
        assert device.ip_address == "192.168.1.1"
        assert device.user_agent == "Mozilla/5.0"
        assert device.last_seen is not None
    
    def test_quarantine_device(self):
        """Test quarantining a device."""
        device = Device.create(
            user_id=uuid4(),
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        device.quarantine()
        
        assert device.status == DeviceStatus.QUARANTINED
        assert device.trust_score == DeviceTrustScore.LOW
    
    def test_mark_compromised(self):
        """Test marking device as compromised."""
        device = Device.create(
            user_id=uuid4(),
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        device.mark_compromised()
        
        assert device.status == DeviceStatus.COMPROMISED
        assert device.trust_score == DeviceTrustScore.LOW
    
    def test_is_trusted(self):
        """Test checking if device is trusted."""
        device = Device.create(
            user_id=uuid4(),
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        assert device.is_trusted() is False
        
        device.trust_score = DeviceTrustScore.HIGH
        device.compliance_score = 85
        assert device.is_trusted() is True
        
        device.compliance_score = 75
        assert device.is_trusted() is False
    
    def test_is_compliant(self):
        """Test checking if device is compliant."""
        device = Device.create(
            user_id=uuid4(),
            device_name="Test Device",
            device_type=DeviceType.LAPTOP,
            device_id="device-123",
            os_type="Windows",
            os_version="11",
        )
        
        assert device.is_compliant() is False
        
        device.compliance_score = 70
        assert device.is_compliant() is True
        
        device.compliance_score = 69
        assert device.is_compliant() is False
