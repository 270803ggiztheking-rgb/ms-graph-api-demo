from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileItem(BaseModel):
    id: str
    name: str
    size: Optional[int] = None
    webUrl: Optional[str] = None
    createdDateTime: Optional[datetime] = None
    lastModifiedDateTime: Optional[datetime] = None
    file: Optional[dict] = None
    folder: Optional[dict] = None
