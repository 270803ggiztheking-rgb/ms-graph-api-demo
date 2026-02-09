from fastapi import APIRouter, Depends
from src.core.graph_client import GraphClient
from src.services.user_service import UserService
from src.models.user import UserProfile
from src.api.deps import get_graph_client

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_me(client: GraphClient = Depends(get_graph_client)):
    """
    Get current user profile.
    """
    service = UserService(client)
    return await service.get_me()
