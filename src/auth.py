"""
Microsoft Graph API Demo - Auth Module
OAuth 2.0 authentication with Azure AD using MSAL
"""

import msal
from functools import lru_cache
from src.config import get_settings


class MSGraphAuth:
    """Handles Microsoft Graph API authentication using MSAL."""

    def __init__(self):
        self.settings = get_settings()
        self.authority = f"https://login.microsoftonline.com/{
            self.settings.tenant_id}"
        self.scopes = self.settings.scopes.split()

        self._msal_app = msal.ConfidentialClientApplication(
            client_id=self.settings.client_id,
            client_credential=self.settings.client_secret,
            authority=self.authority,
        )

    def get_auth_url(self, state: str = None) -> str:
        """Generate the authorization URL for OAuth 2.0 flow."""
        return self._msal_app.get_authorization_request_url(
            scopes=self.scopes, state=state, redirect_uri=self.settings.redirect_uri)

    def acquire_token_by_code(self, code: str) -> dict:
        """Exchange authorization code for access token."""
        result = self._msal_app.acquire_token_by_authorization_code(
            code=code, scopes=self.scopes, redirect_uri=self.settings.redirect_uri)
        return result

    def acquire_token_silent(self, account: dict) -> dict:
        """Acquire token silently from cache."""
        result = self._msal_app.acquire_token_silent(
            scopes=self.scopes, account=account
        )
        return result

    def get_accounts(self) -> list:
        """Get all accounts from token cache."""
        return self._msal_app.get_accounts()


@lru_cache()
def get_auth() -> MSGraphAuth:
    """Dependency injection for MSGraphAuth."""
    return MSGraphAuth()
