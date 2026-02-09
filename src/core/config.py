from typing import List
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Microsoft Graph API Demo"
    API_V1_STR: str = "/api/v1"
    
    # Azure AD Settings
    CLIENT_ID: str
    CLIENT_SECRET: str
    TENANT_ID: str
    REDIRECT_URI: str = "http://localhost:8000/callback"
    GRAPH_API_ENDPOINT: str = "https://graph.microsoft.com/v1.0"
    SCOPES: str = "User.Read Mail.Read Mail.Send Calendars.ReadWrite Files.ReadWrite"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
