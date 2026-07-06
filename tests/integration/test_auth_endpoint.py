"""Integration tests for authentication endpoints."""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.integration
class TestAuthEndpoints:
    """Tests for authentication API endpoints."""
    
    async def test_login_success(self, async_client: AsyncClient):
        """Test successful login."""
        # Mock the authentication service
        with patch("apps.api.api.v1.endpoints.auth.authenticate_user_use_case") as mock:
            from src.application.dto.auth_dto import AuthenticationResultDTO
            from uuid import uuid4
            
            mock.return_value = AsyncMock()
            mock.return_value.execute = AsyncMock(return_value=AuthenticationResultDTO(
                success=True,
                user_id=uuid4(),
                access_token="test_token",
                refresh_token="test_refresh",
                requires_mfa=False,
                error=None,
            ))
            
            response = await async_client.post(
                "/api/v1/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "testpassword",
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "access_token" in data
    
    async def test_login_invalid_credentials(self, async_client: AsyncClient):
        """Test login with invalid credentials."""
        with patch("apps.api.api.v1.endpoints.auth.authenticate_user_use_case") as mock:
            from src.application.dto.auth_dto import AuthenticationResultDTO
            
            mock.return_value = AsyncMock()
            mock.return_value.execute = AsyncMock(return_value=AuthenticationResultDTO(
                success=False,
                user_id=None,
                access_token=None,
                refresh_token=None,
                requires_mfa=False,
                error="Invalid credentials",
            ))
            
            response = await async_client.post(
                "/api/v1/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "wrongpassword",
                }
            )
            
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
