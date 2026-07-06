"""Data Transfer Objects for user operations."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserDTO:
    """DTO for user data."""
    id: UUID
    email: str
    username: str
    full_name: str
    status: str
    role: str
    trust_level: str
    mfa_enabled: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateUserDTO:
    """DTO for creating a user."""
    email: str
    username: str
    full_name: str
    password: str
    role: Optional[str] = "user"


@dataclass
class UpdateUserDTO:
    """DTO for updating a user."""
    full_name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    trust_level: Optional[str] = None


@dataclass
class ChangePasswordDTO:
    """DTO for changing password."""
    current_password: str
    new_password: str
