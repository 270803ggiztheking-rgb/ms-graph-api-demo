"""
Microsoft Graph API Demo - Main Application
FastAPI server with OAuth 2.0 authentication and Graph API endpoints
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import secrets

from src.auth import get_auth, MSGraphAuth
from src.graph_client import GraphClient
from src.config import get_settings

app = FastAPI(
    title="Microsoft Graph API Demo",
    description="Demo de integración con Microsoft Graph API usando OAuth 2.0",
    version="1.0.0"
)

# In-memory session storage (use Redis in production)
sessions: dict = {}


def get_access_token(request: Request) -> str:
    """Extract access token from session."""
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        raise HTTPException(status_code=401, detail="No autenticado. Por favor inicia sesión.")
    return sessions[session_id]["access_token"]


def get_graph_client(access_token: str = Depends(get_access_token)) -> GraphClient:
    """Dependency injection for GraphClient."""
    return GraphClient(access_token)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with login status."""
    session_id = request.cookies.get("session_id")
    logged_in = session_id and session_id in sessions
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MS Graph API Demo</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .btn {{ padding: 10px 20px; font-size: 16px; cursor: pointer; margin: 5px; }}
            .btn-primary {{ background: #0078d4; color: white; border: none; border-radius: 5px; }}
            .btn-danger {{ background: #d13438; color: white; border: none; border-radius: 5px; }}
            .endpoint {{ background: #f3f3f3; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            a {{ color: #0078d4; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h1>🔗 Microsoft Graph API Demo</h1>
        <p>Demostración de integración con Microsoft Graph API</p>
        
        {"<p>✅ <strong>Conectado</strong> - <a href='/logout'>Cerrar sesión</a></p>" if logged_in else "<p>❌ No conectado</p><a href='/login'><button class='btn btn-primary'>🔐 Iniciar sesión con Microsoft</button></a>"}
        
        {"<h2>📚 Endpoints disponibles:</h2><div class='endpoint'><strong>GET</strong> <a href='/me'>/me</a> - Información del usuario</div><div class='endpoint'><strong>GET</strong> <a href='/emails'>/emails</a> - Listar emails</div><div class='endpoint'><strong>GET</strong> <a href='/calendar'>/calendar</a> - Eventos del calendario</div><div class='endpoint'><strong>GET</strong> <a href='/files'>/files</a> - Archivos de OneDrive</div>" if logged_in else ""}
        
        <hr>
        <p><small>Desarrollado por Gael L. Chulim G. | <a href="https://github.com/tu-usuario">GitHub</a></small></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/login")
async def login(auth: MSGraphAuth = Depends(get_auth)):
    """Redirect to Microsoft login page."""
    state = secrets.token_urlsafe(32)
    auth_url = auth.get_auth_url(state=state)
    return RedirectResponse(url=auth_url)


@app.get("/callback")
async def callback(
    request: Request,
    code: Optional[str] = None,
    error: Optional[str] = None,
    auth: MSGraphAuth = Depends(get_auth)
):
    """OAuth 2.0 callback from Azure AD."""
    if error:
        raise HTTPException(status_code=400, detail=f"Error de autenticación: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió código de autorización")
    
    # Exchange code for tokens
    result = auth.acquire_token_by_code(code)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error_description", "Error al obtener token"))
    
    # Create session
    session_id = secrets.token_urlsafe(32)
    sessions[session_id] = {
        "access_token": result["access_token"],
        "account": result.get("id_token_claims", {})
    }
    
    response = RedirectResponse(url="/")
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
    return response


@app.get("/logout")
async def logout(request: Request):
    """Clear session and logout."""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        del sessions[session_id]
    
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# USER ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/me")
async def get_me(client: GraphClient = Depends(get_graph_client)):
    """Get current user profile."""
    return await client.get_me()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIL ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/emails")
async def get_emails(
    top: int = 10,
    client: GraphClient = Depends(get_graph_client)
):
    """Get user's emails."""
    return await client.get_emails(top=top)


@app.get("/emails/{message_id}")
async def get_email(
    message_id: str,
    client: GraphClient = Depends(get_graph_client)
):
    """Get specific email by ID."""
    return await client.get_email(message_id)


@app.post("/send-email")
async def send_email(
    to: list[str],
    subject: str,
    body: str,
    client: GraphClient = Depends(get_graph_client)
):
    """Send an email."""
    await client.send_email(to=to, subject=subject, body=body)
    return {"message": "Email enviado exitosamente"}


# ═══════════════════════════════════════════════════════════════════════════════
# CALENDAR ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/calendar")
async def get_calendar(
    top: int = 10,
    client: GraphClient = Depends(get_graph_client)
):
    """Get calendar events."""
    return await client.get_events(top=top)


@app.post("/calendar/event")
async def create_event(
    subject: str,
    start: str,
    end: str,
    attendees: Optional[list[str]] = None,
    body: str = "",
    client: GraphClient = Depends(get_graph_client)
):
    """Create a calendar event."""
    return await client.create_event(
        subject=subject,
        start=start,
        end=end,
        attendees=attendees,
        body=body
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ONEDRIVE ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/files")
async def get_files(
    folder: str = "root",
    client: GraphClient = Depends(get_graph_client)
):
    """Get files from OneDrive."""
    return await client.get_files(folder_path=folder)


@app.get("/files/{item_id}/download")
async def download_file(
    item_id: str,
    client: GraphClient = Depends(get_graph_client)
):
    """Download a file from OneDrive."""
    content = await client.download_file(item_id)
    return {"content": content.decode("utf-8", errors="ignore")}


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ms-graph-api-demo"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
