from typing import List
from src.core.graph_client import GraphClient
from src.models.calendar import Event, CreateEventRequest

class CalendarService:
    def __init__(self, client: GraphClient):
        self.client = client

    async def get_events(self, top: int = 10) -> List[Event]:
        data = await self.client.get(f"/me/events?$top={top}&$orderby=start/dateTime")
        return [Event(**event) for event in data.get("value", [])]

    async def create_event(self, request: CreateEventRequest) -> Event:
        event_payload = {
            "subject": request.subject,
            "body": {
                "contentType": "HTML",
                "content": request.body or ""
            },
            "start": {
                "dateTime": request.start_time.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": request.end_time.isoformat(),
                "timeZone": "UTC"
            },
            "location": {
                "displayName": request.location
            }
        }
        
        if request.attendees:
            event_payload["attendees"] = [
                {
                    "emailAddress": {"address": email},
                    "type": "required"
                } for email in request.attendees
            ]

        data = await self.client.post("/me/events", data=event_payload)
        return Event(**data)
