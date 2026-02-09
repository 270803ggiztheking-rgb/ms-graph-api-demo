import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.api.deps import get_access_token

@pytest.fixture
def client():
    # Override dependency to skip auth or mock it
    app.dependency_overrides[get_access_token] = lambda: "mock_token"
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
