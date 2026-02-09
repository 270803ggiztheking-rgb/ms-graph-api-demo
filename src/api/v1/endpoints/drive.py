from fastapi import APIRouter, Depends, UploadFile, File
from typing import List
from fastapi.responses import Response
from src.core.graph_client import GraphClient
from src.services.drive_service import DriveService
from src.models.drive import FileItem
from src.api.deps import get_graph_client

router = APIRouter()

@router.get("/files", response_model=List[FileItem])
async def get_files(folder: str = "root", client: GraphClient = Depends(get_graph_client)):
    """
    Get files from OneDrive.
    """
    service = DriveService(client)
    return await service.get_files(folder_path=folder)

@router.get("/files/{item_id}/download")
async def download_file(item_id: str, client: GraphClient = Depends(get_graph_client)):
    """
    Download a file from OneDrive.
    """
    service = DriveService(client)
    content = await service.download_file(item_id)
    return Response(content=content, media_type="application/octet-stream")

@router.post("/files/upload", response_model=FileItem)
async def upload_file(file: UploadFile = File(...), client: GraphClient = Depends(get_graph_client)):
    """
    Upload a file to OneDrive root.
    """
    service = DriveService(client)
    content = await file.read()
    return await service.upload_file(file.filename, content)
