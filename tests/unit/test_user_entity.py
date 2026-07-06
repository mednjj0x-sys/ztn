"""Unit tests for User entity."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.entities.user import User, UserTrustLevel
from src.domain.value_objects.user_status import UserStatus
from src.domain.value_objects.user_role import UserRole


class TestUser:
    """Tests for User entity."""
    
    def test_create_user(self):
        """Test user creation with default values."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"
        assert user.status == UserStatus.ACTIVE
        assert user.role == UserRole.USER
        assert user.trust_level == UserTrustLevel.UNVERIFIED
        assert user.mfa_enabled is False
        assert user.failed_login_attempts == 0
        assert user.account_locked is False
    
    def test_record_failed_login(self):
        """Test recording failed login attempts."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        
        user.record_failed_login()
        assert user.failed_login_attempts == 1
        
        user.record_failed_login()
        assert user.failed_login_attempts == 2
    
    def test_account_lock_after_max_attempts(self):
        """Test account locks after max failed attempts."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        
        # Record 5 failed attempts
        for _ in range(5):
            user.record_failed_login()
        
        assert user.account_locked is True
        assert user.lock_until is not None
    
    def test_record_successful_login(self):
        """Test recording successful login."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        user.failed_login_attempts = 3
        user.account_locked = True
        
        user.record_successful_login()
        
        assert user.failed_login_attempts == 0
        assert user.account_locked is False
        assert user.last_login is not None
    
    def test_is_account_locked(self):
        """Test checking if account is locked."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        
        assert user.is_account_locked() is False
        
        user.lock_account()
        assert user.is_account_locked() is True
    
    def test_account_unlock_after_timeout(self):
        """Test account unlocks after timeout."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        
        user.lock_account(lock_minutes=1)
        assert user.is_account_locked() is True
        
        # Simulate time passing
        user.lock_until = datetime.utcnow() - timedelta(minutes=2)
        assert user.is_account_locked() is False
    
    def test_can_access_resource(self):
        """Test resource access based on trust level."""
        user = User.create(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
        )
        user.trust_level = UserTrustLevel.HIGH
        
        assert user.can_access_resource(UserTrustLevel.MEDIUM) is True
        assert user.can_access_resource(UserTrustLevel.HIGH) is True
        assert user.can_access_resource(UserTrustLevel.CRITICAL) is False
