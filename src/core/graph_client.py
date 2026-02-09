import httpx
from typing import Any, Dict, Optional
from src.core.config import settings
from src.core.exceptions import GraphAPIException
from loguru import logger


class GraphClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = settings.GRAPH_API_ENDPOINT
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def request(
            self,
            method: str,
            endpoint: str,
            headers: Optional[Dict] = None,
            **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        req_headers = self.headers.copy()
        if headers:
            req_headers.update(headers)

        logger.debug(f"Graph API Request: {method} {url}")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method, url=url, headers=req_headers, **kwargs
                )
                response.raise_for_status()

                if response.status_code == 204:
                    return None

                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return response.json()
                return response.content

            except httpx.HTTPStatusError as e:
                logger.error(f"Graph API Error: {e.response.text}")
                try:
                    details = e.response.json()
                except Exception:
                    details = {"raw": e.response.text}
                raise GraphAPIException(
                    status_code=e.response.status_code,
                    message=f"Graph API request failed: {e}",
                    details=details,
                )
            except httpx.RequestError as e:
                logger.error(f"Network Error: {e}")
                raise GraphAPIException(
                    status_code=500, message=f"Network error: {e}")

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        return await self.request("POST", endpoint, json=data)

    async def put(self, endpoint: str, data: Any = None,
                  content_type: str = "application/json") -> Any:
        headers = {"Content-Type": content_type}
        if isinstance(data, (dict, list)):
            return await self.request("PUT", endpoint, headers=headers, json=data)
        else:
            return await self.request("PUT", endpoint, headers=headers, content=data)

    async def delete(self, endpoint: str) -> Any:
        return await self.request("DELETE", endpoint)
