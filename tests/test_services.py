import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.core.exceptions import AuthException

class TestAuthService:
    @patch("src.services.auth_service.msal.ConfidentialClientApplication")
    def test_get_auth_url(self, mock_msal_app):
        mock_instance = mock_msal_app.return_value
        mock_instance.get_authorization_request_url.return_value = "http://login.microsoft.com/auth"
        
        service = AuthService()
        url = service.get_auth_url("test_state")
        
        assert url == "http://login.microsoft.com/auth"
        mock_instance.get_authorization_request_url.assert_called_once()

    @patch("src.services.auth_service.msal.ConfidentialClientApplication")
    def test_acquire_token_success(self, mock_msal_app):
        mock_instance = mock_msal_app.return_value
        mock_instance.acquire_token_by_authorization_code.return_value = {"access_token": "token"}
        
        service = AuthService()
        result = service.acquire_token_by_code("code")
        
        assert result["access_token"] == "token"

    @patch("src.services.auth_service.msal.ConfidentialClientApplication")
    def test_acquire_token_failure(self, mock_msal_app):
        mock_instance = mock_msal_app.return_value
        mock_instance.acquire_token_by_authorization_code.return_value = {"error": "invalid_grant", "error_description": "Bad code"}
        
        service = AuthService()
        with pytest.raises(AuthException) as excinfo:
            service.acquire_token_by_code("bad_code")
        
        assert "Authentication failed" in str(excinfo.value)

class TestUserService:
    @pytest.mark.asyncio
    async def test_get_me(self):
        # Use AsyncMock for the client
        mock_client = Mock()
        mock_client.get = AsyncMock(return_value={"displayName": "Test User", "id": "123", "mail": "test@example.com"})
        
        service = UserService(mock_client)
        result = await service.get_me()
        
        assert result.displayName == "Test User"
        mock_client.get.assert_called_with("/me")
