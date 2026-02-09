from fastapi import APIRouter, Depends
from typing import List
from src.core.graph_client import GraphClient
from src.services.mail_service import MailService
from src.models.mail import Message, SendMessageRequest
from src.api.deps import get_graph_client

router = APIRouter()


@router.get("/", response_model=List[Message])
async def get_emails(
        top: int = 10,
        client: GraphClient = Depends(get_graph_client)):
    """
    Get user's emails.
    """
    service = MailService(client)
    return await service.get_messages(top=top)


@router.get("/{message_id}", response_model=Message)
async def get_email(
        message_id: str,
        client: GraphClient = Depends(get_graph_client)):
    """
    Get specific email by ID.
    """
    service = MailService(client)
    return await service.get_message(message_id)


@router.post("/send")
async def send_email(request: SendMessageRequest,
                     client: GraphClient = Depends(get_graph_client)):
    """
    Send an email.
    """
    service = MailService(client)
    await service.send_message(request)
    return {"message": "Email sent successfully"}
