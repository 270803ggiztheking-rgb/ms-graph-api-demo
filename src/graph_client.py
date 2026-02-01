"""
Microsoft Graph API Demo - Graph Client
HTTP client for Microsoft Graph API requests
"""
import httpx
from typing import Optional
from src.config import get_settings


class GraphClient:
    """HTTP client for Microsoft Graph API."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.settings = get_settings()
        self.base_url = self.settings.graph_api_endpoint
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to Graph API."""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else {}
    
    # ═══════════════════════════════════════════════════════════
    # USER
    # ═══════════════════════════════════════════════════════════
    
    async def get_me(self) -> dict:
        """Get current user's profile."""
        return await self._request("GET", "/me")
    
    async def get_user_photo(self) -> bytes:
        """Get current user's profile photo."""
        url = f"{self.base_url}/me/photo/$value"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            return response.content if response.status_code == 200 else None
    
    # ═══════════════════════════════════════════════════════════
    # MAIL (OUTLOOK)
    # ═══════════════════════════════════════════════════════════
    
    async def get_emails(self, top: int = 10, folder: str = "inbox") -> dict:
        """Get emails from specified folder."""
        return await self._request(
            "GET",
            f"/me/mailFolders/{folder}/messages",
            params={"$top": top, "$orderby": "receivedDateTime desc"}
        )
    
    async def get_email(self, message_id: str) -> dict:
        """Get specific email by ID."""
        return await self._request("GET", f"/me/messages/{message_id}")
    
    async def send_email(
        self,
        to: list[str],
        subject: str,
        body: str,
        body_type: str = "HTML"
    ) -> dict:
        """Send an email."""
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": body_type,
                    "content": body
                },
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in to
                ]
            },
            "saveToSentItems": True
        }
        return await self._request("POST", "/me/sendMail", json=message)
    
    async def delete_email(self, message_id: str) -> None:
        """Delete an email."""
        await self._request("DELETE", f"/me/messages/{message_id}")
    
    # ═══════════════════════════════════════════════════════════
    # CALENDAR
    # ═══════════════════════════════════════════════════════════
    
    async def get_events(self, top: int = 10) -> dict:
        """Get calendar events."""
        return await self._request(
            "GET",
            "/me/events",
            params={"$top": top, "$orderby": "start/dateTime"}
        )
    
    async def create_event(
        self,
        subject: str,
        start: str,
        end: str,
        attendees: Optional[list[str]] = None,
        body: str = ""
    ) -> dict:
        """Create a calendar event."""
        event = {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body},
            "start": {"dateTime": start, "timeZone": "America/Mexico_City"},
            "end": {"dateTime": end, "timeZone": "America/Mexico_City"},
        }
        if attendees:
            event["attendees"] = [
                {"emailAddress": {"address": email}, "type": "required"}
                for email in attendees
            ]
        return await self._request("POST", "/me/events", json=event)
    
    async def delete_event(self, event_id: str) -> None:
        """Delete a calendar event."""
        await self._request("DELETE", f"/me/events/{event_id}")
    
    # ═══════════════════════════════════════════════════════════
    # ONEDRIVE
    # ═══════════════════════════════════════════════════════════
    
    async def get_files(self, folder_path: str = "root") -> dict:
        """Get files from OneDrive folder."""
        endpoint = f"/me/drive/{folder_path}/children" if folder_path == "root" else f"/me/drive/root:/{folder_path}:/children"
        return await self._request("GET", endpoint)
    
    async def upload_file(self, file_name: str, content: bytes) -> dict:
        """Upload a file to OneDrive root."""
        url = f"{self.base_url}/me/drive/root:/{file_name}:/content"
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                content=content
            )
            response.raise_for_status()
            return response.json()
    
    async def download_file(self, item_id: str) -> bytes:
        """Download a file from OneDrive."""
        url = f"{self.base_url}/me/drive/items/{item_id}/content"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, follow_redirects=True)
            return response.content
    
    async def delete_file(self, item_id: str) -> None:
        """Delete a file from OneDrive."""
        await self._request("DELETE", f"/me/drive/items/{item_id}")
