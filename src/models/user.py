from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfile(BaseModel):
    id: str
    displayName: Optional[str] = None
    mail: Optional[EmailStr] = None
    userPrincipalName: Optional[str] = None
    jobTitle: Optional[str] = None
    mobilePhone: Optional[str] = None
    officeLocation: Optional[str] = None
