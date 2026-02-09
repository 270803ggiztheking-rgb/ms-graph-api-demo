from src.core.graph_client import GraphClient
from src.models.user import UserProfile


class UserService:
    def __init__(self, client: GraphClient):
        self.client = client

    async def get_me(self) -> UserProfile:
        data = await self.client.get("/me")
        return UserProfile(**data)
