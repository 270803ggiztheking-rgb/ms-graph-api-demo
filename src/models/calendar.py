from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class DateTimeTimeZone(BaseModel):
    dateTime: str
    timeZone: str = "UTC"

class EmailAddressWrapper(BaseModel):
    address: EmailStr
    name: Optional[str] = None

class EventAttendee(BaseModel):
    type: str = "required"
    emailAddress: EmailAddressWrapper

class Event(BaseModel):
    id: str
    subject: Optional[str] = None
    start: DateTimeTimeZone
    end: DateTimeTimeZone
    location: Optional[dict] = None
    attendees: List[EventAttendee] = []

class CreateEventRequest(BaseModel):
    subject: str
    start_time: datetime
    end_time: datetime
    attendees: List[EmailStr] = []
    body: Optional[str] = None
    location: Optional[str] = None
