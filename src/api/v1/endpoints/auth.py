from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
import secrets
from src.services.auth_service import AuthService
from src.api.deps import get_auth_service, sessions

router = APIRouter()


@router.get("/login")
async def login(auth_service: AuthService = Depends(get_auth_service)):
    """
    Redirects to Microsoft Login.
    """
    state = secrets.token_urlsafe(32)
    auth_url = auth_service.get_auth_url(state=state)
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(
    request: Request,
    code: str,
    state: str = None,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Callback from Microsoft Auth.
    """
    result = auth_service.acquire_token_by_code(code)

    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "access_token": result["access_token"],
        "account": result.get("id_token_claims", {}),
    }

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600)
    return response


@router.get("/logout")
async def logout(request: Request):
    """
    Logs out the user.
    """
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]

    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response
