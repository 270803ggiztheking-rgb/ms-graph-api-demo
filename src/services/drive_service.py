from typing import List
from src.core.graph_client import GraphClient
from src.models.drive import FileItem

class DriveService:
    def __init__(self, client: GraphClient):
        self.client = client

    async def get_files(self, folder_path: str = "root") -> List[FileItem]:
        endpoint = f"/me/drive/{folder_path}/children" if folder_path == "root" else f"/me/drive/root:/{folder_path}:/children"
        data = await self.client.get(endpoint)
        return [FileItem(**item) for item in data.get("value", [])]

    async def download_file(self, item_id: str) -> bytes:
        return await self.client.get(f"/me/drive/items/{item_id}/content")
    
    async def upload_file(self, filename: str, content: bytes) -> FileItem:
        # Simple upload to root
        endpoint = f"/me/drive/root:/{filename}:/content"
        data = await self.client.put(endpoint, data=content)
        return FileItem(**data)
