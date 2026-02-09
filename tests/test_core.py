import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from src.core.graph_client import GraphClient
from src.core.exceptions import GraphAPIException
import httpx

class TestGraphClient:
    @pytest.mark.asyncio
    async def test_get_success(self):
        token = "test_token"
        client = GraphClient(token)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_response.headers = {"Content-Type": "application/json"}
        # raise_for_status is not async
        mock_response.raise_for_status = Mock()
        
        # Mock client instance
        mock_client_instance = MagicMock()
        # Ensure __aenter__ returns self
        mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client_instance.__aexit__ = AsyncMock(return_value=None)
        
        # request method must be awaitable
        mock_client_instance.request = AsyncMock(return_value=mock_response)
        
        # Mock AsyncClient constructor
        with patch("httpx.AsyncClient", return_value=mock_client_instance):
            result = await client.get("/endpoint")
            assert result == {"key": "value"}
            mock_client_instance.request.assert_called()

    @pytest.mark.asyncio
    async def test_get_failure(self):
        token = "test_token"
        client = GraphClient(token)
        
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Error", request=Mock(), response=mock_response)
        
        mock_client_instance = MagicMock()
        mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client_instance.__aexit__ = AsyncMock(return_value=None)
        mock_client_instance.request = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient", return_value=mock_client_instance):
            with pytest.raises(GraphAPIException):
                await client.get("/endpoint")

    @pytest.mark.asyncio
    async def test_post_success(self):
        token = "test_token"
        client = GraphClient(token)
        
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "123"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.raise_for_status = Mock()
        
        mock_client_instance = MagicMock()
        mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client_instance.__aexit__ = AsyncMock(return_value=None)
        mock_client_instance.request = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient", return_value=mock_client_instance):
            result = await client.post("/endpoint", data={"data": "test"})
            assert result == {"id": "123"}
            mock_client_instance.request.assert_called()
