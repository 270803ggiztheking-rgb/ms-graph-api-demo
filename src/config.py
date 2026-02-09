"""
Microsoft Graph API Demo - Configuration
Environment variables and settings management
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    client_id: str
    client_secret: str
    tenant_id: str
    redirect_uri: str = "http://localhost:8000/callback"
    scopes: str = "User.Read Mail.Read Mail.Send Calendars.ReadWrite Files.ReadWrite"
    graph_api_endpoint: str = "https://graph.microsoft.com/v1.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
