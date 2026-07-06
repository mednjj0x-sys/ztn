"""Data Transfer Objects for authentication operations."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class AuthenticationResultDTO:
    """DTO for authentication result."""
    success: bool
    user_id: Optional[UUID]
    access_token: Optional[str]
    refresh_token: Optional[str]
    requires_mfa: bool
    error: Optional[str]


@dataclass
class MFADTO:
    """DTO for MFA operations."""
    secret: str
    qr_code_url: str
    backup_codes: list[str]


@dataclass
class MFAVerificationDTO:
    """DTO for MFA verification result."""
    success: bool
    user_id: Optional[UUID]
    access_token: Optional[str]
    refresh_token: Optional[str]
    error: Optional[str]
