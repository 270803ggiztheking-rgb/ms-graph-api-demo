import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.api.deps import get_access_token, get_auth_service

@pytest.fixture
def mock_auth_service():
    mock = MagicMock()
    mock.get_auth_url.return_value = "http://mock-auth-url"
    mock.acquire_token_by_code.return_value = {"access_token": "mock_token"}
    return mock

@pytest.fixture
def client(mock_auth_service):
    print("DEBUG: Setting up client fixture and overrides")
    # Override dependency to skip auth or mock it
    app.dependency_overrides[get_access_token] = lambda: "mock_token"
    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
    print(f"DEBUG: Overrides set: {app.dependency_overrides}")
    
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
    print("DEBUG: Overrides cleared")
