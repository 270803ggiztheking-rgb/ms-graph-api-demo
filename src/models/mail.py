from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class EmailAddress(BaseModel):
    name: Optional[str] = None
    address: EmailStr


class Recipient(BaseModel):
    emailAddress: EmailAddress


class MessageBody(BaseModel):
    contentType: str
    content: str


class Message(BaseModel):
    id: str
    subject: Optional[str] = None
    bodyPreview: Optional[str] = None
    body: Optional[MessageBody] = None
    sender: Optional[Recipient] = None
    from_: Optional[Recipient] = Field(None, alias="from")
    toRecipients: List[Recipient] = []
    receivedDateTime: Optional[datetime] = None
    isRead: Optional[bool] = None


class SendMessageRequest(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str
    content_type: str = "HTML"
