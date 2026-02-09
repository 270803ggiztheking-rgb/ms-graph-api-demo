from fastapi import APIRouter, Depends
from typing import List
from src.core.graph_client import GraphClient
from src.services.calendar_service import CalendarService
from src.models.calendar import Event, CreateEventRequest
from src.api.deps import get_graph_client

router = APIRouter()


@router.get("/", response_model=List[Event])
async def get_events(
        top: int = 10,
        client: GraphClient = Depends(get_graph_client)):
    """
    Get calendar events.
    """
    service = CalendarService(client)
    return await service.get_events(top=top)


@router.post("/", response_model=Event)
async def create_event(request: CreateEventRequest,
                       client: GraphClient = Depends(get_graph_client)):
    """
    Create a calendar event.
    """
    service = CalendarService(client)
    return await service.create_event(request)
