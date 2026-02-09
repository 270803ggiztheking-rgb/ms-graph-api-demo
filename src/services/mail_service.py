from typing import List
from src.core.graph_client import GraphClient
from src.models.mail import Message, SendMessageRequest


class MailService:
    def __init__(self, client: GraphClient):
        self.client = client

    async def get_messages(self, top: int = 10) -> List[Message]:
        data = await self.client.get(
            f"/me/messages?$top={top}&$orderby=receivedDateTime desc"
        )
        return [Message(**msg) for msg in data.get("value", [])]

    async def get_message(self, message_id: str) -> Message:
        data = await self.client.get(f"/me/messages/{message_id}")
        return Message(**data)

    async def send_message(self, request: SendMessageRequest) -> None:
        message_payload = {
            "message": {
                "subject": request.subject,
                "body": {"contentType": request.content_type, "content": request.body},
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in request.to
                ],
            },
            "saveToSentItems": True,
        }
        await self.client.post("/me/sendMail", data=message_payload)
