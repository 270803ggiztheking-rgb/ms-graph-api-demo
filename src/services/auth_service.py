import msal
from typing import Dict
from src.core.config import settings
from src.core.exceptions import AuthException
from loguru import logger


class AuthService:
    def __init__(self):
        self.authority = f"https://login.microsoftonline.com/{
            settings.TENANT_ID}"
        self.scopes = settings.SCOPES.split()

        self._msal_app = msal.ConfidentialClientApplication(
            client_id=settings.CLIENT_ID,
            client_credential=settings.CLIENT_SECRET,
            authority=self.authority,
        )

    def get_auth_url(self, state: str) -> str:
        return self._msal_app.get_authorization_request_url(
            scopes=self.scopes, state=state, redirect_uri=settings.REDIRECT_URI
        )

    def acquire_token_by_code(self, code: str) -> Dict:
        try:
            result = self._msal_app.acquire_token_by_authorization_code(
                code=code, scopes=self.scopes, redirect_uri=settings.REDIRECT_URI)
            if "error" in result:
                logger.error(f"Auth Error: {result.get('error_description')}")
                raise AuthException(
                    f"Authentication failed: {result.get('error_description')}"
                )
            return result
        except Exception as e:
            if isinstance(e, AuthException):
                raise
            logger.exception("Unexpected error during token acquisition")
            raise AuthException(f"Authentication failed: {str(e)}")
