from fastapi import Request, HTTPException, Depends
from src.core.graph_client import GraphClient
from src.services.auth_service import AuthService

# In-memory session storage (should be Redis in production)
sessions = {}


def get_auth_service() -> AuthService:
    return AuthService()


def get_access_token(request: Request) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return sessions[session_id]["access_token"]


def get_graph_client(access_token: str = Depends(
        get_access_token)) -> GraphClient:
    return GraphClient(access_token)
