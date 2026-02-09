from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

# client fixture is used automatically from conftest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_redirect(client):
    # The dependency is overridden in conftest to return a mock that returns "http://mock-auth-url"
    response = client.get("/api/v1/login", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://mock-auth-url"

def test_auth_callback(client):
    response = client.get("/api/v1/callback?code=123&state=test", follow_redirects=False)
    assert response.status_code == 307
    assert "session_id" in response.cookies

from unittest.mock import patch, AsyncMock

# ... (imports)

def test_get_user_me(client):
    with patch("src.services.user_service.UserService.get_me", new_callable=AsyncMock) as mock_get_me:
        mock_get_me.return_value = {"displayName": "Test User", "mail": "test@example.com", "id": "123"}
        
        response = client.get("/api/v1/users/me")
        assert response.status_code == 200
        assert response.json()["displayName"] == "Test User"

def test_get_user_profile(client):
    with patch("src.services.user_service.UserService.get_me", new_callable=AsyncMock) as mock_get_me:
        mock_get_me.return_value = {"displayName": "Test User", "mail": "test@example.com", "id": "123"}
        
        response = client.get("/api/v1/users/me")
        assert response.status_code == 200
        assert response.json()["displayName"] == "Test User"
